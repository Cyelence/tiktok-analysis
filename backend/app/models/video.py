from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean, Index, BigInteger
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from app.core.database import Base

class TikTokVideo(Base):
    """
    Model for storing TikTok video data.
    
    This table stores the core video metadata including:
    - Basic video information (ID, author, caption)
    - Engagement metrics (views, likes, comments, shares)
    - Content analysis results (fashion-related flag)
    - Processing status and timestamps
    """
    __tablename__ = "tiktok_videos"
    
    # Primary key - using UUID for scalability
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # TikTok-specific fields
    tiktok_id = Column(String, unique=True, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    author_id = Column(String, nullable=False, index=True)
    
    # Content fields
    caption = Column(Text)  # Video caption/description
    hashtags = Column(ARRAY(String))  # Array of hashtags
    
    # Engagement metrics - using BigInteger for large numbers
    view_count = Column(BigInteger, default=0, index=True)
    like_count = Column(BigInteger, default=0)
    comment_count = Column(BigInteger, default=0)
    share_count = Column(BigInteger, default=0)
    
    # Media URLs
    video_url = Column(String)
    thumbnail_url = Column(String)
    duration = Column(Integer)  # Duration in seconds
    
    # Analysis flags
    is_fashion_related = Column(Boolean, default=False, index=True)
    is_processed = Column(Boolean, default=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), index=True)
    processed_at = Column(DateTime)
    tiktok_created_at = Column(DateTime)  # When video was created on TikTok
    
    # Flexible metadata storage using JSONB
    metadata = Column(JSONB)  # Store additional TikTok metadata
    
    # Indexes for performance optimization
    __table_args__ = (
        # Composite indexes for common query patterns
        Index('idx_author_fashion', 'author_id', 'is_fashion_related'),
        Index('idx_created_fashion', 'created_at', 'is_fashion_related'),
        Index('idx_views_fashion', 'view_count', 'is_fashion_related'),
        Index('idx_hashtags_gin', 'hashtags', postgresql_using='gin'),
        Index('idx_metadata_gin', 'metadata', postgresql_using='gin'),
    )
    
    def __repr__(self):
        return f"<TikTokVideo(id={self.id}, tiktok_id={self.tiktok_id}, author={self.author})>"
    
    @property
    def engagement_score(self) -> float:
        """
        Calculate engagement score based on likes, comments, and shares.
        This is useful for trend analysis.
        """
        if self.view_count == 0:
            return 0.0
        
        # Weighted engagement calculation
        engagement = (
            (self.like_count * 1.0) +
            (self.comment_count * 2.0) +
            (self.share_count * 3.0)
        ) / self.view_count
        
        return min(engagement, 1.0)  # Cap at 100%
    
    @property
    def total_engagement(self) -> int:
        """Total engagement (likes + comments + shares)"""
        return self.like_count + self.comment_count + self.share_count
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            "id": self.id,
            "tiktok_id": self.tiktok_id,
            "author": self.author,
            "author_id": self.author_id,
            "caption": self.caption,
            "hashtags": self.hashtags,
            "view_count": self.view_count,
            "like_count": self.like_count,
            "comment_count": self.comment_count,
            "share_count": self.share_count,
            "video_url": self.video_url,
            "thumbnail_url": self.thumbnail_url,
            "duration": self.duration,
            "is_fashion_related": self.is_fashion_related,
            "is_processed": self.is_processed,
            "engagement_score": self.engagement_score,
            "total_engagement": self.total_engagement,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "tiktok_created_at": self.tiktok_created_at.isoformat() if self.tiktok_created_at else None,
        } 