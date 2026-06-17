# import sys
# from pathlib import Path

# CURRENT_DIR = Path(__file__).resolve().parent

# if str(CURRENT_DIR) not in sys.path:
#     sys.path.append(str(CURRENT_DIR))

# import pandas as pd
# from textblob import TextBlob

# from base_cleaner import (
#     safe_fillna,
#     remove_duplicates,
#     clean_text,
#     get_word_count
# )

# RAW_FILE = Path(
#     "backend/storage/raw/campaignindia/articles/Campaign_India_(CocaCola).csv"
# )

# OUTPUT_FILE = Path(
#     "backend/storage/cleaned/campaignindia/articles/Campaign_India_(CocaCola).csv"
# )


# # =========================================================
# # SENTIMENT
# # =========================================================

# def get_sentiment_score(text):

#     try:

#         return round(
#             TextBlob(
#                 str(text)
#             ).sentiment.polarity,
#             4
#         )

#     except:

#         return 0.0


# def get_sentiment_label(score):

#     if score > 0.1:
#         return "Positive"

#     elif score < -0.1:
#         return "Negative"

#     return "Neutral"


# # =========================================================
# # KEYWORD ANALYSIS
# # =========================================================

# def count_keyword_mentions(
#     text,
#     keyword
# ):

#     try:

#         return str(
#             text
#         ).lower().count(
#             str(
#                 keyword
#             ).lower()
#         )

#     except:

#         return 0


# # =========================================================
# # MAIN PROCESS
# # =========================================================

# def process_campaign_india():

#     print("=" * 60)
#     print("Loading Campaign India File")
#     print("=" * 60)

#     df = pd.read_csv(
#         RAW_FILE
#     )

#     original_rows = len(df)

#     df = safe_fillna(df)

#     df = remove_duplicates(df)

#     cleaned_rows = len(df)

#     print(
#         f"Original Rows: {original_rows}"
#     )

#     print(
#         f"Rows After Deduplication: {cleaned_rows}"
#     )

#     print(
#         "Creating Derived Fields..."
#     )

#     # =====================================================
#     # CLEAN TEXT
#     # =====================================================

#     df["clean_title"] = df[
#         "title"
#     ].apply(
#         clean_text
#     )

#     df["clean_content"] = df[
#         "content"
#     ].apply(
#         clean_text
#     )

#     # =====================================================
#     # WORD COUNTS
#     # =====================================================

#     df["title_word_count"] = df[
#         "clean_title"
#     ].apply(
#         get_word_count
#     )

#     df["content_word_count"] = df[
#         "clean_content"
#     ].apply(
#         get_word_count
#     )

#     # =====================================================
#     # CHARACTER COUNTS
#     # =====================================================

#     df["title_char_count"] = df[
#         "clean_title"
#     ].str.len()

#     df["content_char_count"] = df[
#         "clean_content"
#     ].str.len()

#     # =====================================================
#     # READING TIME
#     # =====================================================

#     df["estimated_read_time_min"] = (
#         df["content_word_count"] / 200
#     ).round(2)

#     # =====================================================
#     # SENTIMENT
#     # =====================================================

#     df["sentiment_score"] = df[
#         "clean_content"
#     ].apply(
#         get_sentiment_score
#     )

#     df["sentiment_label"] = df[
#         "sentiment_score"
#     ].apply(
#         get_sentiment_label
#     )

#     # =====================================================
#     # ARTICLE AGE
#     # =====================================================

#     df["article_age_days"] = (
#         pd.Timestamp.now()
#         -
#         pd.to_datetime(
#             df["published_at"],
#             errors="coerce"
#         )
#     ).dt.days

#     # =====================================================
#     # KEYWORD FOUND IN TITLE
#     # =====================================================

#     df["keyword_found_in_title"] = df.apply(
#         lambda row:
#         str(
#             row["matched_keyword"]
#         ).lower()
#         in
#         str(
#             row["title"]
#         ).lower(),
#         axis=1
#     )

#     # =====================================================
#     # KEYWORD FOUND IN CONTENT
#     # =====================================================

#     df["keyword_found_in_content"] = df.apply(
#         lambda row:
#         str(
#             row["matched_keyword"]
#         ).lower()
#         in
#         str(
#             row["content"]
#         ).lower(),
#         axis=1
#     )

