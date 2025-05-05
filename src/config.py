from pydantic import BaseModel, SecretStr

class DatabaseSetting(BaseModel):
    db_username: str
    db_name: str
    db_password: SecretStr
    db_host: str
    db_port: int

    class Config:
        env_file = ".env"
