import os
import requests
from dotenv import load_dotenv
import re

class Summarizer:
    def __init__(self):
        load_dotenv()
        self.api_token = os.getenv("HF_TOKEN")
        self.api_url = "https://api-inference.huggingface.co/models/philschmid/bart-large-cnn-samsum"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}"
        }

    def summarize(self, text):
        try:
            cleaned = self._sanitize_input(text)

            if not cleaned or len(cleaned) < 20:
                return "⚠️ Not enough content to summarize."

            if len(cleaned) > 2000:
                cleaned = cleaned[:2000]

            payload = {"inputs": cleaned}
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()

            summary = response.json()
            if isinstance(summary, list) and 'summary_text' in summary[0]:
                return summary[0]['summary_text']
            else:
                return "⚠️ HF: Unexpected response format."

        except Exception as e:
            # Fallback if HF fails
            return f"🪶 Fallback summary: {cleaned[:150]}..."

    def _sanitize_input(self, text):
        # Remove non-printable/control characters
        text = re.sub(r'[\x00-\x1F\x7F]', '', text)
        # Normalize whitespace
        return ' '.join(text.strip().split())
