# backend/services/battle_service.py

from models import Bot, User, NPCBot
from utils.prompt_evaluator import evaluate_prompt
import random

class BattleService:
    def __init__(self, bot_service, llm_service):
        self.bot_service = bot_service
        self.llm_service = llm_service

    def conduct_battle(self, user_id, bot_id, opponent_bot_id, prompt, is_npc=False):
        bot = self.bot_service.get_bot_by_id(bot_id)
        if is_npc:
            opponent_bot = self.bot_service.get_npc_bot_by_id(opponent_bot_id)
            opponent_user = None
            opponent_api_key = None
            opponent_provider = 'default'
        else:
            opponent_bot = self.bot_service.get_bot_by_id(opponent_bot_id)
            opponent_user = User.query.get(opponent_bot.user_id)
            opponent_api_key = opponent_user.api_key
            opponent_provider = opponent_user.llm_provider

        if not bot or not opponent_bot:
            raise ValueError("One or both bots not found.")

        if bot.user_id != user_id:
            raise ValueError("You do not own this bot.")

        user = User.query.get(user_id)
        user_api_key = user.api_key
        user_provider = user.llm_provider

        user_action = self.llm_service.generate_action(user_provider, user_api_key, prompt)
        opponent_prompt = self.generate_opponent_prompt(opponent_bot)
        opponent_action = self.llm_service.generate_action(opponent_provider, opponent_api_key, opponent_prompt)

        user_score = evaluate_prompt(prompt, bot.stats)
        opponent_score = evaluate_prompt(opponent_prompt, opponent_bot.stats)

        outcome = self.calculate_outcome(bot, opponent_bot, user_score, opponent_score)

        self.bot_service.update_bot_stats(bot, win=(outcome['winner'] == bot.name))
        if not is_npc:
            self.bot_service.update_bot_stats(opponent_bot, win=(outcome['winner'] == opponent_bot.name))

        result = {
            'winner': outcome['winner'],
            'user_action': user_action,
            'opponent_action': opponent_action,
            'details': outcome['details']
        }

        return result

    def generate_opponent_prompt(self, opponent_bot):
        # Generate a prompt for the opponent based on its stats
        strategies = {
            'Strength': 'Use your immense strength to overpower the opponent.',
            'Agility': 'Dodge the attacks swiftly and strike back.',
            'Intelligence': 'Analyze the opponent’s weaknesses and exploit them.',
            'Defense': 'Brace yourself and block incoming attacks effectively.'
        }
        highest_stat = max(opponent_bot.stats, key=opponent_bot.stats.get)
        prompt = strategies.get(highest_stat, 'Engage the opponent with your best abilities.')
        return prompt

    def calculate_outcome(self, bot, opponent_bot, user_score, opponent_score):
        # Adjust scores based on bot stats
        user_total_score = user_score + sum(bot.stats.values()) / 100
        opponent_total_score = opponent_score + sum(opponent_bot.stats.values()) / 100

        if user_total_score > opponent_total_score:
            winner = bot.name
        elif opponent_total_score > user_total_score:
            winner = opponent_bot.name
        else:
            winner = random.choice([bot.name, opponent_bot.name])

        details = {
            'user_total_score': round(user_total_score, 2),
            'opponent_total_score': round(opponent_total_score, 2),
            'user_prompt_score': round(user_score, 2),
            'opponent_prompt_score': round(opponent_score, 2)
        }

        return {'winner': winner, 'details': details}
