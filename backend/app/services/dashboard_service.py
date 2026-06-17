from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta


CLEANED_PATH = Path("storage/cleaned")
_DATA_CACHE = None
_CACHE_TIME = None

# def load_all_cleaned_data():

#     dfs = []

#     csv_files = list(CLEANED_PATH.rglob("*.csv"))

#     for file in csv_files:

#         try:

#             df = pd.read_csv(file)

#             df["source_file"] = file.name

#             dfs.append(df)

#         except Exception as e:

#             print(f"Failed: {file} -> {e}")

#     if not dfs:
#         return pd.DataFrame()

#     return pd.concat(
#         dfs,
#         ignore_index=True
#     )
def load_all_cleaned_data():
    
    global _DATA_CACHE
    global _CACHE_TIME

    if (
        _DATA_CACHE is not None
        and _CACHE_TIME is not None
        and datetime.now() - _CACHE_TIME
        < timedelta(minutes=5)
    ):
        return _DATA_CACHE

    dfs = []

    csv_files = list(
        CLEANED_PATH.rglob("*.csv")
    )

    for file in csv_files:

        try:

            df = pd.read_csv(file)

            df["source_file"] = file.name

            dfs.append(df)

        except Exception as e:

            print(
                f"Failed: {file} -> {e}"
            )

    if not dfs:

        return pd.DataFrame()

    _DATA_CACHE = pd.concat(
        dfs,
        ignore_index=True
    )

    _CACHE_TIME = datetime.now()

    return _DATA_CACHE

def apply_filters(
    df,
    platform=None,
    brand=None,
    sentiment=None,
    keyword=None
):

    if platform and "platform" in df.columns:

        df = df[
            df["platform"]
            .astype(str)
            .str.lower()
            == platform.lower()
        ]

    if sentiment:

        sentiment_col = None

        for col in [
            "sentiment_label",
            "sentiment"
        ]:

            if col in df.columns:

                sentiment_col = col

                break

        if sentiment_col:

            df = df[
                df[sentiment_col]
                .astype(str)
                .str.lower()
                == sentiment.lower()
            ]

    if brand:

        brand_cols = [
            "brand_mentions",
            "matched_keyword",
            "keyword",
            "input_keyword"
        ]

        mask = None

        for col in brand_cols:

            if col in df.columns:

                current_mask = (
                    df[col]
                    .astype(str)
                    .str.contains(
                        brand,
                        case=False,
                        na=False
                    )
                )

                if mask is None:

                    mask = current_mask

                else:

                    mask = mask | current_mask

        if mask is not None:

            df = df[mask]

    if keyword:

        search_cols = [
            "title",
            "content",
            "caption",
            "comment_text",
            "review_text"
        ]

        mask = None

        for col in search_cols:

            if col in df.columns:

                current_mask = (
                    df[col]
                    .astype(str)
                    .str.contains(
                        keyword,
                        case=False,
                        na=False
                    )
                )

                if mask is None:

                    mask = current_mask

                else:

                    mask = mask | current_mask

        if mask is not None:

            df = df[mask]

    return df



def get_dashboard_summary(
    platform=None,
    brand=None,
    sentiment=None,
    keyword=None
):

    df = load_all_cleaned_data()

    if df.empty:

        return {
            "total_records": 0,
            "total_platforms": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 0
        }

    df = apply_filters(
        df,
        platform,
        brand,
        sentiment,
        keyword
    )

    sentiment_col = None

    for col in [
        "sentiment_label",
        "sentiment"
    ]:

        if col in df.columns:

            sentiment_col = col

            break

    positive = 0
    negative = 0
    neutral = 0

    if sentiment_col:

        positive = len(
            df[
                df[sentiment_col]
                .astype(str)
                .str.lower()
                == "positive"
            ]
        )

        negative = len(
            df[
                df[sentiment_col]
                .astype(str)
                .str.lower()
                == "negative"
            ]
        )

        neutral = len(
            df[
                df[sentiment_col]
                .astype(str)
                .str.lower()
                == "neutral"
            ]
        )

    return {

        "total_records": int(len(df)),

        "total_platforms": int(
            df["platform"].nunique()
        )
        if "platform" in df.columns
        else 0,

        "positive": positive,

        "negative": negative,

        "neutral": neutral
    }
