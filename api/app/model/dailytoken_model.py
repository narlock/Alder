from app import db

class DailyToken(db.Model):
    __tablename__ = 'dailytoken'

    user_id = db.Column(db.BigInteger, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False)