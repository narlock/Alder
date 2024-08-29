from marshmallow import Schema, fields

class TodoSchema(Schema):
    id = fields.Int(required=False)
    user_id = fields.Int(required=False)
    item_name = fields.Str(required=False)
    completed_date = fields.Date(required=False)