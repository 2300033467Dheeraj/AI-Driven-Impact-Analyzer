"""Application configuration."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    model_path: str = "app/ml/model.joblib"
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"
    log_level: str = "INFO"

    @property
    def model_path_resolved(self) -> Path:
        """Resolve model path relative to project root."""
        path = Path(self.model_path)
        if not path.is_absolute():
            path = Path(__file__).resolve().parent.parent / path
        return path


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
