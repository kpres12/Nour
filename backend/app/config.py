import os
from typing import List, Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    # Database - make optional for local dev
    DATABASE_URL: Optional[str] = "sqlite:///./nour.db"
    
    # JWT Settings
    JWT_SECRET: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Nour"
    
    # LLM Settings (optional)
    LLM_ENABLED: bool = False
    LLM_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gpt-3.5-turbo"
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10485760  # 10MB
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Local development mode
    LOCAL_DEV: bool = True
    SKIP_DB: bool = True
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
