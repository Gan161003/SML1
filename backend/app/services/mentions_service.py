from app.services.dashboard_service import load_all_cleaned_data
import pandas as pd


# =====================================================
# PLATFORM FILTER
# =====================================================

def filter_platform(df, platform):

    if platform == "instagram":

        return df[
            df["platform"].isin(
                [
                    "instagram_account",
                    "instagram_hashtag"
                ]
            )
        ]

    elif platform == "youtube":

        return df[
            df["platform"] == "youtube"
        ]

    elif platform == "news":

        return df[
            df["platform"].isin(
                [
                    "googlenews",
                    "newsapi"
                ]
            )
        ]

    elif platform == "campaignindia":

        return df[
            df["platform"] == "campaignindia"
        ]

    elif platform == "reviews":

        return df[
            df["platform"] == "rss_reviews"
        ]

    return df


# =====================================================
# KEYWORDS
# =====================================================

def get_keywords(platform):

    df = load_all_cleaned_data()

    if df.empty:
        return []

    df = filter_platform(df, platform)

    keywords = []

    if platform == "instagram":

        if "hashtag" in df.columns:

            result = (
                df["hashtag"]
                .dropna()
                .astype(str)
                .value_counts()
                .reset_index()
            )

            result.columns = [
                "keyword",
                "count"
            ]

            return result.to_dict(
                orient="records"
            )

    elif platform == "youtube":

        if "keyword" in df.columns:

            result = (
                df["keyword"]
                .dropna()
                .astype(str)
                .value_counts()
                .reset_index()
            )

            result.columns = [
                "keyword",
                "count"
            ]

            return result.to_dict(
                orient="records"
            )

    elif platform == "campaignindia":

        if "matched_keyword" in df.columns:

            result = (
                df["matched_keyword"]
                .dropna()
                .astype(str)
                .value_counts()
                .reset_index()
            )

            result.columns = [
                "keyword",
                "count"
            ]

            return result.to_dict(
                orient="records"
            )

    elif platform == "news":

        keyword_cols = [
            "keyword",
            "matched_keyword",
            "input_keyword"
        ]

        for col in keyword_cols:

            if col in df.columns:

                keywords.extend(
                    df[col]
                    .dropna()
                    .astype(str)
                    .tolist()
                )

    elif platform == "reviews":

        if "brand_mentions" in df.columns:

            keywords.extend(
                df["brand_mentions"]
                .dropna()
                .astype(str)
                .tolist()
            )

    if not keywords:
        return []

    result = (
        pd.Series(keywords)
        .value_counts()
        .reset_index()
    )

    result.columns = [
        "keyword",
        "count"
    ]

    return result.to_dict(
        orient="records"
    )


# =====================================================
# OVERVIEW
# =====================================================

