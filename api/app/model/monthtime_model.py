from app import db

class MonthTime(db.Model):
    __tablename__ = 'monthtime'

    user_id = db.Column(db.BigInteger, primary_key=True)
    mth = db.Column(db.SmallInteger, primary_key=True)
    yr = db.Column(db.SmallInteger, primary_key=True)
    stime = db.Column(db.Integer, nullable=False)