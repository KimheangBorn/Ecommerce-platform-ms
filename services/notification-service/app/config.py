from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    
    class Config:
        env_file = ".env"

settings = Settings()
