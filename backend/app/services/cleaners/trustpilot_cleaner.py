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
    "backend/storage/raw/rss_reviews/reviews"
)

OUTPUT_FOLDER = Path(
    "backend/storage/cleaned/rss_reviews/reviews"
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
# BRANDS
# =====================================================

BRANDS = [
    "coca cola",
    "coca-cola",
    "coke",
    "sprite",
    "fanta",
    "pepsi",
    "7up",
    "mountain dew",
    "mirinda"
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
# RATING
# =====================================================

def get_rating_bucket(rating):

    try:

        rating = float(rating)

        if rating <= 2:
            return "Negative"

        elif rating == 3:
            return "Neutral"

        return "Positive"

    except:

        return "Unknown"

# =====================================================
# QUALITY
# =====================================================

def quality_score(row):

    score = 0

    if row["review_word_count"] > 20:
        score += 40

    if pd.notna(row["rating"]):
        score += 20

    if row["brand_count"] > 0:
        score += 20

    if row["sentiment_label"]:
        score += 20

    return min(score, 100)

# =====================================================
# URGENCY
# =====================================================

def urgency_score(row):

    score = 0

    try:

        if float(row["rating"]) <= 2:
            score += 50

    except:
        pass

    if row["sentiment_label"] == "Negative":
        score += 30

    if row["review_word_count"] > 50:
        score += 20

    return min(score, 100)

# =====================================================
# CLEAN FILE
# =====================================================

def clean_trustpilot_file(
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

    df["combined_review"] = (
        df["review_title"].astype(str)
        + " "
        + df["review_text"].astype(str)
    )

    df["clean_review"] = (
        df["combined_review"]
        .apply(clean_text)
    )

    df["review_word_count"] = (
        df["clean_review"]
        .apply(get_word_count)
    )

    df["review_char_count"] = (
        df["clean_review"]
        .str.len()
    )

    df["title_word_count"] = (
        df["review_title"]
        .astype(str)
        .apply(get_word_count)
    )

    df["title_char_count"] = (
        df["review_title"]
        .astype(str)
        .str.len()
    )

    df["sentiment_score"] = (
        df["clean_review"]
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
        df["clean_review"]
        .apply(
            get_subjectivity_score
        )
    )

    df["rating_bucket"] = (
        df["rating"]
        .apply(
            get_rating_bucket
        )
    )

    # =====================================================
        # =====================================================
    # DATE PROCESSING
    # =====================================================

    df["published_date_clean"] = (
        df["published_date"]
        .astype(str)
        .str.extract(
            r"(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
            expand=False
        )
    )

    # print("\nExtracted Dates:")
    # print(
    #     df[
    #         [
    #             "published_date",
    #             "published_date_clean"
    #         ]
    #     ]
    # )

    published = pd.to_datetime(
        df["published_date_clean"],
        format="%d %b %Y",
        errors="coerce",
        utc=True
    )

    print(
        f"\nFailed date parses: {published.isna().sum()}"
    )

    if published.isna().any():

        print("\nFailed values:")

        print(
            df.loc[
                published.isna(),
                [
                    "published_date",
                    "published_date_clean"
                ]
            ]
        )

    current_time = pd.Timestamp.now(
        tz="UTC"
    )

    age = current_time - published

    df["review_age_days"] = (
        age.dt.days
    )

    df["review_age_hours"] = (
        age.dt.total_seconds()
        .div(3600)
        .round(2)
    )

    # print(
    #     df[
    #         [
    #             "published_date",
    #             "published_date_clean",
    #             "review_age_days",
    #             "review_age_hours"
    #         ]
    #     ]
    # )

    current_time = pd.Timestamp.now(
        tz="UTC"
    )

    age = (
        current_time
        - published
    )


    # print(age)

    df["review_age_days"] = (
        age.dt.days
    )

    df["review_age_hours"] = (
        age.dt.total_seconds()
        / 3600
    ).round(2)

    df["brand_mentions"] = (
        df["clean_review"]
        .apply(
            extract_brand_mentions
        )
    )

    df["brand_count"] = (
        df["clean_review"]
        .apply(
            count_brands
        )
    )

    df["quality_score"] = (
        df.apply(
            quality_score,
            axis=1
        )
    )

    df["urgency_score"] = (
        df.apply(
            urgency_score,
            axis=1
        )
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )
    print(
        df[
            [
                "published_date",
                "review_age_days",
                "review_age_hours"
            ]
        ]
    )

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"Saved: {output_file.name}"
    )

# =====================================================
# RUN
# =====================================================

def process_trustpilot():

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

            clean_trustpilot_file(
                file,
                output_file
            )

        except Exception as e:

            print(
                f"Failed: {file.name}"
            )

            print(str(e))


if __name__ == "__main__":

    process_trustpilot()
















