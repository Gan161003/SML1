from googleapiclient.discovery import build
import pandas as pd

from datetime import datetime


def run_youtube_connector(config):

    api_key = config["api_key"]

    keyword = config["keywords"]

    max_videos = int(
        config["max_videos"]
    )

    max_comments = int(
        config["max_comments"]
    )

    connector_name = config.get(
        "connector_name",
        ""
    )

    connector_id = config.get(
        "connector_id",
        ""
    )

    youtube = build(
        "youtube",
        "v3",
        developerKey=api_key
    )

    search_response = (
        youtube.search()
        .list(
            q=keyword,
            part="snippet",
            type="video",
            maxResults=max_videos
        )
        .execute()
    )

    videos = []
    comments = []

    pull_time = datetime.now()

    for item in search_response["items"]:

        try:
            video_id = item["id"]["videoId"]
        except:
            continue

        snippet = item["snippet"]

        title = snippet.get(
            "title",
            ""
        )

        description = snippet.get(
            "description",
            ""
        )

        channel_name = snippet.get(
            "channelTitle",
            ""
        )

        channel_id = snippet.get(
            "channelId",
            ""
        )

        published_at = snippet.get(
            "publishedAt",
            ""
        )

        thumbnail_url = (
            snippet
            .get("thumbnails", {})
            .get("high", {})
            .get("url", "")
        )

        stats = (
            youtube.videos()
            .list(
                part="statistics",
                id=video_id
            )
            .execute()
        )

        statistics = (
            stats["items"][0]
            .get("statistics", {})
        )

        view_count = statistics.get(
            "viewCount",
            0
        )

        like_count = statistics.get(
            "likeCount",
            0
        )

        favorite_count = statistics.get(
            "favoriteCount",
            0
        )

        comment_count = statistics.get(
            "commentCount",
            0
        )

        videos.append({

            "connector_id": connector_id,
            "connector_name": connector_name,

            "platform": "youtube",

            "keyword": keyword,

            "pull_time": pull_time,

            "video_id": video_id,

            "video_title": title,

            "video_description": description,

            "video_url":
            f"https://www.youtube.com/watch?v={video_id}",

            "channel_id": channel_id,

            "channel_name": channel_name,

            "published_at": published_at,

            "view_count": view_count,

            "like_count": like_count,

            "favorite_count": favorite_count,

            "comment_count": comment_count,

            "thumbnail_url": thumbnail_url
        })

        try:

            comment_response = (
                youtube.commentThreads()
                .list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=max_comments,
                    textFormat="plainText"
                )
                .execute()
            )

            for comment_item in comment_response["items"]:

                comment_id = comment_item["id"]

                comment_snippet = (
                    comment_item["snippet"]
                    ["topLevelComment"]
                    ["snippet"]
                )

                comments.append({

                    "connector_id":
                    connector_id,

                    "connector_name":
                    connector_name,

                    "platform":
                    "youtube",

                    "keyword":
                    keyword,

                    "pull_time":
                    pull_time,

                    "video_id":
                    video_id,

                    "video_title":
                    title,

                    "comment_id":
                    comment_id,

                    "comment_author":
                    comment_snippet.get(
                        "authorDisplayName",
                        ""
                    ),

                    "comment_text":
                    comment_snippet.get(
                        "textDisplay",
                        ""
                    ),

                    "comment_like_count":
                    comment_snippet.get(
                        "likeCount",
                        0
                    ),

                    "comment_published_at":
                    comment_snippet.get(
                        "publishedAt",
                        ""
                    ),

                    "comment_updated_at":
                    comment_snippet.get(
                        "updatedAt",
                        ""
                    ),

                    "comment_url":
                    (
                        f"https://www.youtube.com/watch?"
                        f"v={video_id}&lc={comment_id}"
                    )
                })

        except Exception:
            pass

    videos_df = pd.DataFrame(videos)

    comments_df = pd.DataFrame(comments)

    return {
        "videos_df": videos_df,
        "comments_df": comments_df
    }