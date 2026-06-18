"""
Configuration management module for NayePankh AI Assistant.
Handles environment variables and application settings.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Optional Streamlit import for secrets
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False


class Config:
    """Application configuration class."""
    
    # Base paths
    BASE_DIR: Path = Path(__file__).parent.absolute()
    DATA_DIR: Path = BASE_DIR / "data"
    MEMORY_DIR: Path = BASE_DIR / "memory"
    DATABASE_PATH: Path = BASE_DIR / "volunteers.db"
    
    # Get secret from Streamlit secrets or environment variables
    @staticmethod
    def get_secret(key: str, default: Optional[str] = None) -> str:
        """Get secret from Streamlit secrets or environment variables."""
        if STREAMLIT_AVAILABLE:
            try:
                return st.secrets[key]
            except (KeyError, FileNotFoundError):
                return os.getenv(key, default)
        return os.getenv(key, default)
    
    # Admin credentials
    ADMIN_USERNAME: str = get_secret("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD: str = get_secret("ADMIN_PASSWORD", "changeme")
    
    # API Keys
    GEMINI_API_KEY: str = get_secret("GEMINI_API_KEY", "")
    RESEND_API_KEY: str = get_secret("RESEND_API_KEY", "")
    
    # Email configuration
    EMAIL_FROM: str = get_secret("EMAIL_FROM", "NayePankh <onboarding@resend.dev>")
    
    # Gemini configuration
    GEMINI_MODEL: str = "gemini-2.5-flash"
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_TOKENS: int = 1024
    GEMINI_TIMEOUT: int = 30
    
    # Memory configuration
    MEMORY_COLLECTION_NAME: str = "nayepankh_memory"
    MEMORY_MAX_RESULTS: int = 3
    MEMORY_RETENTION_DAYS: int = 30
    
    # Database configuration
    DB_TIMEOUT: int = 30
    
    # Application settings
    APP_TITLE: str = "NayePankh AI Volunteer Assistant"
    APP_ICON: str = "🤖"
    APP_LAYOUT: str = "wide"
    
    # Session configuration
    SESSION_TIMEOUT_MINUTES: int = 30
    
    # Rate limiting
    MAX_REQUESTS_PER_MINUTE: int = 60
    
    @classmethod
    def create_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.MEMORY_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required")
        if not cls.RESEND_API_KEY:
            print("Warning: RESEND_API_KEY not set - email features will be disabled")
        return True


# Initialize directories on import
Config.create_directories()
