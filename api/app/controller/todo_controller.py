from flask import Blueprint, request, jsonify
from app.model.todo_model import TodoModel
from app.schema.todo_schema import TodoSchema
from app import db
from datetime import datetime, timedelta

# Define Todo Blueprint
todo_bp = Blueprint('todo_bp', __name__)

# Initialize TodoSchema
todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

@todo_bp.route('/todo/incomplete/<int:user_id>', methods=['GET'])
def get_incomplete_todo_items(user_id):
    """
    Gets all of the todo items for the user with user_id where
    the completed_date column is null.
    """
    # Query the TodoModel to find incomplete todos for the user
    incomplete_todos = TodoModel.query.filter_by(user_id=user_id, completed_date=None).all()

    # Serialize the list of incomplete todos to JSON format using the schema
    return jsonify(todos_schema.dump(incomplete_todos)), 200

@todo_bp.route('/todo/complete/<int:user_id>', methods=['GET'])
def get_complete_todo_items(user_id):
    """
    Gets all of the todo items for the user with user_id where
    the completed_date column is not null.
    """
    # Query the TodoModel to find completed todos for the user
    complete_todos = TodoModel.query.filter(TodoModel.user_id == user_id, TodoModel.completed_date.isnot(None)).all()

    # Serialize the list of complete todos to JSON format using the schema
    return jsonify(todos_schema.dump(complete_todos)), 200

@todo_bp.route('/todo', methods=['POST'])
def create_todo_item():
    """
    Given a user_id and an item_name, create a todo item
    for the user_id and item_name.
    """
    # Retrieve the JSON payload
    data = request.get_json()

    # Validate the data against the schema
    errors = todo_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Configure new Todo item to write
    new_todo = TodoModel(
        user_id=data['user_id'],
        item_name=data['item_name'],
        completed_date=None
    )

    # Write the new Todo item to the database
    db.session.add(new_todo)
    db.session.commit()

    # Serialize the new todo item to JSON format using the schema
    return jsonify(todo_schema.dump(new_todo)), 201

@todo_bp.route('/todo/<int:id>', methods=['DELETE'])
def delete_todo_item(id):
    """
    Given the ID of the todo item, delete the todo item.
    """
    # Query the TodoModel to find the todo by its ID
    todo_item = TodoModel.query.get(id)
    if todo_item is None:
        return jsonify({'message': f'Todo item not found for id {id}'}), 404

    # Delete the found todo item from the database
    db.session.delete(todo_item)
    db.session.commit()

    # Return 204 No Content
    return '', 204

@todo_bp.route('/todo/<int:id>', methods=['PATCH'])
def update_todo_item_name(id):
    """
    Given the ID of the todo item, along with a request body
    containing a new item_name, change the item_name for
    the todo item name.
    """
    # Retrieve the JSON payload
    data = request.get_json()

    # Validate the input data to ensure 'item_name' is present
    if 'item_name' not in data or not isinstance(data['item_name'], str):
        return jsonify({'message': 'Invalid or missing item_name value'}), 400

    # Query the TodoModel to find the todo by its ID
    todo_item = TodoModel.query.get(id)
    if todo_item is None:
        return jsonify({'message': f'Todo item not found for id {id}'}), 404

    # Update the item_name of the todo item
    todo_item.item_name = data['item_name']

    # Commit the changes to the database
    db.session.commit()

    # Serialize the updated todo item to JSON format using the schema
    return jsonify(todo_schema.dump(todo_item)), 200

@todo_bp.route('/todo/<int:id>/complete', methods=['POST'])
def complete_todo_item(id):
    """
    Given the ID of the todo item, set the completed_date as the
    current date.
    """
    # Query the TodoModel to find the todo item by its ID
    todo_item = TodoModel.query.get(id)
    if todo_item is None:
        return jsonify({'message': f'Todo item not found for id {id}'}), 404

    # Set the completed_date to the current date
    todo_item.completed_date = datetime.utcnow().date()

    # Commit the change to the database
    db.session.commit()

    # Serialize the updated todo item to JSON format using the schema
    return jsonify(todo_schema.dump(todo_item)), 200

@todo_bp.route('/todo/complete/<int:user_id>', methods=['DELETE'])
def delete_old_completed_todo_items(user_id):
    """
    Given the user_id, delete all completed todo items that are
    older than a day with respect to the current date. If today is
    August 23rd, 2024, delete all items that land on August 22nd and
    past.
    """
    # Calculate the date of yesterday
    yesterday = datetime.utcnow().date() - timedelta(days=1)

    # Query and delete completed todo items older than yesterday for the user
    old_todos = TodoModel.query.filter(TodoModel.user_id == user_id, TodoModel.completed_date <= yesterday).all()

    # If no old todos are found, return 404
    if not old_todos:
        return jsonify({'message': 'No old completed todo items found to delete'}), 404

    for todo in old_todos:
        db.session.delete(todo)

    # Commit the deletion to the database
    db.session.commit()

    # Return 204 No Content
    return '', 204

@todo_bp.route('/todo/all/<int:user_id>', methods=['DELETE'])
def delete_all_todo_items_by_user_id(user_id):
    """
    Given the user_id, delete all todo items associated with the user.
    """
    # Query the TodoModel to find all todo items by user_id
    todos = TodoModel.query.filter_by(user_id=user_id).all()

    # If no todos are found, return 404
    if not todos:
        return jsonify({'message': f'No todo items found for user_id {user_id}'}), 404

    # Delete all found todo items from the database
    for todo in todos:
        db.session.delete(todo)

    # Commit the deletion to the database
    db.session.commit()

    # Return 204 No Content
    return '', 204
