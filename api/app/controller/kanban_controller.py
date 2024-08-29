from flask import Blueprint, request, jsonify
from app.model.kanban_model import KanbanModel
from app.schema.kanban_schema import KanbanSchema
from app import db

# Define Kanban Blueprint
kanban_bp = Blueprint('kanban_bp', __name__)

# Initialize KanbanSchema
kanban_schema = KanbanSchema()
kanban_many_schema = KanbanSchema(many=True)

@kanban_bp.route('/kanban', methods=['POST'])
def create_kanban_item():
    """
    Creates a kanban item given request body. The
    request body contains a user_id (required), an
    item_name (required). It will default the column
    to the string 'todo' since the item was just created.
    Optional fields include priority_number, tag_name,
    and velocity.
    """
    # Retrieve the JSON payload
    data = request.get_json()

    # Validate the data against the schema
    errors = kanban_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Configure new Kanban item with default column_name as 'todo'
    new_kanban_item = KanbanModel(
        user_id=data['user_id'],
        item_name=data['item_name'],
        column_name='todo',  # Default column
        priority_number=data.get('priority_number'),
        tag_name=data.get('tag_name'),
        velocity=data.get('velocity')
    )

    # Add and commit the new Kanban item to the database
    db.session.add(new_kanban_item)
    db.session.commit()

    # Serialize the new kanban item to JSON format using the schema
    return jsonify(kanban_schema.dump(new_kanban_item)), 201

@kanban_bp.route('/kanban/user/<int:user_id>', methods=['GET'])
def get_user_kanban_items(user_id):
    """
    Gets the kanban items that match the user_id provided. Provides
    three separate lists as the response that correspond to the
    column. There will be a 'todo' list, which contains the list
    of all of the user's kanban items in the todo list, a 'doing'
    list, which contains the list of all of the user's kanban items
    in the doing list, and a 'done' list, which contains the list
    of all of the user's kanban items in the done list.
    """
    # Query the KanbanModel to find items by user_id and group by column_name
    todo_items = KanbanModel.query.filter_by(user_id=user_id, column_name='todo').all()
    doing_items = KanbanModel.query.filter_by(user_id=user_id, column_name='doing').all()
    done_items = KanbanModel.query.filter_by(user_id=user_id, column_name='done').all()

    # Return the items grouped by column
    return jsonify({
        'todo': kanban_many_schema.dump(todo_items),
        'doing': kanban_many_schema.dump(doing_items),
        'done': kanban_many_schema.dump(done_items)
    }), 200

@kanban_bp.route('/kanban/<int:id>', methods=['POST'])
def move_kanban_item_column(id):
    """
    Given the kanban item id. First check if the calling user
    denoted in the request body as the 'user_id' field contains
    the id provided for the kanban item in the path. If they do,
    then move the kanban item to the next column if no specific
    column is provided. The next column is defined as follows:
    - If the current kanban item is in the 'todo' column, it will
    be moved to the 'doing' column.
    - If the current kanban item is in the 'doing' column, it will
    be moved to the 'done' column.
    - If the current kanban item is in the 'done' column, it will
    not be moved.
    If a column is provided in the 'column' field in the request
    body, then move the item to that column. (It must be either
    'todo', 'doing', or 'done')
    """
    # Retrieve the JSON payload
    data = request.get_json()

    # Retrieve the Kanban item by its ID
    kanban_item = KanbanModel.query.get(id)
    if kanban_item is None:
        return jsonify({'message': f'Kanban item not found for id {id}'}), 404

    # Verify that the user_id matches
    if kanban_item.user_id != data.get('user_id'):
        return jsonify({'message': 'You do not have permission to move this kanban item'}), 403

    # Move the kanban item to the next column if no specific column is provided
    next_column = data.get('column')
    if not next_column:
        if kanban_item.column_name == 'todo':
            kanban_item.column_name = 'doing'
        elif kanban_item.column_name == 'doing':
            kanban_item.column_name = 'done'
    else:
        if next_column in ['todo', 'doing', 'done']:
            kanban_item.column_name = next_column
        else:
            return jsonify({'message': 'Invalid column name'}), 400

    # Commit the changes to the database
    db.session.commit()

    # Serialize the updated kanban item to JSON format using the schema
    return jsonify(kanban_schema.dump(kanban_item)), 200

