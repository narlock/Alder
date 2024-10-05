from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=False)
    tokens = db.Column(db.Integer, nullable=False)
    stime = db.Column(db.BigInteger, nullable=False)
    timezone = db.Column(db.String(100), nullable=False, default='UTC')
    hex = db.Column(db.String(7), nullable=True)
    trivia = db.Column(db.Integer, nullable=True)
