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
    "backend/storage/raw/instagram_account/account_data"
)

OUTPUT_FOLDER = Path(
    "backend/storage/cleaned/instagram_account/account_data"
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
# ENGAGEMENT
# =====================================================

def calculate_engagement(row):
    
    likes = pd.to_numeric(
        row["like_count"],
        errors="coerce"
    )

    comments = pd.to_numeric(
        row["comments_count"],
        errors="coerce"
    )

    likes = 0 if pd.isna(likes) else likes
    comments = 0 if pd.isna(comments) else comments

    return likes + comments

def calculate_engagement_rate(row):

    try:

        followers = float(
            row["followers_count"]
        )

        if followers == 0:
            return 0

        engagement = (
            float(row["like_count"])
            +
            float(row["comments_count"])
        )

        return round(
            (engagement / followers)
            * 100,
            2
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
        score += 20

    if row["has_mentions"]:
        score += 20

    likes = pd.to_numeric(
        row["like_count"],
        errors="coerce"
    )

    comments = pd.to_numeric(
        row["comments_count"],
        errors="coerce"
    )

    if pd.notna(likes) and likes > 0:
        score += 15

    if pd.notna(comments) and comments > 0:
        score += 15

    return min(score, 100)


# =====================================================
# FILE CLEANER
# =====================================================

def clean_instagram_account_file(
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
    # SAFE COLUMN CREATION
    # =====================================

    if "comment_text" not in df.columns:
        df["comment_text"] = ""

    if "comment_timestamp" not in df.columns:
        df["comment_timestamp"] = ""

    if "comment_id" not in df.columns:
        df["comment_id"] = ""

    # Numeric conversions

    for col in [
        "followers_count",
        "follows_count",
        "media_count",
        "like_count",
        "comments_count"
    ]:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

    # =====================================
    # CAPTION CLEANING
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
    id_columns = [
        "post_id",
        "comment_id"
    ]

    for col in id_columns:

        if col in df.columns:

            df[col] = (
                df[col]
                .fillna("")
                .astype(str)
                .str.replace(
                    ".0",
                    "",
                    regex=False
                )
                .str.lstrip("'")
                .str.strip()
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
        df["post_timestamp"],
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
    df["post_age_weeks"] = (
        df["post_age_days"] / 7
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
        df.apply(
            calculate_engagement,
            axis=1
        )
    )

    df["engagement_rate"] = (
        df.apply(
            calculate_engagement_rate,
            axis=1
        )
    )

    # =====================================
    # COMMENT DATA
    # =====================================

    df["clean_comment"] = (
        df["comment_text"]
        .astype(str)
        .apply(clean_text)
    )

    df["comment_word_count"] = (
        df["clean_comment"]
        .apply(get_word_count)
    )

    df["comment_sentiment_score"] = (
        df["clean_comment"]
        .apply(
            get_sentiment_score
        )
    )

    df["comment_sentiment_label"] = (
        df["comment_sentiment_score"]
        .apply(
            get_sentiment_label
        )
    )

    # =====================================
    # COMMENT AGE
    # =====================================

    comment_date = pd.to_datetime(
        df["comment_timestamp"],
        utc=True,
        errors="coerce"
    )

    comment_age = (
        current_time
        - comment_date
    )

    df["comment_age_days"] = (
        comment_age.dt.days
    )

    df["comment_age_hours"] = (
        comment_age.dt.total_seconds()
        / 3600
    ).round(2)

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
    # ACCOUNT METRICS
    # =====================================

    followers = pd.to_numeric(
        df["followers_count"],
        errors="coerce"
    )

    follows = pd.to_numeric(
        df["follows_count"],
        errors="coerce"
    )

    followers = followers.mask(
        followers == 0
    )

    df["following_ratio"] = (
        follows / followers
    ).round(4)

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

def process_instagram_account():

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

            clean_instagram_account_file(
                file,
                output_file
            )

        except Exception as e:

            print(
                f"Failed: {file.name}"
            )

            print(str(e))


if __name__ == "__main__":

    process_instagram_account()