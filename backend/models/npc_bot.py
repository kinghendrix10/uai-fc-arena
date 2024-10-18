from . import db

class NPCBot(db.Model):
    __tablename__ = 'npc_bots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    stats = db.Column(db.PickleType, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    experience = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'stats': self.stats,
            'description': self.description,
            'wins': self.wins,
            'losses': self.losses,
            'experience': self.experience
        }
