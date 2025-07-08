# config/secrets.py
import os
from dotenv import load_dotenv

load_dotenv()

class Secrets:
    LLM_API_URL = os.getenv("LLM_API_URL")
    LLM_API_KEY = os.getenv("LLM_API_KEY")
