# backend/app.py
from flask import Flask, request, jsonify, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS
from config import Config
from services.bot_service import BotService
from services.battle_service import BattleService
from services.llm_service import LLMService
from utils.security import login_required
from utils.prompt_evaluator import evaluate_prompt_detailed
from models import db, User, Bot, NPCBot
import os

# Get the absolute path of the current file (app.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up one level to the project root, then to the frontend/templates directory
template_dir = os.path.join(os.path.dirname(current_dir), 'frontend', 'templates')

static_dir = os.path.join(os.path.dirname(current_dir), 'frontend')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config.from_object(Config)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SESSION_TYPE'] = 'filesystem'
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
Session(app)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Initialize services
bot_service = BotService(db)
llm_service = LLMService()
battle_service = BattleService(bot_service, llm_service)

# Ensure all routes are properly defined here

@app.route('/register', methods=['POST'])
def register():
    """Handle user registration."""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    api_key = data.get('api_key')
    llm_provider = data.get('llm_provider', 'openai')

    if not username or not password or not api_key or not llm_provider:
        return jsonify({'error': 'Missing required fields'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password, api_key=api_key, llm_provider=llm_provider)
    db.session.add(new_user)
    try:
        db.session.commit()
        session['user_id'] = new_user.id  # Set session after successful registration
        return jsonify({'message': 'User registered successfully', 'user_id': new_user.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    """Handle user logout."""
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/create_bot', methods=['POST'])
@login_required
def create_bot():
    try:
        data = request.json
        user_id = session['user_id']
        new_bot = bot_service.create_bot(user_id, data['name'], data['stats'])
        return jsonify({"message": "Bot created successfully", "bot": new_bot.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get_bots', methods=['GET'])
@login_required
def get_bots():
    user_id = session['user_id']
    bots = bot_service.get_user_bots(user_id)
    return jsonify([bot.to_dict() for bot in bots]), 200

@app.route('/get_leaderboard', methods=['GET'])
def get_leaderboard():
    leaderboard = bot_service.get_leaderboard()
    return jsonify([bot.to_dict() for bot in leaderboard]), 200

@app.route('/battle', methods=['POST'])
@login_required
def battle():
    try:
        data = request.json
        user_id = session['user_id']
        is_npc = data.get('is_npc', False)
        result = battle_service.conduct_battle(
            user_id,
            data['bot_id'],
            data['opponent_bot_id'],
            data['prompt'],
            is_npc=is_npc
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get_npc_bots', methods=['GET'])
def get_npc_bots():
    npc_bots = bot_service.get_npc_bots()
    return jsonify([bot.to_dict() for bot in npc_bots]), 200

@app.route('/evaluate_prompt', methods=['POST'])
@login_required
def evaluate_prompt_route():
    """Evaluate a prompt for a user's bot."""
    data = request.json
    prompt = data.get('prompt', '')
    user_id = session['user_id']
    user = User.query.get(user_id)
    bot = Bot.query.filter_by(user_id=user_id).first()
    if not bot:
        return jsonify({'error': 'No bots found for user'}), 400

    scores = evaluate_prompt_detailed(prompt, bot.stats)
    return jsonify(scores), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
