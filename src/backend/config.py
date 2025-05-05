from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings

class DatabaseSetting(BaseSettings):
    db_username: str = Field(..., env="DB_USERNAME")
    db_name: str = Field(..., env="DB_NAME")
    db_password: SecretStr = Field(..., env="DB_PASSWORD")
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'