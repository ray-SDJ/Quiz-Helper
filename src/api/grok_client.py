import requests
from typing import Dict, Any

class GrokClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.x.ai/v1/chat/completions"

    def analyze_question(self, content: str) -> dict:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        data = {
            'messages': [
                {
                    'role': 'system',
                    'content': '''You are a quiz assistant. Analyze web content to:
                    1. Identify quiz questions
                    2. Provide accurate answers
                    3. Give brief explanations
                    Use available context to ensure accuracy.'''
                },
                {
                    'role': 'user',
                    'content': content
                }
            ],
            'model': 'grok-3-latest',
            'stream': False,
            'temperature': 0.7
        }
        
        response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        return response.json()