from marshmallow import Schema, fields

class TriviaQuestionSchema(Schema):
    id = fields.Int(dump_only=True) # Should not be provided in request bodies
    title = fields.Str(required=True)
    option_a = fields.Str(required=True)
    option_b = fields.Str(required=True)
    option_c = fields.Str(required=True)
    option_d = fields.Str(required=True)
    correct = fields.Int(required=True)
    author = fields.Str(required=True)
    category = fields.Str(required=True)