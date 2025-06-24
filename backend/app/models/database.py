from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from datetime import datetime
import os
from transformers import pipeline, WhisperProcessor, WhisperForConditionalGeneration
import easyocr
import asyncio
from functools import lru_cache
from typing import List

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://fashion_user:fashion_password@localhost:5432/fashion_trends")

# Create engine with connection pooling for cost efficiency
engine = create_engine(
    DATABASE_URL,
    pool_size=5,  # Small pool size for cost efficiency
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,  # Recycle connections every 5 minutes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Use smaller, faster models for MVP
MODEL_CONFIG = {
    "object_detection": "yolos-tiny",  # Fast, lightweight
    "image_classification": "resnet-18",  # Smaller than ResNet-50
    "speech_recognition": "whisper-tiny",  # Faster than base model
    "ocr": "easyocr"  # Free alternative to paid services
}

# Pre-trained models (no training costs)
object_detector = pipeline("object-detection", model="hustvl/yolos-tiny")
image_classifier = pipeline("image-classification", model="microsoft/resnet-50")

# Use Whisper for speech recognition
processor = WhisperProcessor.from_pretrained("openai/whisper-base")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")

class TikTokVideo(Base):
    __tablename__ = "tiktok_videos"
    
    id = Column(String, primary_key=True)
    tiktok_id = Column(String, unique=True, nullable=False)
    author = Column(String, nullable=False)
    author_id = Column(String, nullable=False)
    caption = Column(Text)
    hashtags = Column(ARRAY(String))
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    video_url = Column(String)
    thumbnail_url = Column(String)
    duration = Column(Integer)
    is_fashion_related = Column(Boolean, default=False)
    
    # Cost-effective storage: Use JSONB for flexible data
    metadata = Column(JSONB)
    
    # Indexes for performance (cost-effective queries)
    __table_args__ = (
        Index('idx_author_id', 'author_id'),
        Index('idx_created_at', 'created_at'),
        Index('idx_fashion_related', 'is_fashion_related'),
        Index('idx_view_count', 'view_count'),
        Index('idx_hashtags', 'hashtags', postgresql_using='gin'),
    )


class FashionItem(Base):
    __tablename__ = "fashion_items"
    
    id = Column(String, primary_key=True)
    video_id = Column(String, nullable=False)
    item_type = Column(String, nullable=False)  # 'clothing', 'accessory', 'brand', 'style'
    name = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    
    # Store bounding box as JSON for flexibility
    bounding_box = Column(JSONB)
    
    # Cost-effective: Store attributes as JSONB instead of separate columns
    attributes = Column(JSONB)  # color, pattern, material, brand, etc.
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_video_id', 'video_id'),
        Index('idx_item_type', 'item_type'),
        Index('idx_name', 'name'),
        Index('idx_confidence', 'confidence'),
    )


class TrendMetrics(Base):
    __tablename__ = "trend_metrics"
    
    id = Column(String, primary_key=True)
    entity_name = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)  # 'brand', 'style', 'item', 'hashtag'
    date = Column(DateTime, nullable=False)
    mention_count = Column(Integer, default=0)
    engagement_score = Column(Float, default=0.0)
    sentiment_score = Column(Float, default=0.0)
    momentum_score = Column(Float, default=0.0)
    growth_rate = Column(Float, default=0.0)
    reach_estimate = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_entity_name_type', 'entity_name', 'entity_type'),
        Index('idx_date', 'date'),
        Index('idx_momentum_score', 'momentum_score'),
        Index('idx_engagement_score', 'engagement_score'),
    )


class BrandData(Base):
    __tablename__ = "brands"
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    website = Column(String)
    
    # Store social media links as JSONB for flexibility
    social_media = Column(JSONB)
    
    # Store categories as array for efficient querying
    categories = Column(ARRAY(String))
    price_range = Column(String)  # 'budget', 'mid-range', 'luxury'
    target_audience = Column(ARRAY(String))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_brand_name', 'name'),
        Index('idx_categories', 'categories', postgresql_using='gin'),
        Index('idx_price_range', 'price_range'),
    )


