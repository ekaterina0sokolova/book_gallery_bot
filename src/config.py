import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()

if dotenv_path:
    load_dotenv(dotenv_path)
else:
    print("no .env file found. using to environment variables")

BOT_TOKEN = os.getenv("BOT_TOKEN")