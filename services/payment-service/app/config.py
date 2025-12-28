from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/payment_db"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    
    class Config:
        env_file = ".env"

settings = Settings()