# def get_dashboard_summary():

#     df = load_all_cleaned_data()

#     if df.empty:

#         return {
#             "total_records": 0,
#             "total_platforms": 0,
#             "positive": 0,
#             "negative": 0,
#             "neutral": 0
#         }

#     sentiment_col = None

#     for col in [
#         "sentiment_label",
#         "sentiment"
#     ]:

#         if col in df.columns:
#             sentiment_col = col
#             break

#     positive = 0
#     negative = 0
#     neutral = 0

#     if sentiment_col:

#         positive = len(
#             df[
#                 df[sentiment_col]
#                 .astype(str)
#                 .str.lower()
#                 == "positive"
#             ]
#         )

#         negative = len(
#             df[
#                 df[sentiment_col]
#                 .astype(str)
#                 .str.lower()
#                 == "negative"
#             ]
#         )

#         neutral = len(
#             df[
#                 df[sentiment_col]
#                 .astype(str)
#                 .str.lower()
#                 == "neutral"
#             ]
#         )

#     return {

#         "total_records": int(len(df)),

#         "total_platforms": int(
#             df["platform"].nunique()
#         )
#         if "platform" in df.columns
#         else 0,

#         "positive": positive,

#         "negative": negative,

#         "neutral": neutral
#     }


# def get_platform_distribution():

#     df = load_all_cleaned_data()

#     if df.empty:
#         return []

#     if "platform" not in df.columns:
#         return []

#     result = (
#         df["platform"]
#         .value_counts()
#         .reset_index()
#     )

#     result.columns = [
#         "platform",
#         "count"
#     ]

#     return result.to_dict(
#         orient="records"
#     )
def get_platform_distribution(
    platform=None,
    brand=None,
    sentiment=None,
    keyword=None
):

    df = load_all_cleaned_data()

    if df.empty:
        return []

    df = apply_filters(
        df,
        platform,
        brand,
        sentiment,
        keyword
    )

    if "platform" not in df.columns:
        return []

    result = (
        df["platform"]
        .value_counts()
        .reset_index()
    )

    result.columns = [
        "platform",
        "count"
    ]

    return result.to_dict(
        orient="records"
    )

