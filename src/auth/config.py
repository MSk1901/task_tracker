from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')
    jwt_secret: str
    user_manager_secret: str


settings = Settings()
