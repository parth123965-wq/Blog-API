from pydantic_settings import BaseSettings , SettingsConfigDict

class settings(BaseSettings):
    # For Database
    DATABASE_URL:str
    
    # For Setting Model Confing
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'   
    )
    
setting = settings()