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
    "backend/storage/raw/instagram_hashtag/posts"
)

OUTPUT_FOLDER = Path(
    "backend/storage/cleaned/instagram_hashtag/posts"
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


def get_subjectivity_score(text):

    try:
        return round(
            TextBlob(
                str(text)
            ).sentiment.subjectivity,
            4
        )

    except:
        return 0.0

# =====================================================
# HASHTAGS
# =====================================================

def extract_hashtags(text):

    try:

        hashtags = re.findall(
            r"#(\w+)",
            str(text)
        )

        return ",".join(
            list(set(hashtags))
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
# MENTIONS
# =====================================================

def extract_mentions(text):

    try:

        mentions = re.findall(
            r"@(\w+)",
            str(text)
        )

        return ",".join(
            list(set(mentions))
        )

    except:

        return ""


def mention_count(text):

    try:

        return len(
            re.findall(
                r"@(\w+)",
                str(text)
            )
        )

    except:

        return 0

# =====================================================
# QUALITY SCORE
# =====================================================

def content_quality_score(row):

    score = 0

    if row["caption_word_count"] > 10:
        score += 30

    if row["has_hashtags"]:
        score += 30

    if row["has_mentions"]:
        score += 20

    if row["like_count"] > 0:
        score += 10

    if row["comments_count"] > 0:
        score += 10

    return min(score, 100)

# =====================================================
# CLEAN FILE
# =====================================================

def clean_instagram_hashtag_file(
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
    # CLEAN IDS
    # =====================================

    if "post_id" in df.columns:

        df["post_id"] = (
            df["post_id"]
            .astype(str)
            .str.lstrip("'")
        )

    # =====================================
    # NUMERIC FIELDS
    # =====================================

    numeric_cols = [
        "like_count",
        "comments_count"
    ]

    for col in numeric_cols:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

    # =====================================
    # CAPTION
    # =====================================

    df["clean_caption"] = (
        df["caption"]
        .astype(str)
        .apply(clean_text)
    )

    df["caption_word_count"] = (
        df["clean_caption"]
        .apply(get_word_count)
    )

    df["caption_char_count"] = (
        df["clean_caption"]
        .str.len()
    )

    # =====================================
    # SENTIMENT
    # =====================================

    df["sentiment_score"] = (
        df["clean_caption"]
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

    df["subjectivity_score"] = (
        df["clean_caption"]
        .apply(
            get_subjectivity_score
        )
    )

    # =====================================
    # HASHTAGS
    # =====================================

    df["derived_hashtags"] = (
        df["clean_caption"]
        .apply(
            extract_hashtags
        )
    )

    df["derived_hashtag_count"] = (
        df["clean_caption"]
        .apply(
            hashtag_count
        )
    )

    # =====================================
    # MENTIONS
    # =====================================

    df["derived_mentions"] = (
        df["clean_caption"]
        .apply(
            extract_mentions
        )
    )

    df["derived_mention_count"] = (
        df["clean_caption"]
        .apply(
            mention_count
        )
    )

    # =====================================
    # POST AGE
    # =====================================

    post_date = pd.to_datetime(
        df["timestamp"],
        utc=True,
        errors="coerce"
    )

    current_time = pd.Timestamp.now(
        tz="UTC"
    )

    age = (
        current_time
        - post_date
    )

    df["post_age_days"] = (
        age.dt.days
    )

    df["post_age_hours"] = (
        age.dt.total_seconds()
        / 3600
    ).round(2)

    # =====================================
    # FLAGS
    # =====================================

    df["has_caption"] = (
        df["caption"]
        .astype(str)
        .str.strip()
        != ""
    )

    df["has_hashtags"] = (
        df["derived_hashtag_count"]
        > 0
    )

    df["has_mentions"] = (
        df["derived_mention_count"]
        > 0
    )

    # =====================================
    # ENGAGEMENT
    # =====================================

    df["engagement"] = (
        df["like_count"]
        +
        df["comments_count"]
    )

    # =====================================
    # CONTENT TYPE FLAGS
    # =====================================

    df["is_image"] = (
        df["media_type"]
        .astype(str)
        .str.upper()
        == "IMAGE"
    )

    df["is_video"] = (
        df["media_type"]
        .astype(str)
        .str.upper()
        == "VIDEO"
    )

    # =====================================
    # QUALITY SCORE
    # =====================================

    df["content_quality_score"] = (
        df.apply(
            content_quality_score,
            axis=1
        )
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

def process_instagram_hashtag():

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

            clean_instagram_hashtag_file(
                file,
                output_file
            )

        except Exception as e:

            print(
                f"Failed: {file.name}"
            )

            print(str(e))


if __name__ == "__main__":

    process_instagram_hashtag()