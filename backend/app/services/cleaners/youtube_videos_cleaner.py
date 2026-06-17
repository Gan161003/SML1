import sys
import re
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent

if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

import pandas as pd
from textblob import TextBlob

from base_cleaner import (
    safe_fillna,
    remove_duplicates,
    clean_text,
    get_word_count
)

# =====================================================
# CONFIG
# =====================================================

RAW_FOLDER = Path(
    "backend/storage/raw/youtube/videos"
)

OUTPUT_FOLDER = Path(
    "backend/storage/cleaned/youtube/videos"
)

# =====================================================
# SENTIMENT
# =====================================================

def get_sentiment_score(text):

    try:

        return round(
            TextBlob(
                str(text)
            ).sentiment.polarity,
            4
        )

    except:

        return 0.0


def get_sentiment_label(score):

    if score > 0.1:
        return "Positive"

    elif score < -0.1:
        return "Negative"

    return "Neutral"


# =====================================================
# HASHTAGS
# =====================================================

def extract_hashtags(text):

    try:

        tags = re.findall(
            r"#(\w+)",
            str(text)
        )

        return ",".join(
            list(set(tags))
        )

    except:

        return ""


def hashtag_count(text):

    try:

        return len(
            re.findall(
                r"#(\w+)",
                str(text)
            )
        )

    except:

        return 0


# =====================================================
# BRANDS
# =====================================================

BRANDS = [
    "coca cola",
    "coca-cola",
    "coke",
    "pepsi",
    "sprite",
    "fanta",
    "mirinda",
    "7up",
    "mountain dew"
]


def extract_brand_mentions(text):

    found = []

    text = str(text).lower()

    for brand in BRANDS:

        if brand in text:

            found.append(
                brand
            )

    return ",".join(found)


def count_brands(text):

    count = 0

    text = str(text).lower()

    for brand in BRANDS:

        if brand in text:

            count += 1

    return count


# =====================================================
# CONTENT TYPE
# =====================================================

def get_content_type(title):

    title = str(title).lower()

    if "#shorts" in title:

        return "Short"

    if "shorts" in title:

        return "Short"

    return "Video"


# =====================================================
# VIRAL SCORE
# =====================================================

def calculate_viral_score(row):

    views = row["view_count_numeric"]
    likes = row["like_count_numeric"]
    comments = row["comment_count_numeric"]

    score = 0

    if views > 1000000:
        score += 40

    elif views > 100000:
        score += 25

    elif views > 10000:
        score += 15

    if likes > 10000:
        score += 30

    elif likes > 1000:
        score += 20

    if comments > 1000:
        score += 30

    elif comments > 100:
        score += 15

    return min(score, 100)


# =====================================================
# ENGAGEMENT RATE
# =====================================================

def calculate_engagement_rate(row):

    views = row["view_count_numeric"]

    if views == 0:

        return 0

    engagement = (
        row["like_count_numeric"]
        +
        row["comment_count_numeric"]
    )

    return round(
        (engagement / views) * 100,
        4
    )


# =====================================================
# QUALITY SCORE
# =====================================================

def calculate_quality_score(row):

    score = 0

    if row["title_word_count"] > 5:
        score += 25

    if row["description_word_count"] > 20:
        score += 25

    if row["hashtag_count"] > 0:
        score += 20

    if row["brand_count"] > 0:
        score += 15

    if row["engagement_rate"] > 1:
        score += 15

    return min(score, 100)


# =====================================================
# FILE CLEANER
# =====================================================

