from flask import Blueprint, request, jsonify
from app.model.monthtime_model import MonthTime
from app.schema.monthtime_schema import MonthTimeSchema
from app import db
from sqlalchemy import desc
from datetime import datetime
from tools.utils import DateTimeUtils
from tools.log import Logger

# Define monthtime Blueprint for routes
monthtime_bp = Blueprint('monthtime_bp', __name__)

# Initialize MonthSchema
monthtime_schema = MonthTimeSchema()
monthtimes_schema = MonthTimeSchema(many=True)

# Endpoint to retrieve monthtime column by full primary key
@monthtime_bp.route('/monthtime', methods=['GET'])
def get_monthtime_by_primary_key():
    # Extract primary key fields from query parameters
    user_id = request.args.get('user_id', type=int)
    mth = request.args.get('mth', type=int)
    yr = request.args.get('yr', type=int)

    # Validate that all primary key components are provided
    if user_id is None or mth is None or yr is None:
        return jsonify({'error': 'Missing required query parameters'}), 400

    # Query the MonthTime record by its composite primary key
    monthtime_record = MonthTime.query.filter_by(user_id=user_id, mth=mth, yr=yr).first()

    # Check if the record exists
    if monthtime_record is None:
        return jsonify({'error': 'MonthTime record not found'}), 404

    # Serialize the record
    result = monthtime_schema.dump(monthtime_record)

    # Return the serialized record as JSON
    return jsonify(result), 200

# Endpoint to retrieve the current month's MonthTime entry for a given user_id
@monthtime_bp.route('/monthtime/<int:user_id>', methods=['GET'])
def get_monthtime_for_today(user_id):
    # Use the utility method to get the current UTC date
    mth, yr = DateTimeUtils.get_utc_month_year_now()
    
    monthtime_record = MonthTime.query.filter_by(user_id=user_id, mth=mth, yr=yr).first()

    if monthtime_record is None:
        return jsonify({'error': f'No MonthTime record found for {mth}/{yr} for user with id: {user_id}'}), 404

    result = monthtime_schema.dump(monthtime_record)
    return jsonify(result), 200

# Endpoint to create a new MonthTime entry for the current month
@monthtime_bp.route('/monthtime/<int:user_id>', methods=['POST'])
def create_monthtime(user_id):
    # Use the utility method to get the current UTC date
    mth, yr = DateTimeUtils.get_utc_month_year_now()

    existing_record = MonthTime.query.filter_by(user_id=user_id, mth=mth, yr=yr).first()
    if existing_record:
        return jsonify({'error': f'MonthTime record for today already exists on {mth}/{yr} for {user_id}'}), 400

    new_monthtime = MonthTime(
        user_id=user_id,
        mth=mth,
        yr=yr,
        stime=0  # Default stime to 0
    )

    db.session.add(new_monthtime)
    db.session.commit()

    result = monthtime_schema.dump(new_monthtime)
    return jsonify(result), 201

# Endpoint to create a new MonthTime entry for the current month
@monthtime_bp.route('/monthtime', methods=['POST'])
def create_monthtime_specific():

    if request.json.get('user_id') is None:
        return jsonify({'error': f'user_id needs to be required'}), 400
    
    user_id = request.json.get('user_id')

    if request.json.get('mth') is None:
        return jsonify({'error': f'mth needs to be required'}), 400
    
    if request.json.get('yr') is None:
        return jsonify({'error': f'yr needs to be required'}), 400

    mth = request.json.get('mth')
    yr = request.json.get('yr')

    existing_record = MonthTime.query.filter_by(user_id=user_id, mth=mth, yr=yr).first()
    if existing_record:
        return jsonify({'error': f'MonthTime record for today already exists on {mth}/{yr} for {user_id}'}), 400
    
    if request.json.get('stime') is None:
        stime = 0
    else:
        stime = request.json.get('stime')

    new_monthtime = MonthTime(
        user_id=user_id,
        mth=mth,
        yr=yr,
        stime=stime
    )

    db.session.add(new_monthtime)
    db.session.commit()

    result = monthtime_schema.dump(new_monthtime)
    return jsonify(result), 201

# Endpoint to update the stime for the current month
@monthtime_bp.route('/monthtime/<int:user_id>', methods=['PATCH'])
def update_monthtime_stime(user_id):
    # Use the utility method to get the current UTC date
    mth, yr = DateTimeUtils.get_utc_month_year_now()

    monthtime_record = MonthTime.query.filter_by(user_id=user_id, mth=mth, yr=yr).first()

    if monthtime_record is None:
        return jsonify({'error': f'No MonthTime record found for today: {mth}/{yr}'}), 404

    add_stime = request.json.get('stime')
    if add_stime is None:
        return jsonify({'error': 'Missing required field: stime'}), 400

    monthtime_record.stime += add_stime

    db.session.commit()

    result = monthtime_schema.dump(monthtime_record)
    return jsonify(result), 200

@monthtime_bp.route('/monthtime/search', methods=['POST'])
def search_monthtime():
    data = request.get_json()

    # Get the current date from DateTimeUtils or from the provided date
    date_str = data.get('date')
    if date_str:
        try:
            date = datetime.strptime(date_str.strip(), '%m-%Y')
            mth, yr = date.month, date.year
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use mm-yyyy.'}), 400
    else:
        mth, yr = DateTimeUtils.get_utc_month_year_now()

    # Build the base query
    query = MonthTime.query.filter_by(mth=mth, yr=yr)

    # Apply conditions if provided
    conditions = data.get('conditions', [])
    for condition in conditions:
        cond = condition.get('condition')
        value = condition.get('value')

        if not cond or value is None:
            return jsonify({'message': 'Each condition must have a condition, and value'}), 400

        # Build the query based on the condition
        column = MonthTime.stime
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
    query = query.order_by(desc(MonthTime.stime))

    # Apply the limit if provided
    limit = data.get('limit')
    if limit is not None:
        try:
            limit = int(limit)
            query = query.limit(limit)
        except ValueError:
            return jsonify({'message': 'Invalid limit value. Must be an integer.'}), 400

    monthtime_entries = query.all()
    return jsonify(monthtimes_schema.dump(monthtime_entries)), 200

# Endpoint to delete all MonthTime entries for a specific user_id
@monthtime_bp.route('/monthtime/<int:user_id>', methods=['DELETE'])
def delete_monthtime_by_user_id(user_id):
    # Query all MonthTime records for the given user_id
    monthtime_records = MonthTime.query.filter_by(user_id=user_id).all()

    # Check if any records exist
    if not monthtime_records:
        return jsonify({'error': f'No MonthTime records found for user with id: {user_id}'}), 404

    # Delete all found records
    for record in monthtime_records:
        db.session.delete(record)

    db.session.commit()

    # Return 204 No Content
    return '', 204