from pydantic_settings import BaseSettings


# environmental variables -> good for securing our informations instead of hard coding them in our application
# .env file
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config:
        env_file= ".env"

settings = Settings()
