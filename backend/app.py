# At the top, import NPCBot
from models import db, User, Bot, NPCBot

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
