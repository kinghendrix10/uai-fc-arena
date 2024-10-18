# backend/config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'  # Replace with a secure key in production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    CORS_HEADERS = 'Content-Type'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    CEREBRAS_API_KEY = os.environ.get('CEREBRAS_API_KEY')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
