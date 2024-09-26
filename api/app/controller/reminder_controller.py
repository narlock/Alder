from flask import Blueprint, request, jsonify
from app.model.reminder_model import ReminderModel
from app.schema.reminder_schema import ReminderSchema
from app import db

# Define Reminder Blueprint
reminder_bp = Blueprint('reminder_bp', __name__)

# Initialize Reminder Schema
reminder_schema = ReminderSchema()
reminders_schema = ReminderSchema(many=True)

# Endpoint to create a new reminder
@reminder_bp.route('/reminder', methods=['POST'])
def create_reminder():
    """
    Creates a reminder based on the contents of
    the request body for the user.
    """
    data = request.get_json()

    # Validate incoming request data
    errors = reminder_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Create a new reminder instance
    new_reminder = ReminderModel(
        user_id=data['user_id'],
        title=data['title'],
        description=data.get('description'),
        remind_at=data['remind_at'],
        repeat_interval=data.get('repeat_interval'),
        repeat_until=data.get('repeat_until'),
        repeat_count=data.get('repeat_count')
    )

    # Add and commit the reminder to the database
    db.session.add(new_reminder)
    db.session.commit()

    # Return the newly created reminder
    return jsonify(reminder_schema.dump(new_reminder)), 201


# Endpoint to retrieve all reminders for a specific user
@reminder_bp.route('/reminder/user/<int:user_id>', methods=['GET'])
def get_user_reminders(user_id):
    """
    Retrieves all reminders for the user by user_id.
    """
    # Query the database for reminders by user_id
    reminders = ReminderModel.query.filter_by(user_id=user_id).all()

    if not reminders:
        return jsonify({"message": "No reminders found for this user."}), 404

    # Serialize the list of reminders and return
    return jsonify(reminders_schema.dump(reminders)), 200


# Endpoint to retrieve all reminders
@reminder_bp.route('/reminder', methods=['GET'])
def get_all_reminders():
    """
    Returns all reminders stored in the database.
    """
    # Query the database for all reminders
    reminders = ReminderModel.query.all()

    # Serialize the list of reminders and return
    return jsonify(reminders_schema.dump(reminders)), 200


# Endpoint to retrieve a reminder by its ID
@reminder_bp.route('/reminder/<int:id>', methods=['GET'])
def get_reminder(id):
    """
    Retrieves a reminder by its ID.
    """
    # Query the database for a reminder by its ID
    reminder = ReminderModel.query.get(id)

    if reminder is None:
        return jsonify({"message": "Reminder not found."}), 404

    # Serialize and return the reminder
    return jsonify(reminder_schema.dump(reminder)), 200


# Endpoint to delete a reminder by its ID
@reminder_bp.route('/reminder/<int:id>', methods=['DELETE'])
def delete_reminder(id):
    """
    Delete a reminder by its ID.
    """
    # Query the database for a reminder by its ID
    reminder = ReminderModel.query.get(id)

    if reminder is None:
        return jsonify({"message": "Reminder not found."}), 404

    # Delete the reminder and commit the changes
    db.session.delete(reminder)
    db.session.commit()

    # Return 204 No Content status
    return '', 204