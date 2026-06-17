import requests
import pandas as pd
import json
import time

from bs4 import BeautifulSoup

from datetime import datetime

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


def run_campaign_india_connector(
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
            50
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

        search_keyword = (
            keyword.replace(
                " ",
                "+"
            )
        )

        search_url = (

            "https://www.campaignindia.in/search"

            f"?Terms={search_keyword}"

        )

        try:

            response = requests.get(
                search_url,
                headers=HEADERS,
                timeout=30
            )

            if response.status_code != 200:

                continue

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            article_links = set()

            for link in soup.find_all(
                "a",
                href=True
            ):

                href = link["href"]

                if "/article/" in href:

                    if href.startswith("/"):

                        href = (
                            "https://www.campaignindia.in"
                            + href
                        )

                    article_links.add(
                        href
                    )

            article_links = list(
                article_links
            )[:max_articles]

            for article_url in article_links:

                try:

                    time.sleep(1)

                    article_response = (
                        requests.get(
                            article_url,
                            headers=HEADERS,
                            timeout=30
                        )
                    )

                    if (
                        article_response.status_code
                        != 200
                    ):
                        continue

                    article_soup = BeautifulSoup(
                        article_response.text,
                        "html.parser"
                    )

                    # TITLE

                    title = ""

                    title_tag = (
                        article_soup.find(
                            "h1"
                        )
                    )

                    if title_tag:

                        title = (
                            title_tag
                            .get_text(
                                strip=True
                            )
                        )

                    # DESCRIPTION

                    description = ""

                    meta_desc = (
                        article_soup.find(
                            "meta",
                            attrs={
                                "name":
                                "description"
                            }
                        )
                    )

                    if meta_desc:

                        description = (
                            meta_desc.get(
                                "content",
                                ""
                            )
                        )

                    # CONTENT

                    paragraphs = (
                        article_soup.find_all(
                            "p"
                        )
                    )

                    content = " ".join([

                        p.get_text(
                            strip=True
                        )

                        for p in
                        paragraphs

                    ])

                    # AUTHOR

                    author = ""

                    meta_author = (
                        article_soup.find(
                            "meta",
                            attrs={
                                "name":
                                "author"
                            }
                        )
                    )

                    if meta_author:

                        author = (
                            meta_author.get(
                                "content",
                                ""
                            )
                        )

                    # CATEGORY

                    category = ""

                    meta_section = (
                        article_soup.find(
                            "meta",
                            attrs={
                                "property":
                                "article:section"
                            }
                        )
                    )

                    if meta_section:

                        category = (
                            meta_section.get(
                                "content",
                                ""
                            )
                        )

                    # DATE

                    published_at = ""

                    meta_date = (
                        article_soup.find(
                            "meta",
                            attrs={
                                "property":
                                "article:published_time"
                            }
                        )
                    )

                    if meta_date:

                        published_at = (
                            meta_date.get(
                                "content",
                                ""
                            )
                        )

                    if not published_at:

                        time_tag = (
                            article_soup.find(
                                "time"
                            )
                        )

                        if time_tag:

                            published_at = (

                                time_tag.get(
                                    "datetime"
                                )

                                or

                                time_tag.get_text(
                                    strip=True
                                )

                            )

                    # RECORD

                    record = {

                        "connector_id":
                        connector_id,

                        "connector_name":
                        connector_name,

                        "platform":
                        "campaignindia",

                        "source":
                        "Campaign India",

                        "matched_keyword":
                        keyword,

                        "title":
                        title,

                        "description":
                        description,

                        "content":
                        content,

                        "url":
                        article_url,

                        "author":
                        author,

                        "category":
                        category,

                        "published_at":
                        published_at,

                        "collected_at":
                        datetime.now()
                        .isoformat(),

                        "title_length":
                        len(title),

                        "content_length":
                        len(content),

                        "word_count":
                        len(
                            content.split()
                        )

                    }

                    all_articles.append(
                        record
                    )

                except Exception:

                    pass

        except Exception:

            pass

    df = pd.DataFrame(
        all_articles
    )

    if not df.empty:

        df.drop_duplicates(
            subset=["url"],
            inplace=True
        )

    return df
