"""
Configuration loader using python-dotenv.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / '.env')

class Config:
    """Application configuration with sensible defaults."""
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key')
    UPLOAD_FOLDER: str = os.getenv('UPLOAD_FOLDER', str(BASE_DIR / 'uploads'))
    OUTPUT_FOLDER: str = os.getenv('OUTPUT_FOLDER', str(BASE_DIR / 'compressed'))
    MAX_CONTENT_LENGTH: int = int(os.getenv('MAX_CONTENT_LENGTH', 5 * 1024 * 1024))  # 5 MiB
    COMPRESSION_QUALITY: int = int(os.getenv('COMPRESSION_QUALITY', 70))

    # Flask-specific settings
    DEBUG: bool = os.getenv('FLASK_ENV', 'development') == 'development'