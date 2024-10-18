# backend/models/bot.py

from . import db

class Bot(db.Model):
    __tablename__ = 'bots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    stats = db.Column(db.JSON, nullable=False)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    experience = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='bots')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'stats': self.stats,
            'wins': self.wins,
            'losses': self.losses,
            'experience': self.experience,
            'user_id': self.user_id,
            'owner_username': self.user.username
        }
