"""
Configuration management for PLAGIATTRACKER
"""
import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # App Info
    APP_NAME: str = "PLAGIATTRACKER"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    def get_cors_origins(self) -> list:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    # Contact & Support
    SUPPORT_EMAIL: str = "checkone076@gmail.com"
    PARTNER_PHONE: str = "+237690895735"

    # Academic APIs (optional, can be user-provided)
    SEMANTIC_SCHOLAR_API_KEY: str = ""
    PUBMED_API_KEY: str = ""

    # AI Correction APIs (optional, user-provided)
    GROQ_API_KEY: str = ""
    CLAUDE_API_KEY: str = ""

    # Hugging Face
    HF_HOME: str = "/app/models"
    TRANSFORMERS_CACHE: str = "/app/models"

    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: str = "pdf,docx,txt"
    UPLOAD_DIR: str = "/app/uploads"

    def get_allowed_extensions(self) -> list:
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    RATE_LIMIT_PER_DAY: int = 100

    # Activation Codes
    CODE_EXPIRY_DAYS_TRIAL: int = 7
    CODE_EXPIRY_DAYS_PAID: int = 30
    CODE_EXPIRY_DAYS_INSTITUTION: int = 365

    # Processing
    MIN_TEXT_LENGTH: int = 100  # Minimum text length for analysis
    CHUNK_SIZE: int = 500  # Words per chunk for plagiarism detection
    CHUNK_OVERLAP: int = 50  # Overlap between chunks

    # Cache TTL (seconds)
    CACHE_TTL_SHORT: int = 3600  # 1 hour
    CACHE_TTL_LONG: int = 86400  # 24 hours

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# Create global settings instance
settings = Settings()


# Academic API endpoints
ACADEMIC_APIS = {
    "arxiv": {
        "base_url": "http://export.arxiv.org/api/query",
        "requires_key": False,
    },
    "openalex": {
        "base_url": "https://api.openalex.org",
        "requires_key": False,
    },
    "crossref": {
        "base_url": "https://api.crossref.org/works",
        "requires_key": False,
    },
    "semantic_scholar": {
        "base_url": "https://api.semanticscholar.org/graph/v1",
        "requires_key": True,
    },
    "pubmed": {
        "base_url": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils",
        "requires_key": True,
    },
}


# Plan configurations
PLANS = {
    "trial": {
        "name": "Essai",
        "price_fcfa": 0,
        "analyses_limit": 3,
        "validity_days": 7,
        "code_prefix": "TRIAL",
    },
    "student": {
        "name": "Étudiant",
        "price_fcfa": 2500,
        "analyses_limit": 50,
        "validity_days": 30,
        "code_prefix": "STU",
    },
    "teacher": {
        "name": "Enseignant",
        "price_fcfa": 5000,
        "analyses_limit": 200,
        "validity_days": 30,
        "code_prefix": "TCH",
    },
    "researcher": {
        "name": "Chercheur",
        "price_fcfa": 10000,
        "analyses_limit": 500,
        "validity_days": 30,
        "code_prefix": "RES",
    },
    "institution": {
        "name": "Institution",
        "price_fcfa": None,  # Sur devis
        "analyses_limit": -1,  # Illimité
        "validity_days": 365,
        "code_prefix": "INS",
    },
}
