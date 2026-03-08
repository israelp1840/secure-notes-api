from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "dev"
    jwt_secret: str
    jwt_expire_minutes: int = 30
    fernet_key: str
    cors_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()