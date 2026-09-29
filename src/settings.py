from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    app_name:str="DU-cluster"
    api_key:str=""
    ai_provider:str=""
    ai_model:str=""
    ai_api_key:str=""
    ai_base_url:str=""
    database_url:str="sqlite:///data/ducluster.db"
    redis_url:str=""
settings=Settings()
