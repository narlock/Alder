from marshmallow import Schema, fields

class RogueBossUserSchema(Schema):
    user_id = fields.Int(required=True)
    rbtype = fields.Str(required=True)
    xp = fields.Int(required=False)
    model = fields.Int(required=False)
    purchased_models = fields.Str(required=False)
