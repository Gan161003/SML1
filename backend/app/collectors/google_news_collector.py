# import feedparser
# import pandas as pd
# import re

# from datetime import datetime


# # ==========================================
# # FIND MATCHED KEYWORD
# # ==========================================

# def find_matched_keyword(
#     text,
#     keywords
# ):

#     text_lower = text.lower()

#     for keyword in keywords:

#         pattern = (
#             rf"\b"
#             f"{re.escape(keyword.lower())}"
#             rf"\b"
#         )

#         if re.search(
#             pattern,
#             text_lower
#         ):
#             return keyword

#     return None


# # ==========================================
# # MAIN COLLECTOR
# # ==========================================

# def run_google_news_connector(
#     config
# ):

#     connector_id = config.get(
#         "connector_id"
#     )

#     connector_name = config.get(
#         "connector_name"
#     )

#     keywords = config.get(
#         "keywords",
#         ""
#     )

#     max_articles = int(
#         config.get(
#             "max_articles",
#             100
#         )
#     )

#     keyword_list = [

#         k.strip()

#         for k in
#         keywords.split(",")

#         if k.strip()

#     ]

#     all_articles = []

#     for keyword in keyword_list:

#         print(
#             f"Fetching Google News: {keyword}"
#         )

#         search_query = (
#             keyword.replace(
#                 " ",
#                 "+"
#             )
#         )

#         rss_url = (
#             "https://news.google.com/rss/search"
#             f"?q={search_query}"
#         )

#         feed = feedparser.parse(
#             rss_url
#         )

#         count = 0

#         for entry in feed.entries:

#             if count >= max_articles:
#                 break

#             title = entry.get(
#                 "title",
#                 ""
#             )

#             description = entry.get(
#                 "summary",
#                 ""
#             )

#             matched_term = (
#                 find_matched_keyword(
#                     title,
#                     keyword_list
#                 )
#             )

#             if not matched_term:
#                 continue

#             record = {

#                 "connector_id":
#                 connector_id,

#                 "connector_name":
#                 connector_name,

#                 "platform":
#                 "googlenews",

#                 "source":
#                 (
#                     entry.get(
#                         "source",
#                         {}
#                     ).get(
#                         "title"
#                     )
#                     if entry.get(
#                         "source"
#                     )
#                     else ""
#                 ),

#                 "input_keyword":
#                 keyword,

#                 "matched_keyword":
#                 matched_term,

#                 "title":
#                 title,

#                 "description":
#                 description,

#                 "url":
#                 entry.get(
#                     "link"
#                 ),

#                 "published_at":
#                 entry.get(
#                     "published"
#                 ),

#                 "collected_at":
#                 datetime.now()
#                 .isoformat(),

#                 "title_length":
#                 len(title),

#                 "description_length":
#                 len(description),

#                 "word_count":
#                 len(
#                     (
#                         title
#                         + " "
#                         + description
#                     ).split()
#                 )
#             }

#             all_articles.append(
#                 record
#             )

#             count += 1

#     df = pd.DataFrame(
#         all_articles
#     )

#     if not df.empty:

#         df.drop_duplicates(
#             subset=["url"],
#             inplace=True
#         )

#     return df


















import feedparser
import pandas as pd
import requests
import re
from newspaper import Article
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse


# ==========================================
# HEADERS
# ==========================================

HEADERS = {

    "User-Agent":
    (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )

}


# ==========================================
# FIND MATCHED KEYWORD
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
# RESOLVE REAL ARTICLE URL
# ==========================================

def get_real_url(
    google_news_url
):

    try:

        response = requests.get(
            google_news_url,
            headers=HEADERS,
            timeout=30,
            allow_redirects=True
        )

        return response.url

    except:

        return google_news_url


# ==========================================
# SCRAPE ARTICLE
# ==========================================


