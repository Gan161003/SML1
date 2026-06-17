import feedparser
import pandas as pd
import re

from bs4 import BeautifulSoup
from datetime import datetime


def run_rss_reviews_connector(
    config
):

    connector_id = config.get(
        "connector_id"
    )

    connector_name = config.get(
        "connector_name"
    )

    rss_urls = config.get(
        "rss_urls",
        ""
    )

    rss_list = [

        url.strip()

        for url in
        rss_urls.split(",")

        if url.strip()

    ]

    records = []

    for rss_url in rss_list:

        print(
            f"Reading RSS: {rss_url}"
        )

        feed = feedparser.parse(
            rss_url
        )

        for entry in feed.entries:

            title = getattr(
                entry,
                "title",
                ""
            )

            published = getattr(
                entry,
                "published",
                ""
            )

            link = getattr(
                entry,
                "link",
                ""
            )

            description_html = getattr(
                entry,
                "description",
                ""
            )

            soup = BeautifulSoup(
                description_html,
                "html.parser"
            )

            text = soup.get_text(
                " ",
                strip=True
            )

            rating_match = re.search(
                r"Rating:\s*(\d+)\/5\s*\((.*?)\)",
                text,
                re.IGNORECASE
            )

            rating = None
            rating_label = None

            if rating_match:

                rating = (
                    rating_match.group(1)
                )

                rating_label = (
                    rating_match.group(2)
                )

            reviewer_match = re.search(
                r"Reviewer:\s*(.*)",
                text,
                re.IGNORECASE
            )

            reviewer = None

            if reviewer_match:

                reviewer = (
                    reviewer_match.group(1)
                    .strip()
                )

            review_text = text

            review_text = re.sub(
                r"Rating:\s*\d+\/5\s*\(.*?\)",
                "",
                review_text,
                flags=re.IGNORECASE
            )

            review_text = re.sub(
                r"Reviewer:\s*.*",
                "",
                review_text,
                flags=re.IGNORECASE
            )

            review_text = (
                review_text.strip()
            )

            records.append({

                "connector_id":
                connector_id,

                "connector_name":
                connector_name,

                "platform":
                "rss_reviews",

                "feed_url":
                rss_url,

                "review_title":
                title,

                "review_text":
                review_text,

                "rating":
                rating,

                "rating_label":
                rating_label,

                "reviewer":
                reviewer,

                "published_date":
                published,

                "review_url":
                link,

                "collected_at":
                datetime.now()
                .isoformat()

            })

    df = pd.DataFrame(
        records
    )

    return df