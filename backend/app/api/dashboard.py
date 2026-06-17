from fastapi import APIRouter

from app.services.dashboard_service import (
    get_summary,
    get_platform_distribution,
    get_sentiment_distribution
)

router = APIRouter()


@router.get("/summary")
def dashboard_summary():
    return get_summary()


@router.get("/platforms")
def dashboard_platforms():
    return get_platform_distribution()


@router.get("/sentiment")
def dashboard_sentiment():
    return get_sentiment_distribution()