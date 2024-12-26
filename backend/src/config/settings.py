from pydantic_settings import BaseSettings
from dotenv import find_dotenv

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = find_dotenv(".env")
        env_file_encoding = "utf-8"

settings = Settings()