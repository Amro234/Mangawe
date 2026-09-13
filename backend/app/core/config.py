import os
from pathlib import Path
from dotenv import load_dotenv

# *1. Resolve the path to the root directory where .env lives
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

# *2. Load the .env file if it exists
load_dotenv(dotenv_path=ENV_PATH)


class Settings:
    # App Settings
    PROJECT_NAME: str = "Mangawe"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    # Database Configuration
    # Resolves sqlite database path relative to project root by default
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", str(BASE_DIR / "mangawe.db"))

    # Security & JWT Settings
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", 
        "insecure-fallback-key-change-this-in-production"
    )
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # CORS Settings (frontend URLs allowed to communicate with backend)
    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS", 
            "http://localhost:3000,http://localhost:8000,http://127.0.0.1:5500"
        ).split(",")
        if origin.strip()
    ]


# 3. Create a single instance to be imported across the app
settings = Settings()