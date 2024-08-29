from flask import Blueprint, request, jsonify
from app.model.accomplishment_model import Accomplishment
from app.schema.accomplishment_schema import AccomplishmentSchema
from app import db

# Define accomplishment Blueprint
accomplishment_bp = Blueprint('accomplishment_bp', __name__)

# Initialize AccomplishmentSchema
accomplishment_schema = AccomplishmentSchema()
accomplishments_schema = AccomplishmentSchema(many=True)

@accomplishment_bp.route('/accomplishments/<int:user_id>', methods=['GET'])
def get_accomplishments_by_user_id(user_id):
    """
    Gets all of the accomplishments that match the user_id
    """
    
    # Query all Accomplishment records for the given user_id
    accomplishment_records = Accomplishment.query.filter_by(user_id=user_id).all()

    # Check if any records exist
    if not accomplishment_records:
        return jsonify({'error': f'No accomplishments found for user with id: {user_id}'}), 404
    
    # If found, serialize the accomplishments object to JSON using the schema
    return jsonify(accomplishments_schema.dump(accomplishment_records))

@accomplishment_bp.route('/accomplishments', methods=['POST'])
def create_accomplishment():
    """
    Creates an accomplishment for the user based on provided message
    in the request body
    """

    # Load the request JSON data into the AccomplishmentSchema object
    data = request.get_json()
    errors = accomplishment_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    # Create a new Accomplishment object from the validated data
    new_accomplishment = Accomplishment(
        user_id=data['user_id'],
        msg=data['msg']
    )

    # Add the new accomplishment to the session and commit to the database
    db.session.add(new_accomplishment)
    db.session.commit()

    # Return the created accomplishment as the response
    return jsonify(accomplishment_schema.dump(new_accomplishment)), 201

@accomplishment_bp.route('/accomplishments/<int:user_id>', methods=['DELETE'])
def delete_accomplishments_by_user_id(user_id):
    """
    Delete all accomplishments that match the user_id
    """

    # Query all accomplishments by the given user_id
    accomplishment_records = Accomplishment.query.filter_by(user_id=user_id).all()

    # Check if any records exist
    if not accomplishment_records:
        return jsonify({'error': f'No accomplishments found for the user with id: {user_id}'})
    
    # Delete all records that were found
    for record in accomplishment_records:
        db.session.delete(record)

    db.session.commit()

    # Return 204 No Content
    return '', 204