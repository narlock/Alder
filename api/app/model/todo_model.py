from app import db

class TodoModel(db.Model):
    __tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    item_name = db.Column(db.String(250), nullable=False)
    completed_date = db.Column(db.Date, nullable=True)