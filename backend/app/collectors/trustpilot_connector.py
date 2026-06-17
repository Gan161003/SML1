import feedparser
import pandas as pd
from bs4 import BeautifulSoup
import re


def pull_trustpilot_rss(rss_urls):

    all_reviews = []

    # Split comma-separated URLs
    rss_list = [url.strip() for url in rss_urls.split(",") if url.strip()]

    for rss_url in rss_list:

        print(f"Pulling: {rss_url}")

        try:

            feed = feedparser.parse(rss_url)

            for entry in feed.entries:

                title = getattr(entry, "title", "")
                published = getattr(entry, "published", "")
                link = getattr(entry, "link", "")

                description_html = getattr(entry, "description", "")

                soup = BeautifulSoup(
                    description_html,
                    "html.parser"
                )

                text = soup.get_text(
                    " ",
                    strip=True
                )

                # Rating
                rating_match = re.search(
                    r'Rating:\s*(\d+)\/5\s*\((.*?)\)',
                    text,
                    re.IGNORECASE
                )

                rating = None
                rating_label = None

                if rating_match:
                    rating = rating_match.group(1)
                    rating_label = rating_match.group(2)

                # Reviewer
                reviewer_match = re.search(
                    r'Reviewer:\s*(.*)',
                    text,
                    re.IGNORECASE
                )

                reviewer = None

                if reviewer_match:
                    reviewer = reviewer_match.group(1).strip()

                # Clean review text
                review_text = re.sub(
                    r'Rating:\s*\d+\/5\s*\(.*?\)',
                    '',
                    text,
                    flags=re.IGNORECASE
                )

                review_text = re.sub(
                    r'Reviewer:\s*.*',
                    '',
                    review_text,
                    flags=re.IGNORECASE
                )

                review_text = review_text.strip()

                all_reviews.append({
                    "Platform": "Trustpilot",
                    "Source URL": rss_url,
                    "Review Title": title,
                    "Review Text": review_text,
                    "Rating": rating,
                    "Rating Label": rating_label,
                    "Reviewer": reviewer,
                    "Published Date": published,
                    "Review URL": link
                })

        except Exception as e:

            print(
                f"Error reading {rss_url}: {str(e)}"
            )

    return pd.DataFrame(all_reviews)