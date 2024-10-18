# At the top, import NPCBot
from models import db, User, Bot, NPCBot

# ... existing code ...

@app.route('/get_npc_bots', methods=['GET'])
def get_npc_bots():
    npc_bots = bot_service.get_npc_bots()
    return jsonify([bot.to_dict() for bot in npc_bots]), 200
