import os
from dotenv import load_dotenv

load_dotenv()

from typing import Optional

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI") or ""
    SECRET_KEY: str = os.getenv("SECRET_KEY") or ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 0)

settings = Settings()
