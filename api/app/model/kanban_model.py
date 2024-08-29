from app import db

class KanbanModel(db.Model):
    __tablename__ = 'kanban'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    item_name = db.Column(db.String(250), nullable=False)
    column_name = db.Column(db.String(50), nullable=False)
    priority_number = db.Column(db.Integer, nullable=True)
    tag_name = db.Column(db.String(50), nullable=True)
    velocity = db.Column(db.Integer, nullable=True)