# src/config/settings.py
from pydantic import PostgresDsn, SecretStr, EmailStr
from pydantic_settings import BaseSettings
from typing import Optional, Any

class Settings(BaseSettings):
    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str
    DATABASE_URL: Optional[PostgresDsn] = None

    @property
    def sync_database_url(self) -> str:
        """Construct database URL from components."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # JWT settings
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Application settings
    APP_NAME: str = "SantaiRumah"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Email settings
    RESEND_API_KEY: str
    FROM_EMAIL: EmailStr = "jokodok678@gmail.com"
    
    # Scheduler settings
    ENABLE_SCHEDULER: bool = True
    SCHEDULER_API_ENABLED: bool = True
    SCHEDULER_TIMEZONE: str = "Asia/Jakarta"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == "DATABASE_URL":
                if raw_val.startswith("postgresql://"):
                    return raw_val
                return None
            return cls.json_loads(raw_val)

# Create settings instance
settings = Settings()