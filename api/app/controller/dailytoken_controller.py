from flask import Blueprint, request, jsonify
from app.model.dailytoken_model import DailyToken
from app.schema.dailytoken_schema import DailyTokenSchema
from app import db

# Define dailytoken blueprint
dailytoken_bp = Blueprint('dailytoken_bp', __name__)

# Initialize DailyTokenSchema
dailytoken_schema = DailyTokenSchema()

@dailytoken_bp.route('/dailytoken/<int:user_id>', methods=['GET'])
def get_dailytoken_by_user_id(user_id):
    """
    Gets daily token entry for the provided user_id
    """

    # Query the DailyToken model to find an entry matching the user_id
    dailytoken = DailyToken.query.get(user_id)

    if dailytoken is None:
        # Return a 404 error if the dailytoken is not found
        return jsonify({'message': f'Daily token not found for user with id: {user_id}'}), 404
    
    # If found, serialize the dailytoken object to JSON format using the schema
    return jsonify(dailytoken_schema.dump(dailytoken))

@dailytoken_bp.route('/dailytoken', methods=['POST'])
def set_dailytoken_entry():
    """
    Sets the daily token entry given user_id and date_time in
    request body. This can be used as both a create and an update.
    """

    # Parse the request JSON body using the DailyTokenSchema
    data = request.get_json()

    # Validate the data
    errors = dailytoken_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Extract user_id and date_time from the parsed data
    user_id = data.get('user_id')
    date_time = data.get('date_time')

    # Check if a DailyToken entry already exists for the given user_id
    dailytoken = DailyToken.query.get(user_id)

    if dailytoken is None:
        # If no existing entry, create a new DailyToken
        new_dailytoken = DailyToken(user_id=user_id, date_time=date_time)
        db.session.add(new_dailytoken)
        db.session.commit()
        return jsonify(dailytoken_schema.dump(new_dailytoken)), 201  # Return the new entry with 201 status code
    else:
        # If an entry exists, update the date_time field
        dailytoken.date_time = date_time
        db.session.commit()
        return jsonify(dailytoken_schema.dump(dailytoken)), 200  # Return the updated entry with 200 status code

