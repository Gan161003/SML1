import requests
import pandas as pd
import re

from datetime import datetime

BASE_URL = "https://graph.facebook.com/v23.0"


# =====================================================
# SAFE REQUEST
# =====================================================

# def safe_request(url, params=None):

#     try:

#         response = requests.get(
#             url,
#             params=params
#         )

#         if response.status_code == 200:

#             return response.json()

#         return {}

#     except Exception:

#         return {}
def safe_request(url, params=None):
    
    response = requests.get(
        url,
        params=params
    )

    if response.status_code != 200:

        raise Exception(
            response.text
        )

    return response.json()

# =====================================================
# EXTRACT HASHTAGS
# =====================================================

def extract_hashtags(text):

    if not text:
        return ""

    hashtags = re.findall(
        r"#(\w+)",
        text
    )

    return ",".join(hashtags)


# =====================================================
# EXTRACT MENTIONS
# =====================================================

def extract_mentions(text):

    if not text:
        return ""

    mentions = re.findall(
        r"@(\w+)",
        text
    )

    return ",".join(mentions)


# =====================================================
# ACCOUNT DATA
# =====================================================

def get_account_data(
    access_token,
    ig_user_id
):

    url = f"{BASE_URL}/{ig_user_id}"

    params = {

        "fields": (
            "username,"
            "name,"
            "biography,"
            "website,"
            "followers_count,"
            "follows_count,"
            "media_count,"
            "profile_picture_url"
        ),

        "access_token":
        access_token
    }

    return safe_request(
        url,
        params
    )


# =====================================================
# POSTS
# =====================================================

def get_posts(
    access_token,
    ig_user_id
):

    url = f"{BASE_URL}/{ig_user_id}/media"

    params = {

        "fields": (
            "id,"
            "caption,"
            "media_type,"
            "media_url,"
            "permalink,"
            "thumbnail_url,"
            "timestamp,"
            "like_count,"
            "comments_count"
        ),

        "access_token":
        access_token
    }

    return safe_request(
        url,
        params
    )


# =====================================================
# COMMENTS
# =====================================================

def get_comments(
    access_token,
    media_id
):

    url = f"{BASE_URL}/{media_id}/comments"

    params = {

        "fields": (
            "id,"
            "text,"
            "username,"
            "timestamp"
        ),

        "access_token":
        access_token
    }

    return safe_request(
        url,
        params
    )


# =====================================================
# TAGGED POSTS
# =====================================================

def get_tagged_posts(
    access_token,
    ig_user_id
):

    url = f"{BASE_URL}/{ig_user_id}/tags"

    params = {

        "fields": (
            "id,"
            "caption,"
            "media_type,"
            "media_url,"
            "permalink,"
            "timestamp,"
            "like_count,"
            "comments_count"
        ),

        "access_token":
        access_token
    }

    return safe_request(
        url,
        params
    )


# =====================================================
# MAIN COLLECTOR
# =====================================================

def run_instagram_account_connector(
    config
):

    access_token = config[
        "access_token"
    ]

    ig_user_id = config[
        "ig_user_id"
    ]

    max_posts = int(
        config.get(
            "max_posts",
            100
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

    pull_time = datetime.now()

    records = []

    # ==============================================
    # ACCOUNT
    # ==============================================

    account = get_account_data(
        access_token,
        ig_user_id
    )
    print(
        "ACCOUNT RESPONSE:"
    )

    print(account)

    account_username = account.get(
        "username",
        ""
    )

    account_name = account.get(
        "name",
        ""
    )

    followers_count = account.get(
        "followers_count",
        0
    )

    follows_count = account.get(
        "follows_count",
        0
    )

    media_count = account.get(
        "media_count",
        0
    )

    # ==============================================
    # POSTS
    # ==============================================

    posts_response = get_posts(
        access_token,
        ig_user_id
    )
    print(
        "POST RESPONSE:"
    )

    print(posts_response)

    posts = posts_response.get(
        "data",
        []
    )

    posts = posts[:max_posts]

    for post in posts:

        caption = (
            post.get(
                "caption",
                ""
            ) or ""
        )

        hashtags = extract_hashtags(
            caption
        )

        mentions = extract_mentions(
            caption
        )

        records.append({

            "connector_id":
            connector_id,

            "connector_name":
            connector_name,

            "platform":
            "instagram_account",

            "record_type":
            "post",

            "pull_time":
            pull_time,

            "account_username":
            account_username,

            "account_name":
            account_name,

            "followers_count":
            followers_count,

            "follows_count":
            follows_count,

            "media_count":
            media_count,

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

            "permalink":
            post.get(
                "permalink"
            ),

            "post_timestamp":
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

            "hashtags":
            hashtags,

            "mentions":
            mentions,

            "comment_id":
            None,

            "comment_username":
            None,

            "comment_text":
            None,

            "comment_timestamp":
            None
        })

        # ==========================================
        # COMMENTS
        # ==========================================

        comments_response = get_comments(
            access_token,
            post.get("id")
        )

        comments = comments_response.get(
            "data",
            []
        )

        for comment in comments:

            records.append({

                "connector_id":
                connector_id,

                "connector_name":
                connector_name,

                "platform":
                "instagram_account",

                "record_type":
                "comment",

                "pull_time":
                pull_time,

                "account_username":
                account_username,

                "account_name":
                account_name,

                "followers_count":
                followers_count,

                "follows_count":
                follows_count,

                "media_count":
                media_count,

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

                "permalink":
                post.get(
                    "permalink"
                ),

                "post_timestamp":
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

                "hashtags":
                hashtags,

                "mentions":
                mentions,

                "comment_id":
                comment.get("id"),

                "comment_username":
                comment.get(
                    "username"
                ),

                "comment_text":
                comment.get(
                    "text"
                ),

                "comment_timestamp":
                comment.get(
                    "timestamp"
                )
            })

    # ==============================================
    # TAGGED POSTS
    # ==============================================

    tagged_response = get_tagged_posts(
        access_token,
        ig_user_id
    )

    tagged_posts = tagged_response.get(
        "data",
        []
    )

    for tag in tagged_posts:

        caption = (
            tag.get(
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
            "instagram_account",

            "record_type":
            "tagged_post",

            "pull_time":
            pull_time,

            "account_username":
            account_username,

            "account_name":
            account_name,

            "followers_count":
            followers_count,

            "follows_count":
            follows_count,

            "media_count":
            media_count,

            "post_id":
            tag.get("id"),

            "caption":
            caption,

            "media_type":
            tag.get(
                "media_type"
            ),

            "media_url":
            tag.get(
                "media_url"
            ),

            "permalink":
            tag.get(
                "permalink"
            ),

            "post_timestamp":
            tag.get(
                "timestamp"
            ),

            "like_count":
            tag.get(
                "like_count",
                0
            ),

            "comments_count":
            tag.get(
                "comments_count",
                0
            ),

            "hashtags":
            extract_hashtags(
                caption
            ),

            "mentions":
            extract_mentions(
                caption
            ),

            "comment_id":
            None,

            "comment_username":
            None,

            "comment_text":
            None,

            "comment_timestamp":
            None
        })

    return pd.DataFrame(records)