#     # =====================================================
#     # KEYWORD FREQUENCY
#     # =====================================================

#     df["keyword_frequency"] = df.apply(
#         lambda row:
#         count_keyword_mentions(
#             row["content"],
#             row["matched_keyword"]
#         ),
#         axis=1
#     )

#     # =====================================================
#     # MENTION STRENGTH
#     # =====================================================

#     df["mention_strength"] = (
#         (
#             df[
#                 "keyword_found_in_title"
#             ].astype(int)
#             * 5
#         )
#         +
#         (
#             df[
#                 "keyword_found_in_content"
#             ].astype(int)
#             * 2
#         )
#         +
#         df[
#             "keyword_frequency"
#         ]
#     )

#     # =====================================================
#     # SAVE
#     # =====================================================

#     OUTPUT_FILE.parent.mkdir(
#         parents=True,
#         exist_ok=True
#     )

#     df.to_csv(
#         OUTPUT_FILE,
#         index=False
#     )

#     print("=" * 60)
#     print("Cleaning Complete")
#     print("=" * 60)

#     print(
#         f"Saved File: {OUTPUT_FILE}"
#     )

#     print(
#         f"Total Records: {len(df)}"
#     )

#     print(
#         f"Columns: {len(df.columns)}"
#     )

#     print("=" * 60)


# if __name__ == "__main__":

#     process_campaign_india()

























import sys
import re
from pathlib import Path
from urllib.parse import urlparse

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

RAW_FILE = Path(
    "backend/storage/raw/campaignindia/articles/Campaign_India_(CocaCola).csv"
)

OUTPUT_FILE = Path(
    "backend/storage/cleaned/campaignindia/articles/Campaign_India_(CocaCola).csv"
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
# KEYWORD ANALYSIS
# =====================================================

def count_keyword_mentions(text, keyword):

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

    content = str(text).lower()

    count = 0

    for brand in BRANDS:

        if brand in content:
            count += 1

    return count

# =====================================================
# CONTENT QUALITY
# =====================================================

def content_quality_score(row):

    score = 0

    if len(
        str(
            row["clean_title"]
        )
    ) > 20:
        score += 20

    if len(
        str(
            row["clean_content"]
        )
    ) > 300:
        score += 30

    if row[
        "keyword_found_in_title"
    ]:
        score += 20

    if row[
        "keyword_found_in_content"
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
            "keyword_found_in_content"
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

def process_campaign_india():

    print("=" * 60)
    print("Campaign India Cleaner Started")
    print("=" * 60)

    df = pd.read_csv(
        RAW_FILE
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

    df["clean_content"] = (
        df["content"]
        .apply(clean_text)
    )

    # ==========================================
    # WORD COUNTS
    # ==========================================

    df["title_word_count"] = (
        df["clean_title"]
        .apply(get_word_count)
    )

    df["content_word_count"] = (
        df["clean_content"]
        .apply(get_word_count)
    )

    # ==========================================
    # CHAR COUNTS
    # ==========================================

    df["title_char_count"] = (
        df["clean_title"]
        .str.len()
    )

    df["content_char_count"] = (
        df["clean_content"]
        .str.len()
    )

    # ==========================================
    # READ TIME
    # ==========================================

    df["estimated_read_time_min"] = (
        df["content_word_count"] / 200
    ).round(2)

    # ==========================================
    # SENTIMENT
    # ==========================================

    df["sentiment_score"] = (
        df["clean_content"]
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
        df["clean_content"]
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

    df["keyword_found_in_content"] = (
        df.apply(
            lambda row:
            str(
                row["matched_keyword"]
            ).lower()
            in
            str(
                row["content"]
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
                row["content"],
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
                    "content_word_count"
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
                "keyword_found_in_content"
            ].astype(int)
            * 2
        )
        +
        df[
            "keyword_frequency"
        ]
    )

    # ==========================================
    # RELEVANCE
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
        + df["clean_content"]
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

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("=" * 60)
    print("Cleaning Complete")
    print("=" * 60)

    print(
        f"Output File: {OUTPUT_FILE}"
    )

    print(
        f"Records: {len(df)}"
    )

    print(
        f"Columns: {len(df.columns)}"
    )

    print("=" * 60)


if __name__ == "__main__":
    process_campaign_india()