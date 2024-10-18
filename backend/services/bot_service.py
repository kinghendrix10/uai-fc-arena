# backend/services/bot_service.py

from models import Bot, User, NPCBot

class BotService:
    def __init__(self, db):
        self.db = db

    # Existing methods...

    def get_npc_bots(self):
        return NPCBot.query.all()

    def get_npc_bot_by_id(self, npc_bot_id):
        return NPCBot.query.get(npc_bot_id)
