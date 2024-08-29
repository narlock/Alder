from app import db

class Accomplishment(db.Model):
    __tablename__ = 'accomplishment'

    user_id = db.Column(db.BigInteger, primary_key=True)
    msg = db.Column(db.String(200), primary_key=True)