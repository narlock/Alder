from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(required=True)
    tokens = fields.Int(required=True)
    stime = fields.Int(required=True)
    timezone = fields.Str(required=False)
    hex = fields.Str(required=False)
    trivia = fields.Int(required=False)
