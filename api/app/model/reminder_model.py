from app import db
from datetime import datetime

class ReminderModel(db.Model):
    __tablename__ = 'reminder'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    remind_at = db.Column(db.DateTime, nullable=False)
    repeat_interval = db.Column(db.String(50), nullable=True)
    repeat_until = db.Column(db.DateTime, nullable=True)  # NULL means no end
    repeat_count = db.Column(db.Integer, nullable=True)  # NULL means indefinite
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
