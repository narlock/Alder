from app import db

class DailyTime(db.Model):
    __tablename__ = 'dailytime'

    user_id = db.Column(db.BigInteger, primary_key=True)
    d = db.Column(db.SmallInteger, primary_key=True)
    mth = db.Column(db.SmallInteger, primary_key=True)
    yr = db.Column(db.SmallInteger, primary_key=True)
    stime = db.Column(db.Integer, nullable=False)