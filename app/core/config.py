import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")) 

settings = Settings()
