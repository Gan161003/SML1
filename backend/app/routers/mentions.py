from fastapi import APIRouter

from app.services.mentions_service import (
    get_keywords,
    get_overview,
    get_charts,
    get_content
)
from app.services.mentions_service import (
    get_top_content,
    get_top_positive,
    get_top_negative
)

router = APIRouter()


@router.get("/keywords")
def keywords(platform: str):

    return get_keywords(platform)


@router.get("/overview")
def overview(
    platform: str,
    keyword: str = ""
):

    return get_overview(
        platform,
        keyword
    )


@router.get("/charts")
def charts(
    platform: str,
    keyword: str = ""
):

    return get_charts(
        platform,
        keyword
    )


@router.get("/content")
def content(
    platform: str,
    keyword: str = ""
):

    return get_content(
        platform,
        keyword
    )



@router.get("/top-content")
def top_content(
    platform: str,
    keyword: str = ""
):

    return get_top_content(
        platform,
        keyword
    )


@router.get("/top-positive")
def top_positive(
    platform: str,
    keyword: str = ""
):

    return get_top_positive(
        platform,
        keyword
    )


@router.get("/top-negative")
def top_negative(
    platform: str,
    keyword: str = ""
):

    return get_top_negative(
        platform,
        keyword
    )