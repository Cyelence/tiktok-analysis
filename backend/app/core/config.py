from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Application
    app_name: str = "Fashion Trend Discovery API"
    version: str = "1.0.0"
    debug: bool = False
    
    # Database - Supports Railway's DATABASE_URL
    database_url: str = "postgresql://fashion_user:fashion_password@localhost:5432/fashion_trends"
    
    # Redis - Supports Upstash's REDIS_URL
    redis_url: str = "redis://localhost:6379"
    
    # TikTok API
    tiktok_api_key: Optional[str] = None
    tiktok_api_secret: Optional[str] = None
    tiktok_base_url: str = "https://api.tiktok.com"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Rate limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds
    
    # ML Model settings (cost-optimized)
    ml_model_cache_size: int = 10  # Keep only 10 models in memory
    batch_size: int = 5  # Process 5 videos at a time
    max_concurrent_requests: int = 3  # Limit concurrent ML requests
    
    # Caching
    cache_ttl: int = 3600  # 1 hour
    cache_max_size: int = 1000  # Max 1000 cached items
    
    # Logging
    log_level: str = "INFO"
    
    # CORS
    allowed_origins: list = [
        "http://localhost:3000",
        "https://your-frontend-domain.vercel.app",
        "https://fashion-trend-discovery.vercel.app"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings()

# Environment-specific overrides
if os.getenv("RAILWAY_ENVIRONMENT"):
    # Running on Railway
    settings.debug = False
    settings.log_level = "INFO"
elif os.getenv("VERCEL_ENV"):
    # Running on Vercel
    settings.debug = False
    settings.log_level = "INFO"
else:
    # Local development
    settings.debug = True
    settings.log_level = "DEBUG" 