import requests
from bs4 import BeautifulSoup
from typing import Dict

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_quiz_content(self, url: str) -> Dict[str, str]:
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find quiz content - adjust selectors based on target websites
            question_text = ""
            
            # Common selectors for quiz questions
            possible_selectors = [
                '.question-text',
                '.quiz-question',
                '[data-testid="question"]',
                '.mcq-question'
            ]
            
            for selector in possible_selectors:
                element = soup.select_one(selector)
                if element:
                    question_text = element.text.strip()
                    break
            
            # If no specific selector worked, try to get all text
            if not question_text:
                question_text = soup.get_text()
            
            return {
                'question': question_text,
                'url': url,
                'html': response.text  # Save HTML for AI context
            }
            
        except Exception as e:
            raise Exception(f"Failed to scrape URL: {str(e)}")