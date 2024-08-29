from app import db

class StreakModel(db.Model):
    __tablename__ = 'streak'

    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), primary_key=True)
    current_streak = db.Column(db.Integer, nullable=False, default=0)
    previous_connection_date = db.Column(db.Date, nullable=False)
    highest_streak_achieved = db.Column(db.Integer, nullable=False, default=0)