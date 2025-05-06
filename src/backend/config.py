from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings

class DatabaseSetting(BaseSettings):
    db_username: str = Field(default="postgres", alias="DB_USERNAME")
    db_name: str = Field(default="postgres", alias="DB_NAME")
    db_password: str = Field(default="postgres", alias="DB_PASSWORD")
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"