import sys
import re
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent

if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

import pandas as pd
import tldextract
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
    "backend/storage/raw/googlenews/articles"
)

OUTPUT_FOLDER = Path(
    "backend/storage/cleaned/googlenews/articles"
)

# =====================================================
# SENTIMENT
# =====================================================

def get_sentiment_score(text):

    try:
        return round(
            TextBlob(str(text))
            .sentiment
            .polarity,
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
            TextBlob(str(text))
            .sentiment
            .subjectivity,
            4
        )

    except:
        return 0.0

# =====================================================
# KEYWORDS
# =====================================================

def count_keyword_mentions(
    text,
    keyword
):

    try:

        return str(text).lower().count(
            str(keyword).lower()
        )

    except:

        return 0


def calculate_keyword_density(
    frequency,
    word_count
):

    try:

        if word_count == 0:
            return 0

        return round(
            (frequency / word_count) * 100,
            2
        )

    except:

        return 0

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
# DOMAIN
# =====================================================

def get_domain(url):

    try:

        extracted = tldextract.extract(
            str(url)
        )

        return (
            extracted.domain
            + "."
            + extracted.suffix
        )

    except:

        return ""

# =====================================================
# BRANDS
# =====================================================

BRANDS = [
    "coca cola",
    "coca-cola",
    "sprite",
    "fanta",
    "maaza",
    "thumbs up",
    "pepsi",
    "mountain dew",
    "7up",
    "mirinda"
]


def extract_brand_mentions(text):

    found = []

    content = str(text).lower()

    for brand in BRANDS:

        if brand in content:
            found.append(
                brand
            )

    return ",".join(found)


def count_brands(text):

    count = 0

    content = str(text).lower()

    for brand in BRANDS:

        if brand in content:
            count += 1

    return count

# =====================================================
# QUALITY SCORE
# =====================================================

def content_quality_score(row):

    score = 0

    if len(
        str(row["clean_title"])
    ) > 20:
        score += 20

    if len(
        str(row["clean_description"])
    ) > 100:
        score += 30

    if row[
        "keyword_found_in_title"
    ]:
        score += 20

    if row[
        "keyword_found_in_description"
    ]:
        score += 20

    if str(
        row["url"]
    ).strip():
        score += 10

    return min(
        score,
        100
    )

# =====================================================
# RELEVANCE
# =====================================================

def relevance_score(row):

    score = (
        row[
            "keyword_found_in_title"
        ] * 40
        +
        row[
            "keyword_found_in_description"
        ] * 20
        +
        row[
            "keyword_frequency"
        ] * 5
    )

    return min(
        score,
        100
    )

# =====================================================
# MAIN
# =====================================================