def get_overview(
    platform,
    keyword
):

    df = load_all_cleaned_data()

    if df.empty:

        return {}

    df = filter_platform(
        df,
        platform
    )

    if keyword:

        df = df[
            df.astype(str)
            .apply(
                lambda x:
                x.str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

    total_mentions = len(df)

    positive = len(
        df[
            df.get(
                "sentiment_label",
                ""
            )
            .astype(str)
            .str.lower()
            == "positive"
        ]
    )

    neutral = len(
        df[
            df.get(
                "sentiment_label",
                ""
            )
            .astype(str)
            .str.lower()
            == "neutral"
        ]
    )

    negative = len(
        df[
            df.get(
                "sentiment_label",
                ""
            )
            .astype(str)
            .str.lower()
            == "negative"
        ]
    )

    engagement = 0

    if "engagement" in df.columns:

        engagement = (
            pd.to_numeric(
                df["engagement"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )

    quality = 0

    quality_cols = [
        "content_quality_score",
        "quality_score"
    ]

    for col in quality_cols:

        if col in df.columns:

            quality = round(
                pd.to_numeric(
                    df[col],
                    errors="coerce"
                )
                .fillna(0)
                .mean(),
                2
            )

            break

    return {

        "total_mentions":
            int(total_mentions),

        "positive":
            int(positive),

        "neutral":
            int(neutral),

        "negative":
            int(negative),

        "engagement":
            int(engagement),

        "quality_score":
            quality
    }


# =====================================================
# CHARTS
# =====================================================

def get_charts(
    platform,
    keyword
):

    df = load_all_cleaned_data()

    if df.empty:

        return {
            "sentiment": [],
            "trend": []
        }

    df = filter_platform(
        df,
        platform
    )

    if keyword:

        df = df[
            df.astype(str)
            .apply(
                lambda x:
                x.str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

    sentiment_chart = []

    if "sentiment_label" in df.columns:
    
        sentiment_chart = (
            df["sentiment_label"]
            .value_counts()
            .reset_index()
        )

        sentiment_chart.columns = [
            "name",
            "value"
        ]

        sentiment_chart = (
            sentiment_chart
            .to_dict(
                orient="records"
            )
        )

    trend = []

    date_cols = [
        "published_at",
        "timestamp",
        "post_timestamp",
        "published_date"
    ]

    date_col = None

    for col in date_cols:

        if col in df.columns:

            date_col = col

            break

    if date_col:
        print("DATE COL:", date_col)

        if date_col:
            print(
                df[date_col]
                .head(10)
                .tolist()
            )
    
        temp = df.copy()

        temp[date_col] = pd.to_datetime(
            temp[date_col],
            errors="coerce",
            utc=True
        )

        temp = temp.dropna(
            subset=[date_col]
        )

        if not temp.empty:

            trend_df = (

                temp

                .groupby(
                    temp[date_col]
                    .dt.strftime(
                        "%Y-%m-%d"
                    )
                )

                .size()

                .reset_index(
                    name="count"
                )

            )

            trend_df.columns = [
                "date",
                "count"
            ]

            trend = (

                trend_df

                .sort_values(
                    "date"
                )

                .tail(30)

                .to_dict(
                    orient="records"
                )

            )

    return {

        "sentiment":
            sentiment_chart,

        "trend":
            trend
    }


# =====================================================
# CONTENT
# =====================================================

def get_content(
    platform,
    keyword
):

    df = load_all_cleaned_data()

    if df.empty:
        return []

    df = filter_platform(
        df,
        platform
    )
    print(df.columns.tolist())

    if keyword:

        df = df[
            df.astype(str)
            .apply(
                lambda x:
                x.str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

    return (

        df

        .fillna("")

        .head(100)

        .to_dict(
            orient="records"
        )

    )


# =====================================================
# TOP CONTENT
# =====================================================

def get_top_content(platform, keyword):

    df = load_all_cleaned_data()

    if df.empty:
        return []

    df = filter_platform(df, platform)

    if keyword:
        df = df[
            df.astype(str)
            .apply(
                lambda x: x.str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

    sort_col = None

    if platform == "instagram":
        sort_col = "engagement"

    elif platform == "youtube":
        sort_col = "view_count_numeric"

    elif platform == "news":
        sort_col = "content_quality_score"

    elif platform == "campaignindia":
        sort_col = "mention_strength"

    elif platform == "reviews":
        sort_col = "urgency_score"

    if sort_col and sort_col in df.columns:

        df[sort_col] = pd.to_numeric(
            df[sort_col],
            errors="coerce"
        )

        df = df.sort_values(
            sort_col,
            ascending=False
        )

    return (
        df.fillna("")
        .head(10)
        .to_dict(orient="records")
    )


# =====================================================
# TOP POSITIVE
# =====================================================

def get_top_positive(platform, keyword):

    df = load_all_cleaned_data()

    if df.empty:
        return []

    df = filter_platform(df, platform)

    if keyword:

        df = df[
            df.astype(str)
            .apply(
                lambda x:
                x.str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

    if "sentiment_label" in df.columns:

        df = df[
            df["sentiment_label"]
            .astype(str)
            .str.lower()
            == "positive"
        ]

    score_col = None

    for col in [
        "content_quality_score",
        "quality_score"
    ]:

        if col in df.columns:

            score_col = col

            break

    if score_col:

        df[score_col] = pd.to_numeric(
            df[score_col],
            errors="coerce"
        )

        df = df.sort_values(
            score_col,
            ascending=False
        )

    return (
        df.fillna("")
        .head(10)
        .to_dict(orient="records")
    )


# =====================================================
# TOP NEGATIVE
# =====================================================

def get_top_negative(platform, keyword):

    df = load_all_cleaned_data()

    if df.empty:
        return []

    df = filter_platform(df, platform)

    if keyword:

        df = df[
            df.astype(str)
            .apply(
                lambda x:
                x.str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            )
            .any(axis=1)
        ]

    if "sentiment_label" in df.columns:

        df = df[
            df["sentiment_label"]
            .astype(str)
            .str.lower()
            == "negative"
        ]

    score_col = None

    for col in [
        "urgency_score",
        "quality_score",
        "content_quality_score"
    ]:

        if col in df.columns:

            score_col = col

            break

    if score_col:

        df[score_col] = pd.to_numeric(
            df[score_col],
            errors="coerce"
        )

        df = df.sort_values(
            score_col,
            ascending=False
        )

    return (
        df.fillna("")
        .head(10)
        .to_dict(orient="records")
    )


