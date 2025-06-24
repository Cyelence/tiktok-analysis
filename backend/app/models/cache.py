from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
import uuid

from app.core.database import Base

class CacheEntry(Base):
    """
    Model for storing cached data to improve performance.
    
    This table stores:
    - API response caching
    - Computed trend data
    - ML model predictions
    - Frequently accessed data
    """
    __tablename__ = "cache_entries"
    
    # Primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Cache key and type
    cache_key = Column(String, unique=True, nullable=False, index=True)  # Unique cache key
    cache_type = Column(String, nullable=False, index=True)  # 'api_response', 'trend_data', 'ml_prediction'
    
    # Cached data
    data = Column(JSONB, nullable=False)  # The actual cached data
    
    # Cache metadata
    size_bytes = Column(Integer, default=0)  # Size of cached data in bytes
    hit_count = Column(Integer, default=0)  # Number of times this cache was accessed
    last_accessed = Column(DateTime, default=func.now())  # Last time cache was accessed
    
    # Expiration
    expires_at = Column(DateTime, nullable=False, index=True)  # When cache expires
    ttl_seconds = Column(Integer, default=3600)  # Time to live in seconds
    
    # Status
    is_valid = Column(Boolean, default=True, index=True)  # Is cache still valid?
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_cache_type_expires', 'cache_type', 'expires_at'),
        Index('idx_cache_valid_expires', 'is_valid', 'expires_at'),
        Index('idx_cache_hit_count', 'hit_count'),
        Index('idx_cache_last_accessed', 'last_accessed'),
        Index('idx_data_gin', 'data', postgresql_using='gin'),
    )
    
    def __repr__(self):
        return f"<CacheEntry(id={self.id}, key={self.cache_key}, type={self.cache_type})>"
    
    @property
    def is_expired(self) -> bool:
        """Check if cache entry has expired"""
        from datetime import datetime
        return datetime.utcnow() > self.expires_at
    
    @property
    def age_seconds(self) -> int:
        """Get age of cache entry in seconds"""
        from datetime import datetime
        return int((datetime.utcnow() - self.created_at).total_seconds())
    
    def increment_hit_count(self):
        """Increment the hit count and update last accessed time"""
        self.hit_count += 1
        self.last_accessed = func.now()
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            "id": self.id,
            "cache_key": self.cache_key,
            "cache_type": self.cache_type,
            "data": self.data,
            "size_bytes": self.size_bytes,
            "hit_count": self.hit_count,
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "ttl_seconds": self.ttl_seconds,
            "is_valid": self.is_valid,
            "is_expired": self.is_expired,
            "age_seconds": self.age_seconds,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 