from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import uvicorn
from loguru import logger

from app.core.config import settings
from app.core.database import get_db, create_tables
from app.models.video import TikTokVideo
from app.models.fashion import FashionItem, BrandData, StyleData
from app.models.trends import TrendMetrics

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Fashion Trend Discovery API", "version": settings.version}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "fashion-trend-api",
        "version": settings.version
    }

# Database test endpoint
@app.get("/api/v1/db-test")
async def test_database(db: Session = Depends(get_db)):
    """Test database connection and basic operations"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        
        # Test model creation
        test_video = TikTokVideo(
            tiktok_id="test_123",
            author="test_author",
            author_id="test_author_id",
            caption="Test video caption",
            hashtags=["#fashion", "#test"],
            view_count=1000,
            like_count=100,
            comment_count=10,
            share_count=5,
            is_fashion_related=True
        )
        
        db.add(test_video)
        db.commit()
        db.refresh(test_video)
        
        # Clean up test data
        db.delete(test_video)
        db.commit()
        
        return {
            "status": "success",
            "message": "Database connection and operations working correctly",
            "test_video_id": test_video.id
        }
    except Exception as e:
        logger.error(f"Database test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database test failed: {str(e)}")

# Basic API endpoints for MVP
@app.get("/api/v1/trends")
async def get_trends(db: Session = Depends(get_db)):
    """Get current fashion trends - MVP placeholder"""
    return {
        "trends": [
            {
                "id": "1",
                "name": "Y2K Fashion",
                "category": "style",
                "momentum_score": 0.85,
                "mention_count": 1250,
                "description": "Early 2000s fashion revival"
            },
            {
                "id": "2", 
                "name": "Brandy Melville",
                "category": "brand",
                "momentum_score": 0.92,
                "mention_count": 2100,
                "description": "Trending teen fashion brand"
            }
        ]
    }

@app.get("/api/v1/brands")
async def get_brands(db: Session = Depends(get_db)):
    """Get trending brands - MVP placeholder"""
    return {
        "brands": [
            {
                "id": "1",
                "name": "Brandy Melville",
                "category": ["clothing", "teen"],
                "price_range": "mid-range",
                "trending_score": 0.92
            },
            {
                "id": "2",
                "name": "Urban Outfitters", 
                "category": ["clothing", "lifestyle"],
                "price_range": "mid-range",
                "trending_score": 0.78
            }
        ]
    }

@app.get("/api/v1/styles")
async def get_styles(db: Session = Depends(get_db)):
    """Get trending styles - MVP placeholder"""
    return {
        "styles": [
            {
                "id": "1",
                "name": "Y2K",
                "description": "Early 2000s aesthetic",
                "popularity_score": 0.85,
                "seasonality": ["spring", "summer"]
            },
            {
                "id": "2",
                "name": "Minimalist",
                "description": "Clean, simple aesthetic", 
                "popularity_score": 0.72,
                "seasonality": ["all"]
            }
        ]
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Fashion Trend Discovery API")
    try:
        # Create database tables
        create_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    ) 