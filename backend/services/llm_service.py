import openai
import requests

class LLMService:
    def __init__(self):
        pass

    def generate_action(self, provider, api_key, prompt):
        if provider == 'openai':
            return self._generate_action_openai(api_key, prompt)
        elif provider == 'cerebras':
            return self._generate_action_cerebras(api_key, prompt)
        elif provider == 'groq':
            return self._generate_action_groq(api_key, prompt)
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
        # Pseudo-code: Replace with actual Cerebras API integration
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
            response = requests.post('https://api.cerebras.net/generate', headers=headers, json=data)
            response.raise_for_status()
            action = response.json().get('generated_text', '').strip()
            return action
        except Exception as e:
            raise ValueError(f"Cerebras API error: {str(e)}")

    def _generate_action_groq(self, api_key, prompt):
        # Pseudo-code: Replace with actual Groq API integration
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
            response = requests.post('https://api.groq.com/generate', headers=headers, json=data)
            response.raise_for_status()
            action = response.json().get('generated_text', '').strip()
            return action
        except Exception as e:
            raise ValueError(f"Groq API error: {str(e)}")
