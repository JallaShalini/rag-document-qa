from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'
load_dotenv(dotenv_path=ENV_PATH)


class Settings(BaseSettings):
    llm_api_key: str | None = None
    llm_provider: str | None = None
    model_name: str | None = None
    upload_path: str | None = None
    chroma_path: str | None = None
    log_path: str | None = None
    top_k: int | None = None
    chunk_size: int | None = None
    chunk_overlap: int | None = None

    class Config:
        env_file = ENV_PATH
        case_sensitive = False


settings = Settings()