HEADERS = {
    "User-Agent":
    (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}


def scrape_article(article_url):

    # ----------------------------------
    # METHOD 1 - NEWSPAPER3K
    # ----------------------------------

    try:

        article = Article(article_url)

        article.download()

        article.parse()

        content = (
            article.text or ""
        )

        if len(content) > 100:

            return {

                "title":
                article.title,

                "description":
                article.meta_description,

                "content":
                content,

                "author":
                ",".join(
                    article.authors
                )
            }

    except Exception:
        pass

    # ----------------------------------
    # METHOD 2 - BEAUTIFULSOUP FALLBACK
    # ----------------------------------

    try:

        response = requests.get(
            article_url,
            headers=HEADERS,
            timeout=30
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = ""

        title_tag = soup.find("h1")

        if title_tag:

            title = (
                title_tag.get_text(
                    strip=True
                )
            )

        description = ""

        meta_desc = soup.find(
            "meta",
            attrs={
                "name":
                "description"
            }
        )

        if meta_desc:

            description = (
                meta_desc.get(
                    "content",
                    ""
                )
            )

        author = ""

        meta_author = soup.find(
            "meta",
            attrs={
                "name":
                "author"
            }
        )

        if meta_author:

            author = (
                meta_author.get(
                    "content",
                    ""
                )
            )

        paragraphs = soup.find_all(
            "p"
        )

        content = " ".join([

            p.get_text(
                strip=True
            )

            for p in paragraphs

        ])

        return {

            "title":
            title,

            "description":
            description,

            "content":
            content,

            "author":
            author
        }

    except Exception:

        return {

            "title": "",

            "description": "",

            "content": "",

            "author": ""
        }
# ==========================================
# MAIN COLLECTOR
# ==========================================

def run_google_news_connector(
    config
):

    connector_id = config.get(
        "connector_id"
    )

    connector_name = config.get(
        "connector_name"
    )

    keywords = config.get(
        "keywords",
        ""
    )

    max_articles = int(
        config.get(
            "max_articles",
            100
        )
    )

    keyword_list = [

        k.strip()

        for k in
        keywords.split(",")

        if k.strip()

    ]

    all_articles = []

    for keyword in keyword_list:

        print(
            f"Fetching Google News: {keyword}"
        )

        search_query = (
            keyword.replace(
                " ",
                "+"
            )
        )

        rss_url = (
            "https://news.google.com/rss/search"
            f"?q={search_query}"
        )

        feed = feedparser.parse(
            rss_url
        )

        count = 0

        for entry in feed.entries:

            if count >= max_articles:
                break

            rss_title = entry.get(
                "title",
                ""
            )
            rss_description = BeautifulSoup(
                entry.get("summary", ""),
                "html.parser"
            ).get_text(
                " ",
                strip=True
            )

            matched_keyword = (
                find_matched_keyword(
                    rss_title,
                    keyword_list
                )
            )

            if not matched_keyword:
                continue

            google_news_url = (
                entry.get(
                    "link"
                )
            )

            real_url = (
                get_real_url(
                    google_news_url
                )
            )

            article_data = (
                scrape_article(
                    real_url
                )
            )

            domain = ""

            try:

                domain = (
                    urlparse(
                        real_url
                    ).netloc
                )

            except:

                pass

            title = (
                article_data[
                    "title"
                ]
                or
                rss_title
            )

            description = (
                article_data.get(
                    "description",
                    ""
                )
                or
                rss_description
            )

            bad_descriptions = [

                "Comprehensive, up-to-date news coverage",

                "Google News",

                "aggregated from sources"

            ]

            if any(
                bad.lower()
                in description.lower()
                for bad in bad_descriptions
            ):
                description = rss_description

            # content = (
            #     article_data[
            #         "content"
            #     ]
            # )
            content = (
                article_data.get(
                    "content",
                    ""
                )
            )

            author = (
                article_data[
                    "author"
                ]
            )

            record = {

                "connector_id":
                connector_id,

                "connector_name":
                connector_name,

                "platform":
                "googlenews",

                "source":
                (
                    entry.get(
                        "source",
                        {}
                    ).get(
                        "title"
                    )
                    if entry.get(
                        "source"
                    )
                    else ""
                ),

                "input_keyword":
                keyword,

                "matched_keyword":
                matched_keyword,

                "title":
                title,

                "description":
                description,

                "content":
                content,

                "author":
                author,

                "domain":
                domain,

                "google_news_url":
                google_news_url,

                "article_url":
                real_url,

                "published_at":
                entry.get(
                    "published"
                ),

                "collected_at":
                datetime.now()
                .isoformat(),

                "title_length":
                len(title),

                "description_length":
                len(description),

                "content_length":
                len(content),

                "word_count":
                len(
                    content.split()
                ),

                "keyword_found_in_title":
                (
                    matched_keyword.lower()
                    in title.lower()
                ),

                "keyword_found_in_description":
                (
                    matched_keyword.lower()
                    in description.lower()
                ),

                "keyword_found_in_content":
                (
                    matched_keyword.lower()
                    in content.lower()
                )
            }

            all_articles.append(
                record
            )

            count += 1

    df = pd.DataFrame(
        all_articles
    )

    if not df.empty:

        df.drop_duplicates(
            subset=[
                "article_url"
            ],
            inplace=True
        )

    return df