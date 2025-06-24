from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
import uuid

from app.core.database import Base

class TrendMetrics(Base):
    """
    Model for storing trend metrics over time.
    
    This table stores time-series data for:
    - Brand performance trends
    - Style popularity trends
    - Fashion item trends
    - Hashtag trends
    """
    __tablename__ = "trend_metrics"
    
    # Primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Entity identification
    entity_name = Column(String, nullable=False, index=True)  # Brand name, style name, etc.
    entity_type = Column(String, nullable=False, index=True)  # 'brand', 'style', 'item', 'hashtag'
    
    # Time period
    date = Column(DateTime, nullable=False, index=True)  # Date for this metric
    period = Column(String, default='daily', index=True)  # 'hourly', 'daily', 'weekly', 'monthly'
    
    # Core metrics
    mention_count = Column(Integer, default=0, index=True)  # Number of mentions
    engagement_score = Column(Float, default=0.0, index=True)  # Average engagement
    sentiment_score = Column(Float, default=0.0)  # Sentiment analysis (-1 to 1)
    momentum_score = Column(Float, default=0.0, index=True)  # Trend momentum
    growth_rate = Column(Float, default=0.0)  # Growth rate from previous period
    reach_estimate = Column(Integer, default=0)  # Estimated reach
    
    # Additional metrics
    video_count = Column(Integer, default=0)  # Number of videos mentioning this entity
    unique_authors = Column(Integer, default=0)  # Number of unique authors
    average_views = Column(Float, default=0.0)  # Average views per video
    
    # Trend indicators
    is_trending = Column(Boolean, default=False, index=True)  # Is this trending?
    trend_strength = Column(Float, default=0.0, index=True)  # How strong is the trend?
    
    # Additional data
    metadata = Column(JSONB)  # Store additional trend data
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Indexes for performance optimization
    __table_args__ = (
        # Composite indexes for common query patterns
        Index('idx_entity_name_type_date', 'entity_name', 'entity_type', 'date'),
        Index('idx_entity_type_date', 'entity_type', 'date'),
        Index('idx_trending_date', 'is_trending', 'date'),
        Index('idx_momentum_date', 'momentum_score', 'date'),
        Index('idx_mention_count_date', 'mention_count', 'date'),
        Index('idx_metadata_gin', 'metadata', postgresql_using='gin'),
    )
    
    def __repr__(self):
        return f"<TrendMetrics(id={self.id}, entity={self.entity_name}, type={self.entity_type}, date={self.date})>"
    
    @property
    def trend_direction(self) -> str:
        """
        Determine trend direction based on growth rate.
        """
        if self.growth_rate > 0.1:  # 10% growth
            return "increasing"
        elif self.growth_rate < -0.1:  # 10% decline
            return "decreasing"
        else:
            return "stable"
    
    @property
    def trend_category(self) -> str:
        """
        Categorize trend strength.
        """
        if self.trend_strength > 0.8:
            return "viral"
        elif self.trend_strength > 0.6:
            return "trending"
        elif self.trend_strength > 0.4:
            return "growing"
        elif self.trend_strength > 0.2:
            return "stable"
        else:
            return "declining"
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            "id": self.id,
            "entity_name": self.entity_name,
            "entity_type": self.entity_type,
            "date": self.date.isoformat() if self.date else None,
            "period": self.period,
            "mention_count": self.mention_count,
            "engagement_score": self.engagement_score,
            "sentiment_score": self.sentiment_score,
            "momentum_score": self.momentum_score,
            "growth_rate": self.growth_rate,
            "reach_estimate": self.reach_estimate,
            "video_count": self.video_count,
            "unique_authors": self.unique_authors,
            "average_views": self.average_views,
            "is_trending": self.is_trending,
            "trend_strength": self.trend_strength,
            "trend_direction": self.trend_direction,
            "trend_category": self.trend_category,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 