class StyleData(Base):
    __tablename__ = "styles"
    
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    category = Column(String, nullable=False)
    subcategories = Column(ARRAY(String))
    seasonality = Column(ARRAY(String))
    popularity_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_style_name', 'name'),
        Index('idx_category', 'category'),
        Index('idx_popularity_score', 'popularity_score'),
    )


class CacheEntry(Base):
    __tablename__ = "cache_entries"
    
    id = Column(String, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(JSONB)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_cache_key', 'key'),
        Index('idx_expires_at', 'expires_at'),
    )


class VideoAnalysis(Base):
    __tablename__ = "video_analyses"
    
    id = Column(String, primary_key=True)
    video_id = Column(String, nullable=False)
    
    # Visual analysis results
    detected_items = Column(JSONB)  # Clothing items, brands, colors
    style_classification = Column(JSONB)
    
    # Text analysis results
    extracted_text = Column(ARRAY(String))
    brand_mentions = Column(ARRAY(String))
    product_mentions = Column(ARRAY(String))
    
    # Audio analysis results
    transcription = Column(Text)
    audio_brand_mentions = Column(ARRAY(String))
    sentiment_score = Column(Float)
    
    # Combined results
    confidence_score = Column(Float)
    fashion_relevance_score = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)


# Run all analyses concurrently for speed
async def analyze_video(video_url):
    # Visual analysis
    visual_results = await analyze_visual_content(video_frames)
    
    # Text extraction (OCR)
    text_results = await extract_text_overlays(video_frames)
    
    # Audio analysis
    audio_results = await analyze_audio_content(audio_segment)
    
    return combine_results(visual_results, text_results, audio_results)


# Extract text from video frames
reader = easyocr.Reader(['en'])
text_results = []

for frame in video_frames:
    results = reader.readtext(frame)
    text_results.extend([text[1] for text in results])

# Transcribe audio
audio_input = processor(audio_segment, return_tensors="pt")
transcription = model.generate(audio_input)

class VideoAnalyzer:
    def __init__(self):
        self.visual_analyzer = VisualAnalyzer()
        self.text_analyzer = TextAnalyzer()
        self.audio_analyzer = AudioAnalyzer()
    
    async def analyze_video(self, video_url: str) -> VideoAnalysis:
        # Download video (with caching)
        video_path = await self.download_video(video_url)
        
        # Extract components
        frames = self.extract_frames(video_path)
        audio = self.extract_audio(video_path)
        
        # Parallel analysis
        visual_results, text_results, audio_results = await asyncio.gather(
            self.visual_analyzer.analyze(frames),
            self.text_analyzer.analyze(frames),
            self.audio_analyzer.analyze(audio)
        )
        
        return self.combine_results(visual_results, text_results, audio_results) 

# Process videos in batches to reduce costs
class BatchProcessor:
    def __init__(self, batch_size=5):
        self.batch_size = batch_size
        self.queue = asyncio.Queue()
    
    async def process_batch(self):
        videos = []
        for _ in range(self.batch_size):
            if not self.queue.empty():
                videos.append(await self.queue.get())
        
        # Process batch together
        results = await self.analyze_batch(videos)
        return results 

# Cache ML model results
@lru_cache(maxsize=32)  # 32 entries cache
async def analyze_video_cached(video_id: str):
    return await analyze_video(video_id)

# Process multiple videos together
async def process_video_batch(video_urls: List[str]):
    # Download all videos
    videos = await download_videos(video_urls)
    
    # Extract frames and audio in parallel
    frames_batch = await extract_frames_batch(videos)
    audio_batch = await extract_audio_batch(videos)
    
    # Run ML models on batches
    results = await run_ml_models_batch(frames_batch, audio_batch)
    
    return results 