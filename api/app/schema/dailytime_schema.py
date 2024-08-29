from marshmallow import Schema, fields

class DailyTimeSchema(Schema):
    user_id = fields.Int(required=True)
    d = fields.Int(required=True)
    mth = fields.Int(required=True)
    yr = fields.Int(required=True)
    stime = fields.Int(required=True)