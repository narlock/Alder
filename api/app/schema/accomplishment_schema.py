from marshmallow import Schema, fields

class AccomplishmentSchema(Schema):
    user_id = fields.Int(required=True)
    msg = fields.Str(required=True)