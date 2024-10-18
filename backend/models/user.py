# backend/models/user.py
from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    api_key = db.Column(db.String(100), nullable=False)
    llm_provider = db.Column(db.String(20), nullable=False, default='openai')

    bots = db.relationship('Bot', backref='owner', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username
            # Do not include password or api_key for security reasons
        }
