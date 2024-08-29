from marshmallow import Schema, fields

class AchievementSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)