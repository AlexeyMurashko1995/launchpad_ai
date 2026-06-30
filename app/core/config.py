import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')