from app import db

class RogueBossUserModel(db.Model):
    __tablename__ = 'rbuser'

    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    rbtype = db.Column(db.String(15), nullable=False)
    xp = db.Column(db.BigInteger, nullable=False)
    model = db.Column(db.Integer, nullable=False)
    purchased_models = db.Column(db.String(200), nullable=True)