def get_sentiment_distribution(
    platform=None,
    brand=None,
    sentiment=None,
    keyword=None
):

    df = load_all_cleaned_data()

    if df.empty:
        return []

    sentiment_col = None

    for col in [
        "sentiment_label",
        "sentiment"
    ]:

        if col in df.columns:
            sentiment_col = col
            break

    if not sentiment_col:
        return []

    result = (
        df[sentiment_col]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    result.columns = [
        "sentiment",
        "count"
    ]

    return result.to_dict(
        orient="records"
    )


def get_latest_records(limit=50):

    df = load_all_cleaned_data()

    if df.empty:
        return []

    return (
        df.head(limit)
        .fillna("")
        .to_dict(
            orient="records"
        )
    )


def get_brand_distribution():
    
    df = load_all_cleaned_data()

    if df.empty:
        return []

    brand_cols = [
        "brand_mentions",
        "matched_keyword",
        "keyword",
        "input_keyword"
    ]

    brands = []

    for col in brand_cols:

        if col in df.columns:

            brands.extend(
                df[col]
                .dropna()
                .astype(str)
                .tolist()
            )

    if not brands:
        return []

    brand_df = pd.Series(brands)

    result = (
        brand_df
        .value_counts()
        .head(20)
        .reset_index()
    )

    result.columns = [
        "brand",
        "count"
    ]

    return result.to_dict(
        orient="records"
    )


def get_hashtag_distribution():
    
    df = load_all_cleaned_data()

    if df.empty:
        return []

    hashtags = []

    for col in [
        "hashtags",
        "derived_hashtags"
    ]:

        if col in df.columns:

            for value in df[col].dropna():

                hashtags.extend(
                    str(value).split(",")
                )

    if not hashtags:
        return []

    result = (
        pd.Series(hashtags)
        .str.strip()
        .value_counts()
        .head(20)
        .reset_index()
    )

    result.columns = [
        "hashtag",
        "count"
    ]

    return result.to_dict(
        orient="records"
    )

def get_top_youtube_videos():
    
    df = load_all_cleaned_data()

    if df.empty:
        return []

    if "video_title" not in df.columns:
        return []

    result = (
        df[
            df["platform"] == "youtube"
        ]
        .sort_values(
            "view_count_numeric",
            ascending=False
        )
        .head(20)
    )

    cols = [
        "video_title",
        "channel_name",
        "view_count_numeric",
        "like_count_numeric",
        "comment_count_numeric",
        "viral_score"
    ]

    cols = [
        c for c in cols
        if c in result.columns
    ]

    return (
        result[cols]
        .fillna("")
        .to_dict(
            orient="records"
        )
    )



def get_top_instagram_posts():
    
    df = load_all_cleaned_data()

    if df.empty:
        return []

    if "engagement" not in df.columns:
        return []

    result = (
        df
        .sort_values(
            "engagement",
            ascending=False
        )
        .head(20)
    )

    cols = [
        "caption",
        "engagement",
        "engagement_rate",
        "like_count",
        "comments_count"
    ]

    cols = [
        c for c in cols
        if c in result.columns
    ]

    return (
        result[cols]
        .fillna("")
        .to_dict(
            orient="records"
        )
    )


def get_top_negative_mentions():
    
    df = load_all_cleaned_data()

    if df.empty:
        return []

    sentiment_col = None

    for col in [
        "sentiment_label",
        "sentiment"
    ]:

        if col in df.columns:
            sentiment_col = col
            break

    if not sentiment_col:
        return []

    negative = df[
        df[sentiment_col]
        .astype(str)
        .str.lower()
        == "negative"
    ]

    return (
        negative
        .head(50)
        .fillna("")
        .to_dict(
            orient="records"
        )
    )


def get_top_positive_mentions():
    
    df = load_all_cleaned_data()

    if df.empty:
        return []

    sentiment_col = None

    for col in [
        "sentiment_label",
        "sentiment"
    ]:

        if col in df.columns:
            sentiment_col = col
            break

    if not sentiment_col:
        return []

    positive = df[
        df[sentiment_col]
        .astype(str)
        .str.lower()
        == "positive"
    ]

    return (
        positive
        .head(50)
        .fillna("")
        .to_dict(
            orient="records"
        )
    )


from collections import Counter
import re


def get_keyword_distribution():

    df = load_all_cleaned_data()

    if df.empty:
        return []

    text_cols = [
        "title",
        "content",
        "caption",
        "comment_text",
        "review_text"
    ]

    text = ""

    for col in text_cols:

        if col in df.columns:

            text += " ".join(
                df[col]
                .dropna()
                .astype(str)
                .tolist()
            )

    words = re.findall(
        r"\b[a-zA-Z]{4,}\b",
        text.lower()
    )

    common = Counter(words).most_common(20)

    return [

        {
            "keyword": k,
            "count": v
        }

        for k, v in common

    ]




def get_dashboard_overview():
    
    return {

        "summary":
            get_dashboard_summary(),

        "platforms":
            get_platform_distribution(),

        "sentiment":
            get_sentiment_distribution(),

        "brands":
            get_brand_distribution(),

        "hashtags":
            get_hashtag_distribution(),

        "keywords":
            get_keyword_distribution(),

        "top_youtube":
            get_top_youtube_videos(),

        "top_instagram":
            get_top_instagram_posts(),

        "top_positive":
            get_top_positive_mentions(),

        "top_negative":
            get_top_negative_mentions(),

        "latest":
            get_latest_records()

    }


def get_filter_options():
    
    df = load_all_cleaned_data()

    if df.empty:

        return {
            "platforms": [],
            "sentiments": [],
            "brands": []
        }

    platforms = []

    if "platform" in df.columns:

        platforms = sorted(
            df["platform"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    sentiments = []

    sentiment_col = None

    for col in [
        "sentiment_label",
        "sentiment"
    ]:

        if col in df.columns:

            sentiment_col = col

            break

    if sentiment_col:

        sentiments = sorted(
            df[sentiment_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

    brands = []

    for col in [
        "brand_mentions",
        "matched_keyword",
        "keyword",
        "input_keyword"
    ]:

        if col in df.columns:

            brands.extend(
                df[col]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

    brands = sorted(
        list(set(brands))
    )

    return {
        "platforms": platforms,
        "sentiments": sentiments,
        "brands": brands
    }