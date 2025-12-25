from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb+srv://zerohathacker_db_user:CUYjQe3zTlBX2KMq@cluster0.dohzfpo.mongodb.net/?appName=Cluster0"
    MONGO_DB_NAME: str = "instagram_db"
    SECRET_KEY: str = "instagram"  # move to .env in prod
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()