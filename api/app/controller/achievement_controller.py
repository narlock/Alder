from flask import Blueprint, request, jsonify
from app.model.achievement_model import Achievement
from app.schema.achievement_schema import AchievementSchema
from app import db

# Define achievement Blueprint
achievement_bp = Blueprint('achievement_bp', __name__)

# Initialize achievement schema
achievement_schema = AchievementSchema()
achievements_schema = AchievementSchema(many=True)

@achievement_bp.route('/achievements/<int:user_id>', methods=['GET'])
def get_achievements_by_user_id(user_id):
    """
    Gets all of the achievements that match the user_id
    """

    # Query all achievement records for the given user_id
    achievement_records = Achievement.query.filter_by(user_id=user_id).all()

    # Check if any records exist
    if not achievement_records:
        return jsonify({'error': f'No achievements found for user with id: {user_id}'}), 404
    
    # If found, serialize the achievement records to JSON using the schema
    return jsonify(achievements_schema.dump(achievement_records))

@achievement_bp.route('/achievements', methods=['POST'])
def create_achievement():
    """
    Creates an achievement entry for the provided id and user_id
    in the request body
    """

    # Load the request JSON data into the AchievementSchema object
    data = request.get_json()
    errors = achievement_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    # Create the new achievement object from the validated data
    new_achievement = Achievement(
        id=data['id'],
        user_id=data['user_id']
    )

    # Add the new achievement to the session and commit to the database
    db.session.add(new_achievement)
    db.session.commit()

    # Return the created achievement as the response
    return jsonify(achievement_schema.dump(new_achievement)), 201

@achievement_bp.route('/achievements/<int:user_id>', methods=['DELETE'])
def delete_achievements_by_user_id(user_id):
    """
    Delete all achievements that match the user_id
    """

    # Query all achievements by the given user_id
    achievement_records = Achievement.query.filter_by(user_id=user_id).all()

    # Check if any records exist
    if not achievement_records:
        return jsonify({'error': f'No achievements found for the user with id: {user_id}'}), 404
    
    # Delete all records that were found
    for record in achievement_records:
        db.session.delete(record)

    db.session.commit()

    # Return 204 No Content
    return '', 204
