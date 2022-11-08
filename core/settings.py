import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

APP_NAME = os.getenv("APP_NAME")
# APP_URL = os.getenv("APP_URL")
APP_SECRET = os.getenv("APP_SECRET")
APP_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_VERSION = "0.1.0"

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")