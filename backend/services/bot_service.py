# backend/services/bot_service.py

from models import Bot, User, NPCBot
from sqlalchemy.exc import IntegrityError

class BotService:
    def __init__(self, db):
        self.db = db

    def create_bot(self, user_id, name, stats):
        if not self.validate_stats(stats):
            raise ValueError("Invalid stats. Each stat must be between 0 and 25, and total must not exceed 100.")
        new_bot = Bot(name=name, stats=stats, user_id=user_id)
        self.db.session.add(new_bot)
        try:
            self.db.session.commit()
        except IntegrityError:
            self.db.session.rollback()
            raise ValueError("Bot with this name already exists for this user.")
        return new_bot

    def get_user_bots(self, user_id):
        return Bot.query.filter_by(user_id=user_id).all()

    def get_bot_by_id(self, bot_id):
        return Bot.query.get(bot_id)

    def get_leaderboard(self, limit=10):
        return Bot.query.order_by(Bot.wins.desc(), Bot.experience.desc()).limit(limit).all()

    def validate_stats(self, stats):
        required_stats = {'Strength', 'Agility', 'Intelligence', 'Defense'}
        if set(stats.keys()) != required_stats:
            return False
        total_points = sum(stats.values())
        if total_points > 100:
            return False
        for stat_value in stats.values():
            if not (0 <= stat_value <= 25):
                return False
        return True

    def get_npc_bots(self):
        return NPCBot.query.all()

    def get_npc_bot_by_id(self, npc_bot_id):
        return NPCBot.query.get(npc_bot_id)

    def update_bot_stats(self, bot, win=False):
        bot.wins += 1 if win else 0
        bot.losses += 0 if win else 1
        bot.experience += 10
        self.db.session.commit()
