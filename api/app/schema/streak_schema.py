from marshmallow import Schema, fields

class StreakSchema(Schema):
    user_id = fields.Int(required=True)
    current_streak = fields.Int(required=True, default=0)
    previous_connection_date = fields.Date(required=True)
    highest_streak_achieved = fields.Int(required=True, default=0)
