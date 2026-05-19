from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432                  # ← era 3306 (MySQL), PostgreSQL usa 5432
    DB_USER: str = "postgres"            # ← usuario por defecto en PostgreSQL
    DB_PASSWORD: str = ""
    DB_NAME: str = "agrocontrol"

    # JWT
    SECRET_KEY: str = "clave-super-secreta-cambiar-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # CORS
    FRONTEND_URL: str = "http://localhost:5173"

    @property
    def DATABASE_URL(self) -> str:
        # ← era mysql+pymysql con ?charset=utf8mb4
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
