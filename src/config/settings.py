from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    APP_NAME: str
    APP_VERSION: str
    ALLOWED_FILE_TYPES: list
    MAX_FILE_SIZE: int
    TESSERACT_CMD: str
    ARA_MODEL: str
    ENG_MODEL: str

    class Config:
        env_file = ".env"


settings = Settings()

def get_settings():
    return Settings()
