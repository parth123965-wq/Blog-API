from pydantic_settings import BaseSettings , SettingsConfigDict
from pydantic import field_validator

class settings(BaseSettings):
    # For Database
    DATABASE_URL:str
    
    # For JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def fix_postgres_suffix(cls, value: str) -> str:
        if value and value.startswith("postgres://"):
            value = value.replace("postgres://", "postgresql+asyncpg://", 1)
        elif value and value.startswith("postgresql://"):
            value = value.replace("postgresql://", "postgresql+asyncpg://", 1)
        return value
    # For Setting Model Confing
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'   
    )
    
setting = settings()