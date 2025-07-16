from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.orm import Session
from ..models.schemas import TopProduct, TrendPoint
from ..services.analytics import get_top_products, get_posting_trends
from ..services.database import get_db

router = APIRouter()

@router.get("/top-products", response_model=List[TopProduct])
async def top_products(
    limit: int = Query(10, gt=0, le=100),
    db: Session = Depends(get_db)
):
    """Get top mentioned medical products"""
    return get_top_products(db, limit)

@router.get("/posting-trends", response_model=List[TrendPoint])
async def posting_trends(
    period: str = Query("day", regex="^(day|week|month)$"),
    db: Session = Depends(get_db)
):
    """Get message posting trends over time"""
    return get_posting_trends(db, period)