import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    # General
    log_level: str = os.getenv("JOB_SCRAPY_LOG_LEVEL", "INFO")
    
    # Scraping limits
    max_results: int = int(os.getenv("JOB_SCRAPY_MAX_RESULTS", "20"))
    timeout: int = int(os.getenv("JOB_SCRAPY_TIMEOUT", "30"))
    max_concurrency: int = int(os.getenv("JOB_SCRAPY_MAX_CONCURRENCY", "3"))
    
    # API Keys (Remote Boards)
    findwork_api_key: str | None = os.getenv("FINDWORK_API_KEY")
    jooble_api_key: str | None = os.getenv("JOOBLE_API_KEY")
    adzuna_app_id: str | None = os.getenv("ADZUNA_APP_ID")
    adzuna_app_key: str | None = os.getenv("ADZUNA_APP_KEY")
    usajobs_api_key: str | None = os.getenv("USAJOBS_API_KEY")
    themuse_api_key: str | None = os.getenv("THEMUSE_API_KEY")

settings = Settings()
