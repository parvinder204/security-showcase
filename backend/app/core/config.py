from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    session_secret: str = "dev-secret-key-change-in-production"
    allowed_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    class Config:
        env_file = ".env"


settings = Settings()