from flask import Blueprint, request, jsonify
from app.model.dailytime_model import DailyTime
from app.schema.dailytime_schema import DailyTimeSchema
from app import db
from sqlalchemy import desc
from datetime import datetime
from tools.utils import DateTimeUtils

# Define dailytime Blueprint for routes
dailytime_bp = Blueprint('dailytime_bp', __name__)

# Initialize UserSchema
dailytime_schema = DailyTimeSchema()
dailytimes_schema = DailyTimeSchema(many=True)

# Endpoint to retrieve dailytime column by full primary key
@dailytime_bp.route('/dailytime', methods=['GET'])
def get_dailytime_by_primary_key():
    # Extract primary key fields from query parameters
    user_id = request.args.get('user_id', type=int)
    d = request.args.get('d', type=int)
    mth = request.args.get('mth', type=int)
    yr = request.args.get('yr', type=int)

    # Validate that all primary key components are provided
    if user_id is None or d is None or mth is None or yr is None:
        return jsonify({'error': 'Missing required query parameters'}), 400

    # Query the DailyTime record by its composite primary key
    dailytime_record = DailyTime.query.filter_by(user_id=user_id, d=d, mth=mth, yr=yr).first()

    # Check if the record exists
    if dailytime_record is None:
        return jsonify({'error': 'DailyTime record not found'}), 404

    # Serialize the record
    result = dailytime_schema.dump(dailytime_record)

    # Return the serialized record as JSON
    return jsonify(result), 200

# Endpoint to retrieve today's DailyTime entry for a given user_id
@dailytime_bp.route('/dailytime/<int:user_id>', methods=['GET'])
def get_dailytime_for_today(user_id):
    # Use the utility method to get the current UTC date
    mth, d, yr, string = DateTimeUtils.get_utc_date_now()
    
    dailytime_record = DailyTime.query.filter_by(user_id=user_id, d=d, mth=mth, yr=yr).first()

    if dailytime_record is None:
        return jsonify({'error': f'No DailyTime record found for {string}'}), 404

    result = dailytime_schema.dump(dailytime_record)
    return jsonify(result), 200

# Endpoint to create a new DailyTime entry for the current day
@dailytime_bp.route('/dailytime/<int:user_id>', methods=['POST'])
def create_dailytime(user_id):
    # Use the utility method to get the current UTC date
    mth, d, yr, string = DateTimeUtils.get_utc_date_now()

    existing_record = DailyTime.query.filter_by(user_id=user_id, d=d, mth=mth, yr=yr).first()
    if existing_record:
        return jsonify({'error': f'DailyTime record for today already exists on {string} for {user_id}'}), 400

    new_dailytime = DailyTime(
        user_id=user_id,
        d=d,
        mth=mth,
        yr=yr,
        stime=0  # Default stime to 0
    )

    db.session.add(new_dailytime)
    db.session.commit()

    result = dailytime_schema.dump(new_dailytime)
    return jsonify(result), 201

# Endpoint to update the stime for the current day
@dailytime_bp.route('/dailytime/<int:user_id>', methods=['PATCH'])
def update_dailytime_stime(user_id):
    # Use the utility method to get the current UTC date
    mth, d, yr, string = DateTimeUtils.get_utc_date_now()

    dailytime_record = DailyTime.query.filter_by(user_id=user_id, d=d, mth=mth, yr=yr).first()

    if dailytime_record is None:
        return jsonify({'error': f'No DailyTime record found for today: {string}'}), 404

    add_stime = request.json.get('stime')
    if add_stime is None:
        return jsonify({'error': 'Missing required field: stime'}), 400

    dailytime_record.stime += add_stime

    db.session.commit()

    result = dailytime_schema.dump(dailytime_record)
    return jsonify(result), 200

# Endpoint to search for DailyTime
@dailytime_bp.route('/dailytime/search', methods=['POST'])
def search_dailytime():
    data = request.get_json()

    # Get the current date from DateTimeUtils or from the provided date
    date_str = data.get('date')
    if date_str:
        try:
            date = datetime.strptime(date_str, '%m-%d-%Y')
            mth, d, yr = date.month, date.day, date.year
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use mm-dd-yyyy.'}), 400
    else:
        mth, d, yr, string = DateTimeUtils.get_utc_date_now()

    # Build the base query
    query = DailyTime.query.filter_by(d=d, mth=mth, yr=yr)

    # Apply conditions if provided
    conditions = data.get('conditions', [])
    for condition in conditions:
        cond = condition.get('condition')
        value = condition.get('value')

        if not cond or value is None:
            return jsonify({'message': 'Each condition must have a condition, and value'}), 400

        # Build the query based on the condition
        column = DailyTime.stime
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

    # Always sort by stime in descending order
    query = query.order_by(desc(DailyTime.stime))

    # Apply the limit if provided
    limit = data.get('limit')
    if limit is not None:
        try:
            limit = int(limit)
            query = query.limit(limit)
        except ValueError:
            return jsonify({'message': 'Invalid limit value. Must be an integer.'}), 400

    dailytime_entries = query.all()
    return jsonify(dailytimes_schema.dump(dailytime_entries)), 200

# Endpoint to delete all DailyTime entries for a specific user_id
@dailytime_bp.route('/dailytime/<int:user_id>', methods=['DELETE'])
def delete_dailytime_by_user_id(user_id):
    # Query all DailyTime records for the given user_id
    dailytime_records = DailyTime.query.filter_by(user_id=user_id).all()

    # Check if any records exist
    if not dailytime_records:
        return jsonify({'error': f'No DailyTime records found for user with id: {user_id}'}), 404

    # Delete all found records
    for record in dailytime_records:
        db.session.delete(record)

    db.session.commit()

    # Return 204 No Content
    return '', 204