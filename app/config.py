from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # Matches whatever variable name you used in .env
    DATAGOV_API_KEY: str = ""
    MANDI_RESOURCE_ID: str = "9ef84268-d588-465a-a308-a864a43d0070"
    CACHE_TTL_SECONDS: int = 3600  # 1 hour cache
    MIN_REFRESH_INTERVAL_SECONDS: int = 30  # Anti-DoS refresh cooldown
    APP_ENV: str = "development"
    ENABLE_DOCS: bool = True
    ALLOWED_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()