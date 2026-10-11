from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Unified Inbox Agent"
    database_url: str = "sqlite:///./inbox_agent.db"
    telegram_bot_token: str = ""
    demo_mode: bool = True
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

settings = Settings()
