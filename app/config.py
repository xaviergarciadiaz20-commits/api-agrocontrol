from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Render inyectará esta variable automáticamente
    DATABASE_URL: str 
    
    # JWT
    SECRET_KEY: str = "clave-super-secreta-cambiar-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # CORS
    FRONTEND_URL: str = "*" # Cambiar por tu URL de frontend en producción

    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    # SQLAlchemy requiere "postgresql://" pero a veces Render u otros servicios envían "postgres://"
    if settings.DATABASE_URL and settings.DATABASE_URL.startswith("postgres://"):
        settings.DATABASE_URL = settings.DATABASE_URL.replace("postgres://", "postgresql://", 1)
    return settings
