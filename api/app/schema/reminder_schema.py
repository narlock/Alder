from marshmallow import Schema, fields, validate, ValidationError
import re

# Custom validator for combinations of mtwhfsu
def validate_repeat_interval(value):
    # Allow standard intervals
    standard_intervals = ['daily', 'weekly', 'monthly', 'yearly']
    if value in standard_intervals:
        return True
    
    # Regex pattern to match any combination of mtwhfsu
    if re.fullmatch(r'[mtwhfsu]+', value):
        return True
    
    raise ValidationError(f"Invalid repeat_interval: {value}. Must be a valid combination of 'mtwhfsu' or a standard interval (daily, weekly, monthly, yearly).")

class ReminderSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    title = fields.Str(required=True, validate=validate.Length(max=255))
    description = fields.Str()
    remind_at = fields.DateTime(required=True, format="%Y-%m-%dT%H:%M:%S")
    repeat_interval = fields.Str(validate=validate_repeat_interval)  # Custom validator here
    repeat_until = fields.DateTime(format="%Y-%m-%dT%H:%M:%S")
    repeat_count = fields.Int(validate=validate.Range(min=0))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
