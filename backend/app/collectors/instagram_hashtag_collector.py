import requests
import pandas as pd
import re

from datetime import datetime

BASE_URL = "https://graph.facebook.com/v23.0"


# ==========================================
# SAFE REQUEST
# ==========================================

def safe_request(url, params=None):
    
    try:

        response = requests.get(
            url,
            params=params
        )

        print("=" * 60)
        print("REQUEST URL")
        print(response.url)
        print("=" * 60)

        print("STATUS CODE")
        print(response.status_code)

        print("RESPONSE")
        print(response.text)

        print("=" * 60)

        if response.status_code == 200:

            return response.json()

        return {
            "error": response.text
        }

    except Exception as e:

        print(f"REQUEST ERROR: {e}")

        return {
            "error": str(e)
        }


# ==========================================
# HASHTAGS
# ==========================================

def extract_hashtags(text):

    if not text:
        return ""

    hashtags = re.findall(
        r"#(\w+)",
        text
    )

    return ",".join(hashtags)


# ==========================================
# MENTIONS
# ==========================================

def extract_mentions(text):

    if not text:
        return ""

    mentions = re.findall(
        r"@(\w+)",
        text
    )

    return ",".join(mentions)


# ==========================================
# GET HASHTAG ID
# ==========================================
def get_hashtag_id(
    access_token,
    ig_user_id,
    hashtag
):

    url = (
        f"{BASE_URL}/ig_hashtag_search"
    )

    params = {

        "user_id":
        ig_user_id,

        "q":
        hashtag,

        "access_token":
        access_token
    }

    response = safe_request(
        url,
        params
    )

    print("=" * 60)
    print("HASHTAG SEARCH RESPONSE")
    print(response)
    print("=" * 60)

    if "data" not in response:

        return None

    if len(response["data"]) == 0:

        return None

    return response["data"][0]["id"]

# ==========================================
# GET POSTS
# ==========================================

def get_hashtag_posts(
    access_token,
    ig_user_id,
    hashtag_id,
    max_posts
):

    url = (
        f"{BASE_URL}/"
        f"{hashtag_id}/recent_media"
    )

    params = {

        "user_id":
        ig_user_id,

        "fields":
        (
            "id,"
            "caption,"
            "media_type,"
            "media_url,"
            "timestamp,"
            "comments_count,"
            "like_count"
        ),

        "access_token":
        access_token
    }

    posts = []

    response = requests.get(
        url,
        params=params
    )

    if response.status_code != 200:

        return posts

    data = response.json()

    posts.extend(
        data.get(
            "data",
            []
        )
    )

    next_url = (
        data.get(
            "paging",
            {}
        ).get(
            "next"
        )
    )

    while (
        next_url
        and len(posts)
        < max_posts
    ):

        response = requests.get(
            next_url
        )

        if response.status_code != 200:

            break

        data = response.json()

        posts.extend(
            data.get(
                "data",
                []
            )
        )

        next_url = (
            data.get(
                "paging",
                {}
            ).get(
                "next"
            )
        )

    return posts[:max_posts]


# ==========================================
# MAIN
# ==========================================

def run_instagram_hashtag_connector(
    config
):

    access_token = config[
        "access_token"
    ]

    ig_user_id = config[
        "ig_user_id"
    ]

    hashtags = config.get(
        "hashtags",
        ""
    )

    max_posts = int(
        config.get(
            "max_posts",
            500
        )
    )

    connector_id = config.get(
        "connector_id",
        ""
    )

    connector_name = config.get(
        "connector_name",
        ""
    )

    hashtag_list = [
        

        h.strip()

        for h in
        hashtags.split(",")

        if h.strip()

    ]
    print("=" * 50)
    print("HASHTAGS")
    print(hashtag_list)
    print("=" * 50)

    records = []

    pull_time = datetime.now()

    for hashtag in hashtag_list:

        hashtag_id = get_hashtag_id(

            access_token,

            ig_user_id,

            hashtag

        )
        print(
            f"Hashtag: {hashtag}"
        )

        print(
            f"Hashtag ID: {hashtag_id}"
        )

        if not hashtag_id:
    
            print(
                f"Could not find hashtag id for: {hashtag}"
            )

            continue

        posts = get_hashtag_posts(

            access_token,

            ig_user_id,

            hashtag_id,

            max_posts

        )
        print(
            f"Posts Returned: {len(posts)}"
        )

        for post in posts:

            caption = (
                post.get(
                    "caption",
                    ""
                ) or ""
            )

            records.append({

                "connector_id":
                connector_id,

                "connector_name":
                connector_name,

                "platform":
                "instagram_hashtag",

                "pull_time":
                pull_time,

                "hashtag":
                hashtag,

                "post_id":
                post.get("id"),

                "caption":
                caption,

                "media_type":
                post.get(
                    "media_type"
                ),

                "media_url":
                post.get(
                    "media_url"
                ),

                "timestamp":
                post.get(
                    "timestamp"
                ),

                "like_count":
                post.get(
                    "like_count",
                    0
                ),

                "comments_count":
                post.get(
                    "comments_count",
                    0
                ),

                "hashtags_found":
                extract_hashtags(
                    caption
                ),

                "mentions_found":
                extract_mentions(
                    caption
                )
            })

    print(
        f"Total Records: {len(records)}"
    )

    return pd.DataFrame(records)