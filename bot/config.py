import os

from dotenv import load_dotenv

load_dotenv()


DB_URL: str = os.getenv('DB_URL')
TG_TOKEN: str = os.getenv('TG_TOKEN')