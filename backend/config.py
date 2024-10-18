# backend/config.py

import os

class Config:
    SECRET_KEY = 'your-secret-key'  # Replace with a secure key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    CORS_HEADERS = 'Content-Type'