@kanban_bp.route('/kanban/<int:id>', methods=['PATCH'])
def update_kanban_item_details(id):
    """
    Given the kanban item id. First check if the calling user
    denoted in the request body as the 'user_id' field contains
    the id provided for the kanban item in the path. If they do,
    then update the properties of the kanban task with the given
    id based on what is provided in the request body. These fields
    can be
    - `item_name`
    - `priority_number`
    - `tag_name`
    - and `velocity`
    This is a partial update, so they are not all required. Update
    the ones that are provided in the request body.

    If the user does not have the id of the kanban item in their
    list of kanban items, they cannot update the kanban item
    since they do not own it.
    """
    # Retrieve the JSON payload
    data = request.get_json()

    # Retrieve the Kanban item by its ID
    kanban_item = KanbanModel.query.get(id)
    if kanban_item is None:
        return jsonify({'message': f'Kanban item not found for id {id}'}), 404

    # Verify that the user_id matches
    if kanban_item.user_id != data.get('user_id'):
        return jsonify({'message': 'You do not have permission to update this kanban item'}), 403

    # Update fields if they are present in the request body
    if 'item_name' in data:
        kanban_item.item_name = data['item_name']
    if 'priority_number' in data:
        kanban_item.priority_number = data['priority_number']
    if 'tag_name' in data:
        kanban_item.tag_name = data['tag_name']
    if 'velocity' in data:
        kanban_item.velocity = data['velocity']

    # Commit the changes to the database
    db.session.commit()

    # Serialize the updated kanban item to JSON format using the schema
    return jsonify(kanban_schema.dump(kanban_item)), 200

@kanban_bp.route('/kanban/user/<int:user_id>/<int:id>', methods=['DELETE'])
def delete_kanban_item(user_id, id):
    """
    Given the user_id and the kanban id. Delete the kanban item if
    the user has the kanban item in their list of kanban items. 
    """
    # Retrieve the Kanban item by its ID
    kanban_item = KanbanModel.query.get(id)
    if kanban_item is None:
        return jsonify({'message': f'Kanban item not found for id {id}'}), 404

    # Verify that the user_id matches
    if kanban_item.user_id != user_id:
        return jsonify({'message': 'You do not have permission to delete this kanban item'}), 403

    # Delete the found kanban item from the database
    db.session.delete(kanban_item)
    db.session.commit()

    # Return 204 No Content
    return '', 204

@kanban_bp.route('/kanban/user/<int:user_id>', methods=['DELETE'])
def delete_completed_kanban_items(user_id):
    """
    Given the user_id, delete all Kanban items that are marked as
    completed (i.e., in the 'done' column).
    """
    # Query to find all Kanban items in the 'done' column for the user
    completed_items = KanbanModel.query.filter_by(user_id=user_id, column_name='done').all()

    # If no completed items are found, return 404
    if not completed_items:
        return jsonify({'message': 'No completed Kanban items found for this user'}), 404

    # Delete all completed items
    for item in completed_items:
        db.session.delete(item)

    # Commit the deletions to the database
    db.session.commit()

    # Return 204 No Content to indicate successful deletion
    return '', 204

@kanban_bp.route('/kanban/user/<int:user_id>/tag/<string:tag_name>', methods=['GET'])
def get_user_kanban_items_by_tag(user_id, tag_name):
    """
    Given the user_id, search for all items that match the given tag_name.
    Provides three separate lists as the response that correspond to the
    column. There will be a 'todo' list, which contains the list
    of all of the user's kanban items in the todo list, a 'doing'
    list, which contains the list of all of the user's kanban items
    in the doing list, and a 'done' list, which contains the list
    of all of the user's kanban items in the done list.
    """
    # Query the KanbanModel to find items by user_id and tag_name, grouped by column_name
    todo_items = KanbanModel.query.filter_by(user_id=user_id, tag_name=tag_name, column_name='todo').all()
    doing_items = KanbanModel.query.filter_by(user_id=user_id, tag_name=tag_name, column_name='doing').all()
    done_items = KanbanModel.query.filter_by(user_id=user_id, tag_name=tag_name, column_name='done').all()

    # Return the items grouped by column
    return jsonify({
        'todo': kanban_many_schema.dump(todo_items),
        'doing': kanban_many_schema.dump(doing_items),
        'done': kanban_many_schema.dump(done_items)
    }), 200