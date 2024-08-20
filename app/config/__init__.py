import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MAIN_DB_NAME: str = os.getenv("MAIN_DB_NAME")
    MAIN_DB_USER: str = os.getenv("MAIN_DB_USER")
    MAIN_DB_PASSWORD: str = os.getenv("MAIN_DB_PASSWORD")
    MAIN_DB_HOST: str = os.getenv("MAIN_DB_HOST")
    MAIN_DB_PORT: str = os.getenv("MAIN_DB_PORT")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

settings = Settings()