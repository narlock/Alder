from flask import Blueprint, request, jsonify
from app.model.user_model import User
from app.schema.user_schema import UserSchema
from app import db
from sqlalchemy import desc  # Import desc for descending order

# Define a new Blueprint for user-related routes
user_bp = Blueprint('user_bp', __name__)

# Initialize UserSchema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Endpoint to retrieve a user by ID
@user_bp.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    # Query the User model to find a user by the given ID
    user = User.query.get(id)
    if user is None:
        # Return a 404 error if the user is not found
        return jsonify({'message': 'User not found'}), 404

    # Serialize the user object to JSON format using the UserSchema
    return jsonify(user_schema.dump(user))

# Endpoint to create a new user
@user_bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    # Validate the data against the schema
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_user = User(
        id=data['id'],
        tokens=data['tokens'],
        stime=data['stime'],
        hex=data.get('hex'),
        trivia=data.get('trivia')
    )
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 201

# Endpoint to update an existing user
@user_bp.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()

    # Validate the data against the schema
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    user.tokens = data['tokens']
    user.stime = data['stime']
    user.hex = data.get('hex')
    user.trivia = data.get('trivia')

    db.session.commit()

    return jsonify(user_schema.dump(user))

# Endpoint to partially update an existing user
@user_bp.route('/user/<int:id>', methods=['PATCH'])
def partial_update_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()

    # Validate the partial data against the schema, only for provided fields
    errors = user_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    # Update only the fields that are present in the request data
    if 'tokens' in data:
        user.tokens = data['tokens']
    if 'stime' in data:
        user.stime = data['stime']
    if 'hex' in data:
        user.hex = data.get('hex')
    if 'trivia' in data:
        user.trivia = data.get('trivia')

    db.session.commit()

    return jsonify(user_schema.dump(user))

# Endpoint to delete a user by ID
@user_bp.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    # Return 204 No Content
    return '', 204

# Set Timezone endpoint
@user_bp.route('/user/<int:id>/timezone', methods=['PUT'])
def set_user_timezone(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    
    # Check if timezone is provided in the request body
    if 'timezone' not in data:
        return jsonify({'message': 'Timezone is required'}), 400

    timezone = data['timezone']

    # Update user's timezone if valid
    user.timezone = timezone
    db.session.commit()

    return jsonify(user_schema.dump(user))

# Search endpoint
@user_bp.route('/user/search', methods=['POST'])
def search_users():
    data = request.get_json()

    # Optional conditions and limit
    conditions = data.get('conditions', [])
    limit = data.get('limit')
    sort_field = data.get('sort_field')  # Change this to match your request body

    query = User.query

    # Apply conditions if provided
    for condition in conditions:
        field = condition.get('field')
        cond = condition.get('condition')
        value = condition.get('value')

        if not field or not cond or value is None:
            return jsonify({'message': 'Each condition must have a field, condition, and value'}), 400

        # Map the field name to the actual model attribute
        if field == 'stime':
            column = User.stime
        elif field == 'trivia':
            column = User.trivia
        elif field == 'tokens':
            column = User.tokens
        elif field == 'hex':
            column = User.hex
        else:
            return jsonify({'message': f'Invalid field: {field}'}), 400

        # Build the query based on the condition
        if cond == 'eq':
            query = query.filter(column == value)
        elif cond == 'lt':
            query = query.filter(column < value)
        elif cond == 'gt':
            query = query.filter(column > value)
        elif cond == 'le':
            query = query.filter(column <= value)
        elif cond == 'ge':
            query = query.filter(column >= value)
        elif cond == 'ne':
            query = query.filter(column != value)
        elif cond == 'like':
            query = query.filter(column.like(f'%{value}%'))
        else:
            return jsonify({'message': f'Invalid condition: {cond}'}), 400

    # Apply sorting if provided (highest to lowest)
    if sort_field:
        if sort_field == 'stime':
            sort_column = User.stime
        elif sort_field == 'trivia':
            sort_column = User.trivia
        elif sort_field == 'tokens':
            sort_column = User.tokens
        elif sort_field == 'hex':
            sort_column = User.hex
        else:
            return jsonify({'message': f'Invalid sort field: {sort_field}'}), 400

        query = query.order_by(desc(sort_column))  # Ensure sorting is in descending order

    # Apply the limit if provided
    if limit is not None:
        try:
            limit = int(limit)
            query = query.limit(limit)
        except ValueError:
            return jsonify({'message': 'Invalid limit value. Must be an integer.'}), 400

    users = query.all()
    return jsonify(users_schema.dump(users))
