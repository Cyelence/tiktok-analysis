from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os
from loguru import logger

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://fashion_user:fashion_password@localhost:5432/fashion_trends")

# Create engine with connection pooling for cost efficiency
engine = create_engine(
    DATABASE_URL,
    # Connection pooling settings for cost optimization
    poolclass=QueuePool,
    pool_size=5,  # Small pool size for cost efficiency
    max_overflow=10,  # Allow up to 10 additional connections
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,  # Recycle connections every 5 minutes
    pool_timeout=30,  # Wait up to 30 seconds for available connection
    echo=False,  # Set to True for SQL query logging in development
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db():
    """
    Database dependency for FastAPI.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_tables():
    """
    Create all database tables.
    This should be called on application startup.
    """
    try:
        # Import all models to ensure they're registered with Base
        from app.models.video import TikTokVideo
        from app.models.fashion import FashionItem, BrandData, StyleData
        from app.models.trends import TrendMetrics
        from app.models.cache import CacheEntry
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

def drop_tables():
    """
    Drop all database tables.
    WARNING: This will delete all data!
    Only use in development/testing.
    """
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
    except Exception as e:
        logger.error(f"Failed to drop database tables: {e}")
        raise 