def clean_youtube_video_file(
    input_file,
    output_file
):

    print(
        f"Processing: {input_file.name}"
    )

    df = pd.read_csv(
        input_file
    )

    df = safe_fillna(df)

    df = remove_duplicates(df)

    # =====================================
    # CLEAN TITLE
    # =====================================

    df["clean_video_title"] = (
        df["video_title"]
        .astype(str)
        .apply(clean_text)
    )

    df["title_word_count"] = (
        df["clean_video_title"]
        .apply(get_word_count)
    )

    df["title_char_count"] = (
        df["clean_video_title"]
        .str.len()
    )

    # =====================================
    # CLEAN DESCRIPTION
    # =====================================

    df["clean_video_description"] = (
        df["video_description"]
        .astype(str)
        .apply(clean_text)
    )

    df["description_word_count"] = (
        df["clean_video_description"]
        .apply(get_word_count)
    )

    df["description_char_count"] = (
        df["clean_video_description"]
        .str.len()
    )

    # =====================================
    # SENTIMENT
    # =====================================

    df["sentiment_score"] = (
        df["clean_video_title"]
        .apply(
            get_sentiment_score
        )
    )

    df["sentiment_label"] = (
        df["sentiment_score"]
        .apply(
            get_sentiment_label
        )
    )

    # =====================================
    # VIDEO AGE
    # =====================================

    publish_date = pd.to_datetime(
        df["published_at"],
        utc=True,
        errors="coerce"
    )

    current_time = pd.Timestamp.now(
        tz="UTC"
    )

    age = (
        current_time
        - publish_date
    )

    df["video_age_days"] = (
        age.dt.days
    )

    df["video_age_hours"] = (
        age.dt.total_seconds()
        / 3600
    ).round(2)

    # =====================================
    # NUMERIC METRICS
    # =====================================

    numeric_columns = [
        "view_count",
        "like_count",
        "favorite_count",
        "comment_count"
    ]

    for col in numeric_columns:

        df[f"{col}_numeric"] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)

    # =====================================
    # HASHTAGS
    # =====================================

    combined_text = (
        df["video_title"]
        .astype(str)
        +
        " "
        +
        df["video_description"]
        .astype(str)
    )

    df["hashtags"] = (
        combined_text
        .apply(
            extract_hashtags
        )
    )

    df["hashtag_count"] = (
        combined_text
        .apply(
            hashtag_count
        )
    )

    # =====================================
    # BRANDS
    # =====================================

    df["brand_mentions"] = (
        combined_text
        .apply(
            extract_brand_mentions
        )
    )

    df["brand_count"] = (
        combined_text
        .apply(
            count_brands
        )
    )

    # =====================================
    # CONTENT TYPE
    # =====================================

    df["content_type"] = (
        df["video_title"]
        .apply(
            get_content_type
        )
    )

    # =====================================
    # ENGAGEMENT
    # =====================================

    df["total_engagement"] = (
        df["like_count_numeric"]
        +
        df["comment_count_numeric"]
    )

    df["engagement_rate"] = (
        df.apply(
            calculate_engagement_rate,
            axis=1
        )
    )

    # =====================================
    # VIRAL SCORE
    # =====================================

    df["viral_score"] = (
        df.apply(
            calculate_viral_score,
            axis=1
        )
    )

    # =====================================
    # QUALITY SCORE
    # =====================================

    df["quality_score"] = (
        df.apply(
            calculate_quality_score,
            axis=1
        )
    )

    # =====================================
    # PERFORMANCE BUCKET
    # =====================================

    df["performance_bucket"] = pd.cut(
        df["viral_score"],
        bins=[
            -1,
            25,
            50,
            75,
            100
        ],
        labels=[
            "Low",
            "Medium",
            "High",
            "Viral"
        ]
    )

    # =====================================
    # SAVE
    # =====================================

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"Saved: {output_file.name}"
    )


# =====================================================
# RUN ALL FILES
# =====================================================

def process_youtube_videos():

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    files = list(
        RAW_FOLDER.glob(
            "*.csv"
        )
    )

    print(
        f"Files Found: {len(files)}"
    )

    for file in files:

        try:

            output_file = (
                OUTPUT_FOLDER
                / file.name
            )

            clean_youtube_video_file(
                file,
                output_file
            )

        except Exception as e:

            print(
                f"Failed: {file.name}"
            )

            print(str(e))


if __name__ == "__main__":

    process_youtube_videos()