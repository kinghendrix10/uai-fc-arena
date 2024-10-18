# backend/models/user.py

from . import db
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    api_key = db.Column(db.String(100), nullable=False)
    llm_provider = db.Column(db.String(20), nullable=False, default='openai')

    bots = db.relationship('Bot', back_populates='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'llm_provider': self.llm_provider
            # Do not include password_hash or api_key for security reasons
        }
