



from fastapi import APIRouter

from app.services.dashboard_service import (
    get_dashboard_summary,
    get_platform_distribution,
    get_sentiment_distribution,
    get_latest_records,
    get_brand_distribution,
    get_hashtag_distribution,
    get_keyword_distribution,
    get_top_youtube_videos,
    get_top_instagram_posts,
    get_top_positive_mentions,
    get_top_negative_mentions,
    get_dashboard_overview,
    get_filter_options
)

router = APIRouter()


# ==================================================
# SUMMARY
# ==================================================

# @router.get("/summary")
# def dashboard_summary():

#     return get_dashboard_summary()


from fastapi import Query


@router.get("/summary")
def dashboard_summary(
    platform: str | None = Query(None),
    brand: str | None = Query(None),
    sentiment: str | None = Query(None),
    keyword: str | None = Query(None)
):

    return get_dashboard_summary(
        platform,
        brand,
        sentiment,
        keyword
    )
# ==================================================
# PLATFORM DISTRIBUTION
# ==================================================

# @router.get("/platforms")
# def platform_distribution():

#     return get_platform_distribution()
@router.get("/platforms")
def platform_distribution(
    platform: str | None = Query(None),
    brand: str | None = Query(None),
    sentiment: str | None = Query(None),
    keyword: str | None = Query(None)
):

    return get_platform_distribution(
        platform,
        brand,
        sentiment,
        keyword
    )

# ==================================================
# SENTIMENT DISTRIBUTION
# ==================================================

# @router.get("/sentiment")
# def sentiment_distribution():

#     return get_sentiment_distribution()
@router.get("/sentiment")
def sentiment_distribution(
    platform: str | None = Query(None),
    brand: str | None = Query(None),
    sentiment: str | None = Query(None),
    keyword: str | None = Query(None)
):

    return get_sentiment_distribution(
        platform,
        brand,
        sentiment,
        keyword
    )

# ==================================================
# LATEST RECORDS
# ==================================================

@router.get("/latest")
def latest_records():

    return get_latest_records()


@router.get("/filter-options")
def filter_options():

    return get_filter_options()
# ==================================================
# BRAND DISTRIBUTION
# ==================================================

@router.get("/brands")
def brand_distribution():

    return get_brand_distribution()


# ==================================================
# HASHTAG DISTRIBUTION
# ==================================================

@router.get("/hashtags")
def hashtag_distribution():

    return get_hashtag_distribution()


# ==================================================
# KEYWORD DISTRIBUTION
# ==================================================

@router.get("/keywords")
def keyword_distribution():

    return get_keyword_distribution()


# ==================================================
# TOP YOUTUBE VIDEOS
# ==================================================

@router.get("/top-youtube")
def top_youtube_videos():

    return get_top_youtube_videos()


# ==================================================
# TOP INSTAGRAM POSTS
# ==================================================

@router.get("/top-instagram")
def top_instagram_posts():

    return get_top_instagram_posts()


# ==================================================
# TOP POSITIVE MENTIONS
# ==================================================

@router.get("/top-positive")
def top_positive_mentions():

    return get_top_positive_mentions()


# ==================================================
# TOP NEGATIVE MENTIONS
# ==================================================

@router.get("/top-negative")
def top_negative_mentions():

    return get_top_negative_mentions()



@router.get("/overview")
def dashboard_overview():

    return get_dashboard_overview()