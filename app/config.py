from pydantic_settings import BaseSettings , SettingsConfigDict

class settings(BaseSettings):
    # For Database
    DATABASE_URL:str
    
    # For JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    
    # For Setting Model Confing
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'   
    )
    
setting = settings()