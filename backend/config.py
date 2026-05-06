from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str = ""
    SPORTMONKS_API_KEY: str = ""
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/scout"
    PINECONE_API_KEY: str = ""
    PINECONE_ENV: str = ""
    LANGCHAIN_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
