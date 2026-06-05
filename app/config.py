import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1").strip(),
    "user": os.getenv("DB_USER", "root").strip(),
    "password": os.getenv("DB_PASSWORD", "").strip(),
    "database": os.getenv("DB_NAME", "livraria").strip(),
}
