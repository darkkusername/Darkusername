from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = 'development'
    app_name: str = 'AI Venture Factory'
    database_path: str = 'data/venture_factory.json'
    approval_mode: str = 'human_for_sensitive'
    max_experiment_eur: float = 100.0
    max_daily_spend_eur: float = 250.0
    llm_provider: str = 'stub'
    llm_api_key: str | None = None
    llm_model: str | None = None
    make_webhook_url: str | None = None
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
