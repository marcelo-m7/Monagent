import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ENV: str = Field(default_factory=lambda: os.getenv("ENV", "dev"))
    SUPABASE_SCHEMA: str = Field(default_factory=lambda: os.getenv("SUPABASE_SCHEMA", "app"))
    SUPABASE_URL: str = Field(default_factory=lambda: os.getenv("SUPABASE_URL", ""))
    SUPABASE_ANON_KEY: str = Field(default_factory=lambda: os.getenv("SUPABASE_ANON_KEY", ""))
    SUPABASE_SERVICE_ROLE_KEY: str = Field(
        default_factory=lambda: os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    )

settings = Settings()