def clean_google_news_file(
    input_file,
    output_file
):

    print("=" * 60)
    print("Google News Cleaner Started")
    print("=" * 60)

    print(
        f"Processing: {input_file.name}"
    )

    df = pd.read_csv(
        input_file
    )

    original_rows = len(df)

    df = safe_fillna(df)

    df = remove_duplicates(df)

    print(
        f"Original Rows: {original_rows}"
    )

    print(
        f"Rows After Cleaning: {len(df)}"
    )

    # ==========================================
    # CLEAN TEXT
    # ==========================================

    df["clean_title"] = (
        df["title"]
        .apply(clean_text)
    )

    df["clean_description"] = (
        df["description"]
        .apply(clean_text)
    )

    # ==========================================
    # WORD COUNTS
    # ==========================================

    df["title_word_count"] = (
        df["clean_title"]
        .apply(get_word_count)
    )

    df["description_word_count"] = (
        df["clean_description"]
        .apply(get_word_count)
    )

    # ==========================================
    # CHARACTER COUNTS
    # ==========================================

    df["title_char_count"] = (
        df["clean_title"]
        .str.len()
    )

    df["description_char_count"] = (
        df["clean_description"]
        .str.len()
    )

    # ==========================================
    # READ TIME
    # ==========================================

    df["estimated_read_time_min"] = (
        df["description_word_count"] / 200
    ).round(2)

    # ==========================================
    # SENTIMENT
    # ==========================================

    df["sentiment_score"] = (
        df["clean_description"]
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
        df["clean_description"]
        .apply(
            get_subjectivity_score
        )
    )

    # ==========================================
    # ARTICLE AGE
    # ==========================================

    published = pd.to_datetime(
        df["published_at"],
        errors="coerce"
    )

    age = (
        pd.Timestamp.now()
        - published
    )

    df["article_age_days"] = (
        age.dt.days
    )

    df["article_age_hours"] = (
        age.dt.total_seconds() / 3600
    ).round(2)

    # ==========================================
    # KEYWORD FLAGS
    # ==========================================

    df["keyword_found_in_title"] = (
        df.apply(
            lambda row:
            str(
                row["matched_keyword"]
            ).lower()
            in
            str(
                row["title"]
            ).lower(),
            axis=1
        )
    )

    df["keyword_found_in_description"] = (
        df.apply(
            lambda row:
            str(
                row["matched_keyword"]
            ).lower()
            in
            str(
                row["description"]
            ).lower(),
            axis=1
        )
    )

    # ==========================================
    # KEYWORD FREQUENCY
    # ==========================================

    df["keyword_frequency"] = (
        df.apply(
            lambda row:
            count_keyword_mentions(
                row["description"],
                row["matched_keyword"]
            ),
            axis=1
        )
    )

    df["keyword_density"] = (
        df.apply(
            lambda row:
            calculate_keyword_density(
                row[
                    "keyword_frequency"
                ],
                row[
                    "description_word_count"
                ]
            ),
            axis=1
        )
    )

    # ==========================================
    # MENTION STRENGTH
    # ==========================================

    df["mention_strength"] = (
        (
            df[
                "keyword_found_in_title"
            ].astype(int)
            * 5
        )
        +
        (
            df[
                "keyword_found_in_description"
            ].astype(int)
            * 2
        )
        +
        df[
            "keyword_frequency"
        ]
    )

    # ==========================================
    # RELEVANCE SCORE
    # ==========================================

    df["relevance_score"] = (
        df.apply(
            relevance_score,
            axis=1
        )
    )

    # ==========================================
    # HASHTAGS
    # ==========================================

    combined_text = (
        df["clean_title"]
        + " "
        + df["clean_description"]
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

    # ==========================================
    # MENTIONS
    # ==========================================

    df["mentions"] = (
        combined_text
        .apply(
            extract_mentions
        )
    )

    df["mention_count"] = (
        combined_text
        .apply(
            mention_count
        )
    )

    # ==========================================
    # DOMAIN
    # ==========================================

    df["domain"] = (
        df["url"]
        .apply(
            get_domain
        )
    )

    # ==========================================
    # BRANDS
    # ==========================================

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

    # ==========================================
    # QUALITY SCORE
    # ==========================================

    df["content_quality_score"] = (
        df.apply(
            content_quality_score,
            axis=1
        )
    )

    # ==========================================
    # SAVE
    # ==========================================

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_file,
        index=False
    )

    print("=" * 60)
    print("Google News Cleaning Complete")
    print("=" * 60)

    print(
        f"Output File: {output_file}"
    )

    print(
        f"Records: {len(df)}"
    )

    print(
        f"Columns: {len(df.columns)}"
    )

    print("=" * 60)

def process_google_news():
    
    print("=" * 60)
    print("Google News Folder Cleaner Started")
    print("=" * 60)

    OUTPUT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    files = list(
        RAW_FOLDER.glob("*.csv")
    )

    print(
        f"Files Found: {len(files)}"
    )

    for file in files:

        output_file = (
            OUTPUT_FOLDER
            / file.name
        )

        try:

            clean_google_news_file(
                file,
                output_file
            )

            print(
                f"Saved: {output_file.name}"
            )

        except Exception as e:

            print(
                f"Failed: {file.name}"
            )

            print(str(e))

    print("=" * 60)
    print("All Google News Files Cleaned")
    print("=" * 60)

    
if __name__ == "__main__":
    process_google_news()