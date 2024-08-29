from marshmallow import Schema, fields

class MonthTimeSchema(Schema):
    user_id = fields.Int(required=True)
    mth = fields.Int(required=True)
    yr = fields.Int(required=True)
    stime = fields.Int(required=True)