import requests
import pandas as pd
import re

from textblob import TextBlob
from datetime import datetime


# ==========================================
# SENTIMENT
# ==========================================

def get_sentiment(text):

    try:

        polarity = TextBlob(
            text
        ).sentiment.polarity

        if polarity > 0:

            return "Positive"

        elif polarity < 0:

            return "Negative"

        else:

            return "Neutral"

    except:

        return "Neutral"


# ==========================================
# MATCH FUNCTION
# SAME AS OLD CODE
# ==========================================

def find_matched_keyword(
    text,
    keywords
):

    text_lower = text.lower()

    for keyword in keywords:

        pattern = (
            rf"\b"
            f"{re.escape(keyword.lower())}"
            rf"\b"
        )

        if re.search(
            pattern,
            text_lower
        ):

            return keyword

    return None


# ==========================================
# MAIN COLLECTOR
# ==========================================

def run_newsapi_connector(
    config
):

    connector_id = config.get(
        "connector_id"
    )

    connector_name = config.get(
        "connector_name"
    )

    api_key = config.get(
        "api_key",
        ""
    )

    keywords = config.get(
        "keywords",
        ""
    )

    keyword_list = [

        keyword.strip()

        for keyword in
        keywords.split(",")

        if keyword.strip()

    ]

    all_articles = []

    print("\n===================")
    print("NEWSAPI RUN")
    print("===================")

    print(
        "Keywords:",
        keyword_list
    )

    for keyword in keyword_list:

        print(
            f"\nFetching news for: {keyword}"
        )

        url = (
            "https://newsapi.org/v2/everything?"
            f"q={keyword}"
            "&language=en"
            "&sortBy=publishedAt"
            "&pageSize=100"
            f"&apiKey={api_key}"
        )

        response = requests.get(
            url,
            timeout=30
        )

        if response.status_code != 200:

            print(
                "API Error:",
                response.text
            )

            continue

        data = response.json()

        articles = data.get(
            "articles",
            []
        )

        print(
            "Articles Found:",
            len(articles)
        )

        for article in articles:

            title = (
                article.get(
                    "title",
                    ""
                ) or ""
            )

            description = (
                article.get(
                    "description",
                    ""
                ) or ""
            )

            content = (
                article.get(
                    "content",
                    ""
                ) or ""
            )

            # ==========================
            # OLD LOGIC
            # TITLE ONLY
            # ==========================

            matched_term = (
                find_matched_keyword(
                    title,
                    keyword_list
                )
            )

            if not matched_term:

                continue

            combined_text = (
                title
                + " "
                + description
            )

            sentiment = (
                get_sentiment(
                    combined_text
                )
            )

            record = {

                "connector_id":
                connector_id,

                "connector_name":
                connector_name,

                "platform":
                "newsapi",

                "source":
                article.get(
                    "source",
                    {}
                ).get(
                    "name"
                ),

                "author":
                article.get(
                    "author"
                ),

                "title":
                title,

                "description":
                description,

                "content":
                content,

                "url":
                article.get(
                    "url"
                ),

                "published_at":
                article.get(
                    "publishedAt"
                ),

                "input_keyword":
                keyword,

                "matched_term":
                matched_term,

                "sentiment":
                sentiment,

                "language":
                "en",

                "collected_at":
                datetime.now()
                .astimezone()
                .isoformat()

            }

            all_articles.append(
                record
            )

    df = pd.DataFrame(
        all_articles
    )

    if not df.empty:

        df.drop_duplicates(
            subset=["url"],
            inplace=True
        )

    print(
        "\nFinal Records:",
        len(df)
    )

    return df