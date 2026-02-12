import os
from dotenv import load_dotenv

load_dotenv()

GROK_API_KEY = os.getenv("GROK_API_KEY")
BACKEND_URL = os.getenv("FLASK_BACKEND_URL")
