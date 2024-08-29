from flask import Blueprint, request, jsonify
from app.model.streak_model import StreakModel
from app.schema.streak_schema import StreakSchema
from app import db
from datetime import datetime, timezone, timedelta

# Define the streak Blueprint
streak_bp = Blueprint('streak_bp', __name__)

# Initialize StreakSchema
streak_schema = StreakSchema()
streaks_schema = StreakSchema(many=True)

@streak_bp.route('/streak/<int:user_id>', methods=['POST'])
def set_user_streak(user_id):
    """
    A user streak will be created if one did not exist before. The
    current_streak and highest_streak fields will be set to their defaults.
    The previous_connection_date will be set to the current date.

    If a user streak already exists, this operation will obtain the current
    date with respect to UTC timezone. Then, will modify the streak under
    these conditions:
    - If the current date is equal to the user streak's previous_connection_date,
    we will skip and do nothing.
    - If the user streak's previous_connection_date is the previous day when comparing
    against the current date, we will increment the value of the user streak's current
    streak. We will also compare if the newly incremented current_streak is greater than
    the user streak's highest_streak value. If it is, we will set the current_streak value
    to the highest_streak value.
    - If the user streak's previous_connection_date is more than two days past the
    current date, we will set the current_streak value to 0.
    """
    # Fetch the current UTC date
    current_date = datetime.now(timezone.utc).date()

    # Query the StreakModel to find the streak by user_id
    streak = StreakModel.query.get(user_id)

    if streak is None:
        # If no streak exists, create a new one with default values
        new_streak = StreakModel(
            user_id=user_id,
            current_streak=0,
            previous_connection_date=current_date,
            highest_streak_achieved=0
        )
        db.session.add(new_streak)
        db.session.commit()
        return jsonify(streak_schema.dump(new_streak)), 201

    # If streak exists, check the conditions for updating the streak
    last_login_date = streak.previous_connection_date

    if last_login_date == current_date:
        # Do nothing if the current date is the same as the last login date
        return jsonify({'message': f'Streak already updated for today for {user_id}'}), 200

    elif last_login_date == current_date - timedelta(days=1):
        # Increment current streak if the last login date was yesterday
        streak.current_streak += 1

        # Update highest streak if the current streak exceeds it
        if streak.current_streak > streak.highest_streak_achieved:
            streak.highest_streak_achieved = streak.current_streak

    else:
        # Reset the current streak to 0 if more than one day has passed
        streak.current_streak = 0

    # Update the previous login date to the current date
    streak.previous_connection_date = current_date
    db.session.commit()

    return jsonify(streak_schema.dump(streak)), 200

@streak_bp.route('/streak/<int:user_id>', methods=['GET'])
def get_user_streak(user_id):
    """
    Retrieves the streak given the user_id
    """

    # Query the StreakModel to find the streak by user_id
    streak = StreakModel.query.get(user_id)

    if streak is None:
        # Return a 404 error if the streak is not found
        return jsonify({'message': 'Streak not found'}), 404

    # Serialize the streak object to JSON format using the StreakSchema
    return jsonify(streak_schema.dump(streak))

@streak_bp.route('/streak/search', methods=['POST'])
def search_streaks():
    """
    Searches for streaks given a `search_field` inside of the
    request body. This `search_field` can either be the
    `highest_streak_achieved` field or the `current_streak` field.
    
    Optionally, a `limit` field can be provided to restrict the
    number of results returned.
    """
    # Get the request JSON data
    data = request.get_json()

    # Validate that search_field is provided
    search_field = data.get('search_field')
    limit = data.get('limit', 10)  # Optional limit field, defaults to None

    if not search_field:
        return jsonify({'message': 'Missing search_field'}), 400

    # Ensure the search_field is either 'highest_streak_achieved' or 'current_streak'
    if search_field not in ['highest_streak_achieved', 'current_streak']:
        return jsonify({'message': 'Invalid search_field. Must be either "highest_streak_achieved" or "current_streak"'}), 400

    try:
        # Build the query based on the search_field
        query = StreakModel.query.order_by(getattr(StreakModel, search_field).desc())
        
        if limit is not None:
            # Apply the limit to the query if provided
            query = query.limit(limit)
        
        streaks = query.all()
        
    except Exception as e:
        return jsonify({'message': 'Error occurred during streak search.'}), 500

    if not streaks:
        return jsonify({'message': 'No streaks found matching the criteria.'}), 404

    # Serialize the results
    return jsonify(streaks_schema.dump(streaks)), 200

