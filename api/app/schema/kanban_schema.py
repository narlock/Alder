from marshmallow import Schema, fields

class KanbanSchema(Schema):
    id = fields.Int(required=False)
    user_id = fields.Int(required=True)
    item_name = fields.Str(required=True)
    column_name = fields.Str(required=False)
    priority_number = fields.Int(required=False)
    tag_name = fields.Str(required=False)
    velocity = fields.Str(required=False)