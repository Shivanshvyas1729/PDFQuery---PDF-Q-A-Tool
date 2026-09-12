from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized configuration using Pydantic Settings.
    Automatically loads from .env file and environment variables.
    """

    # Directory Paths (resolves to project root)
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    UPLOADS_DIR: Path = DATA_DIR / "uploads"
    VECTOR_STORE_DIR: Path = DATA_DIR / "vector_store"

    # API Credentials
    AICREDITS_API_KEY: str = Field(default="", description="API key for LLM and Embeddings")
    AICREDITS_BASE_URL: str = Field(
        default="https://aicredits.in/v1",
        description="Base URL for OpenAI-compatible endpoint"
    )

    # Model Configuration
    EMBEDDING_MODEL: str = Field(
        default="openai/text-embedding-3-small",
        description="Embedding model"
    )
    LLM_MODEL: str = Field(
        default="openai/gpt-4o-mini",
        description="Chat model for answer generation"
    )
    LLM_TEMPERATURE: float = Field(default=0.1, ge=0.0, le=1.0)

    # Document Chunking Settings
    CHUNK_SIZE: int = Field(default=1000, description="Chunk size in characters")
    CHUNK_OVERLAP: int = Field(default=200, description="Chunk overlap in characters")

    # Retrieval Settings
    TOP_K_RESULTS: int = Field(default=4, description="Number of context chunks to retrieve")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    def init_directories(self) -> None:
        """Ensure necessary data folders exist."""
        self.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        self.VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)


# Global singleton instance
settings = Settings()
settings.init_directories()
