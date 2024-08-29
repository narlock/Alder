from marshmallow import Schema, fields

class DailyTokenSchema(Schema):
    user_id = fields.Int(required=True)
    date_time = fields.DateTime(required=False)