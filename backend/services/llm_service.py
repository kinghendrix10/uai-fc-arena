# backend/services/llm_service.py

import openai
import requests
from config import Config

class LLMService:
    def __init__(self):
        self.openai_api_key = Config.OPENAI_API_KEY
        self.cerebras_api_key = Config.CEREBRAS_API_KEY
        self.groq_api_key = Config.GROQ_API_KEY

    def generate_action(self, provider, api_key, prompt):
        if provider == 'openai':
            return self._generate_action_openai(api_key or self.openai_api_key, prompt)
        elif provider == 'cerebras':
            return self._generate_action_cerebras(api_key or self.cerebras_api_key, prompt)
        elif provider == 'groq':
            return self._generate_action_groq(api_key or self.groq_api_key, prompt)
        else:
            raise ValueError("Unsupported LLM provider.")

    def _generate_action_openai(self, api_key, prompt):
        openai.api_key = api_key
        try:
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                max_tokens=50,
                temperature=0.7
            )
            action = response.choices[0].text.strip()
            return action
        except Exception as e:
            raise ValueError(f"OpenAI API error: {str(e)}")

    def _generate_action_cerebras(self, api_key, prompt):
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'prompt': prompt,
            'max_tokens': 50,
            'temperature': 0.7
        }
        try:
            response = requests.post('https://api.cerebras.net/v1/generate', headers=headers, json=data)
            response.raise_for_status()
            action = response.json().get('generated_text', '').strip()
            return action
        except Exception as e:
            raise ValueError(f"Cerebras API error: {str(e)}")

    def _generate_action_groq(self, api_key, prompt):
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'prompt': prompt,
            'max_tokens': 50,
            'temperature': 0.7
        }
        try:
            response = requests.post('https://api.groq.com/v1/generate', headers=headers, json=data)
            response.raise_for_status()
            action = response.json().get('generated_text', '').strip()
            return action
        except Exception as e:
            raise ValueError(f"Groq API error: {str(e)}")
