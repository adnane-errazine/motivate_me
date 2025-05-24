import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Configuration class for the application"""

    # Mistral API Configuration
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    MISTRAL_MODEL: str = "mistral-medium-latest"  # "mistral-small-latest"

    # Google Custom Search Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_CSE_ID: str = os.getenv("GOOGLE_CSE_ID", "")

    # Image Search Settings
    MAX_IMAGE_RESULTS: int = 2
    IMAGE_SEARCH_SAFE: str = "active"

    # LLM Settings
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.3

    # Workflow Settings
    MAX_CONCEPTS_PER_REQUEST: int = 10
    CONCEPT_CONFIDENCE_THRESHOLD: float = 0.6

    # File Settings
    # ALLOWED_IMAGE_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    # MAX_FILE_SIZE_MB: int = 10

    def validate(self) -> bool:
        """Validate that required configuration is present"""
        required_fields = [
            self.MISTRAL_API_KEY,
            self.GOOGLE_API_KEY,
            self.GOOGLE_CSE_ID,
        ]
        return all(field for field in required_fields)

    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables"""
        return cls()


# Global config instance
config = Config.from_env()
