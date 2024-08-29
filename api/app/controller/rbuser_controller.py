from flask import Blueprint, request, jsonify
from app.model.rbuser_model import RogueBossUserModel
from app.schema.rbuser_schema import RogueBossUserSchema
from app import db
from sqlalchemy import desc

# Define Rogue Boss user Blueprint
rbuser_bp = Blueprint('rbuser_bp', __name__)

# Initialize RogueBossUserSchema
rogue_boss_user_schema = RogueBossUserSchema()
rogue_boss_users_schema = RogueBossUserSchema(many=True)

@rbuser_bp.route('/rb/<int:user_id>', methods=['GET'])
def get_rogue_boss_user(user_id):
    """
    Gets the Rogue Boss User by the given user_id
    """

    # Query the RogueBossUserModel to find a rbUser by the given ID
    rb_user = RogueBossUserModel.query.get(user_id)
    if rb_user is None:
        # Return a 404 error if the rbUser is not found
        return jsonify({'message': f'Rogue Boss User not found for user_id {user_id}'}), 404
    
    # Serialize the rb_user object to JSON format using the schema
    return jsonify(rogue_boss_user_schema.dump(rb_user))

@rbuser_bp.route('/rb', methods=['POST'])
def create_rogue_boss_user():
    """
    Creates a Rogue Boss user given the user_id and rbtype
    """

    # Retrieve the JSON payload
    data = request.get_json()

    # Validate the data against the schema
    errors = rogue_boss_user_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    # Configure new Rogue Boss user to write
    new_rb_user = RogueBossUserModel(
        user_id=data['user_id'],
        rbtype=data['rbtype'],
        xp=0,
        model=0,
        purchased_models=''
    )

    # Write the new Rogue Boss user to the database
    db.session.add(new_rb_user)
    db.session.commit()

    return jsonify(rogue_boss_user_schema.dump(new_rb_user))

@rbuser_bp.route('/rb/<int:user_id>', methods=['PATCH'])
def update_rogue_boss_user(user_id):
    """
    A partial update to a Rogue Boss user. The rbtype,
    model, and purchased_models values can be updated by
    using this endpoint when they are provided in the
    request body.
    """

    # Retrieve the JSON payload
    data = request.get_json()

    # Query the RogueBossUserModel to find the user by the given ID
    rb_user = RogueBossUserModel.query.get(user_id)
    if rb_user is None:
        return jsonify({'message': f'Rogue Boss User not found for user_id {user_id}'}), 404

    # Update fields if they are present in the request body
    if 'rbtype' in data:
        rb_user.rbtype = data['rbtype']
    if 'model' in data:
        rb_user.model = data['model']
    if 'purchased_models' in data:
        rb_user.purchased_models = data['purchased_models']

    # Commit the changes to the database
    db.session.commit()

    # Serialize the updated rb_user object to JSON format using the schema
    return jsonify(rogue_boss_user_schema.dump(rb_user)), 200

@rbuser_bp.route('/rb/<int:user_id>/xp', methods=['PATCH'])
def add_xp_to_rogue_boss_user(user_id):
    """
    Add experience points to a Rogue Boss user given its id and
    a request body containing xp with the amount to add.
    """

    # Retrieve the JSON payload
    data = request.get_json()

    # Validate the input data to ensure 'xp' is present and is an integer
    if 'xp' not in data or not isinstance(data['xp'], int):
        return jsonify({'message': 'Invalid or missing xp value'}), 400
    
    # Query the RogueBossUserModel to find the user by the given ID
    rb_user = RogueBossUserModel.query.get(user_id)
    if rb_user is None:
        # Return a 404 error if the Rogue Boss User is not found
        return jsonify({'message': f'Rogue Boss User not found for user_id {user_id}'}), 404
    
    # Add the specified xp to the user's current xp
    rb_user.xp += data['xp']

    # Commit the changes to the database
    db.session.commit()

    # Serialize the updated rb_user object to JSON format using the schema
    return jsonify(rogue_boss_user_schema.dump(rb_user)), 200

@rbuser_bp.route('/rb/<int:user_id>', methods=['DELETE'])
def delete_rogue_boss_user(user_id):
    """
    Delete a Rogue Boss user given user_id
    """
    rb_user = RogueBossUserModel.query.get(user_id)
    if rb_user is None:
        return jsonify({'message': f'Rogue Boss User not found for user_id {user_id}'}), 404
    
    db.session.delete(rb_user)
    db.session.commit()

    # Return 204 No Content
    return '', 204

@rbuser_bp.route('/rb/top', methods=['GET'])
def top_rogue_boss_users():
    """
    Retrieve the top Rogue Boss users (indicated by their xp value)
    The limit query parameter is used to determine how many users
    to return. If this query parameter is not provided, it will
    default to 10.
    """

    # Get the limit from query parameters, defaulting to 10 if not provided
    limit = request.args.get('limit', default=10, type=int)

    # Query the RogueBossUserModel to get the top users sorted by xp in descending order
    top_users = RogueBossUserModel.query.order_by(desc(RogueBossUserModel.xp)).limit(limit).all()

    # Serialize the list of top users to JSON format using the schema
    return jsonify(rogue_boss_users_schema.dump(top_users)), 200