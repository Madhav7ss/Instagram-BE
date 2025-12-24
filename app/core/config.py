from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb+srv://guthavamsisoftsuave_db_user:NuaAHOnxPFaoQ7ZD@instagram.vxy98se.mongodb.net/?appName=Instagram"
    MONGO_DB_NAME: str = "instagram_db"

    class Config:
        env_file = ".env"

settings = Settings()
