import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

APP_NAME = os.getenv("APP_NAME")
APP_URL = os.getenv("APP_URL")
APP_SECRET = os.getenv("APP_SECRET")
APP_ALGORITHM = "HS256"
APP_VERSION = "0.1.0"