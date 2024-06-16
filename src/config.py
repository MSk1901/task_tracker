from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')
    db_user: str
    db_pass: str
    db_host: str
    db_port: str
    db_name: str

    test_db_name: str


settings = Settings()
