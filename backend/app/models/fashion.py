from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean, Index, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base

class FashionItem(Base):
    """
    Model for storing detected fashion items from videos.
    
    This table stores items detected through:
    - Computer vision analysis
    - Text extraction (OCR)
    - Audio transcription
    """
    __tablename__ = "fashion_items"
    
    # Primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign key to video
    video_id = Column(String, ForeignKey("tiktok_videos.id"), nullable=False, index=True)
    
    # Item identification
    item_type = Column(String, nullable=False, index=True)  # 'clothing', 'accessory', 'brand', 'style'
    name = Column(String, nullable=False, index=True)
    confidence = Column(Float, nullable=False, index=True)  # Detection confidence (0-1)
    
    # Detection source
    detection_source = Column(String, nullable=False)  # 'visual', 'text', 'audio', 'combined'
    
    # Visual detection data (if applicable)
    bounding_box = Column(JSONB)  # {x, y, width, height}
    frame_number = Column(Integer)  # Which frame the item was detected in
    
    # Item attributes - flexible storage using JSONB
    attributes = Column(JSONB)  # color, pattern, material, brand, etc.
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), index=True)
    
    # Relationship to video
    video = relationship("TikTokVideo", backref="fashion_items")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_video_item_type', 'video_id', 'item_type'),
        Index('idx_name_confidence', 'name', 'confidence'),
        Index('idx_detection_source', 'detection_source'),
        Index('idx_attributes_gin', 'attributes', postgresql_using='gin'),
    )
    
    def __repr__(self):
        return f"<FashionItem(id={self.id}, name={self.name}, type={self.item_type})>"
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            "id": self.id,
            "video_id": self.video_id,
            "item_type": self.item_type,
            "name": self.name,
            "confidence": self.confidence,
            "detection_source": self.detection_source,
            "bounding_box": self.bounding_box,
            "frame_number": self.frame_number,
            "attributes": self.attributes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class BrandData(Base):
    """
    Model for storing brand information and performance data.
    """
    __tablename__ = "brands"
    
    # Primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Brand information
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text)
    website = Column(String)
    
    # Social media presence
    social_media = Column(JSONB)  # {instagram, tiktok, twitter, etc.}
    
    # Brand categorization
    categories = Column(ARRAY(String), index=True)  # ['clothing', 'teen', 'streetwear']
    price_range = Column(String, index=True)  # 'budget', 'mid-range', 'luxury'
    target_audience = Column(ARRAY(String))  # ['teen', 'young-adult', 'adult']
    
    # Performance metrics
    total_mentions = Column(Integer, default=0)
    trending_score = Column(Float, default=0.0, index=True)
    average_engagement = Column(Float, default=0.0)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_brand_categories_gin', 'categories', postgresql_using='gin'),
        Index('idx_brand_price_range', 'price_range'),
        Index('idx_brand_trending', 'trending_score'),
    )
    
    def __repr__(self):
        return f"<BrandData(id={self.id}, name={self.name})>"
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "website": self.website,
            "social_media": self.social_media,
            "categories": self.categories,
            "price_range": self.price_range,
            "target_audience": self.target_audience,
            "total_mentions": self.total_mentions,
            "trending_score": self.trending_score,
            "average_engagement": self.average_engagement,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class StyleData(Base):
    """
    Model for storing fashion style information and popularity data.
    """
    __tablename__ = "styles"
    
    # Primary key
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Style information
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text)
    category = Column(String, nullable=False, index=True)  # 'aesthetic', 'era', 'subculture'
    
    # Style characteristics
    subcategories = Column(ARRAY(String))  # ['grunge', 'punk', 'goth']
    seasonality = Column(ARRAY(String))  # ['spring', 'summer', 'fall', 'winter']
    color_palette = Column(ARRAY(String))  # ['black', 'white', 'pastels']
    
    # Performance metrics
    popularity_score = Column(Float, default=0.0, index=True)
    total_mentions = Column(Integer, default=0)
    growth_rate = Column(Float, default=0.0)  # Weekly growth rate
    
    # Status
    is_trending = Column(Boolean, default=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_style_category', 'category'),
        Index('idx_style_popularity', 'popularity_score'),
        Index('idx_style_trending', 'is_trending'),
        Index('idx_style_subcategories_gin', 'subcategories', postgresql_using='gin'),
    )
    
    def __repr__(self):
        return f"<StyleData(id={self.id}, name={self.name})>"
    
    def to_dict(self):
        """Convert model to dictionary for API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "subcategories": self.subcategories,
            "seasonality": self.seasonality,
            "color_palette": self.color_palette,
            "popularity_score": self.popularity_score,
            "total_mentions": self.total_mentions,
            "growth_rate": self.growth_rate,
            "is_trending": self.is_trending,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 