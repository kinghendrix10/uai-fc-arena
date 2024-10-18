# backend/models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .bot import Bot
from .npc_bot import NPCBot
