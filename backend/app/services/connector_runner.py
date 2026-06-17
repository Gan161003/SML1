# import json

# from app.storage.excel_storage import (
#     get_connectors,
#     save_connectors
# )

# from app.collectors.youtube_collector import (
#     run_youtube_connector
# )

# from app.storage.raw_storage import (
#     save_raw_dataframe
# )

# from datetime import datetime


# def run_connector(
#     connector_id
# ):

#     df = get_connectors()

#     row = df[
#         df["connector_id"]
#         == connector_id
#     ]

#     if row.empty:

#         return {
#             "status": "error",
#             "message": "Connector not found"
#         }

#     connector = (
#         row.iloc[0]
#         .to_dict()
#     )

#     connector_type = connector[
#         "connector_type"
#     ]

#     config = json.loads(
#         connector["config_json"]
#     )

#     config["connector_id"] = (
#         connector_id
#     )

#     config["connector_name"] = (
#         connector["connector_name"]
#     )

#     if connector_type == "youtube":

#         result = (
#             run_youtube_connector(
#                 config
#             )
#         )

#         video_file = (
#             save_raw_dataframe(
#                 result["videos_df"],
#                 "youtube",
#                 "videos"
#             )
#         )

#         comment_file = (
#             save_raw_dataframe(
#                 result["comments_df"],
#                 "youtube",
#                 "comments"
#             )
#         )

#         idx = row.index[0]

#         df.at[
#             idx,
#             "last_run"
#         ] = datetime.now().strftime(
#             "%Y-%m-%d %H:%M:%S"
#         )

#         save_connectors(df)

#         return {

#             "status": "success",

#             "video_records":
#             len(
#                 result["videos_df"]
#             ),

#             "comment_records":
#             len(
#                 result["comments_df"]
#             ),

#             "video_file":
#             video_file,

#             "comment_file":
#             comment_file
#         }

#     return {
#         "status": "error",
#         "message":
#         f"Unsupported connector: "
#         f"{connector_type}"
#     }
















import json

from datetime import datetime

# from app.storage.excel_storage import (
#     get_connectors,
#     save_connectors
# )

from app.storage.excel_storage import (
    get_connectors,
    save_connectors,
    save_connector_run_history
)

from app.collectors.youtube_collector import (
    run_youtube_connector
)
from app.collectors.google_news_collector import (
    run_google_news_connector
)

from app.collectors.instagram_account_collector import (
    run_instagram_account_connector
)
from app.collectors.instagram_hashtag_collector import (
    run_instagram_hashtag_connector
)

from app.storage.raw_storage import (
    save_raw_dataframe
)
from app.collectors.campaign_india_collector import (
    run_campaign_india_connector
)
from app.collectors.newsapi_collector import (
    run_newsapi_connector
)
from app.collectors.rss_reviews_collector import (
    run_rss_reviews_connector
)



# def get_connector_history(
#     connector_id
# ):

#     history_file = (
#         "storage/config/connector_history.xlsx"
#     )

#     if not os.path.exists(
#         history_file
#     ):
#         return []

#     df = pd.read_excel(
#         history_file
#     )

#     df = df[
#         df["connector_id"]
#         == connector_id
#     ]

#     return (
#         df.to_dict(
#             orient="records"
#         )
#     )


def run_connector(
    connector_id
):
    print(
        "RUNNING CONNECTOR:",
        connector_id
    )

    df = get_connectors()

    row = df[
        df["connector_id"]
        == connector_id
    ]

    if row.empty:

        return {
            "status": "error",
            "message": "Connector not found"
        }

    connector = (
        row.iloc[0]
        .to_dict()
    )

    connector_type = connector[
        "connector_type"
    ]

    config = json.loads(
        connector["config_json"]
    )

    config["connector_id"] = (
        connector_id
    )

    config["connector_name"] = (
        connector["connector_name"]
    )
    try:
    

        # ==========================================
        # YOUTUBE
        # ==========================================

        if connector_type == "youtube":

            result = (
                run_youtube_connector(
                    config
                )
            )

            video_file = (
                save_raw_dataframe(
                    dataframe=result["videos_df"],
                    platform="youtube",
                    dataset_type="videos",
                    connector_name=connector[
                        "connector_name"
                    ]
                )
            )

            comment_file = (
                save_raw_dataframe(
                    dataframe=result["comments_df"],
                    platform="youtube",
                    dataset_type="comments",
                    connector_name=connector[
                        "connector_name"
                    ]
                )
            )

            idx = row.index[0]

            df.at[
                idx,
                "last_run"
            ] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            save_connectors(df)
            save_connector_run_history(
                connector_id=connector_id,
                connector_name=connector[
                    "connector_name"
                ],
                status="success"
            )

            return {

                "status":
                "success",

                "connector_type":
                "youtube",

                "video_records":
                len(
                    result["videos_df"]
                ),

                "comment_records":
                len(
                    result["comments_df"]
                ),

                "video_file":
                video_file,

                "comment_file":
                comment_file
            }

        # ==========================================
        # INSTAGRAM ACCOUNT
        # ==========================================

        elif (
            connector_type
            == "instagram_account"
        ):

            instagram_df = (
                run_instagram_account_connector(
                    config
                )
            )
            if instagram_df.empty:
                
                raise Exception(
                    "No records returned"
                )

            output_file = (
                save_raw_dataframe(
                    dataframe=instagram_df,
                    platform="instagram_account",
                    dataset_type="account_data",
                    connector_name=connector[
                        "connector_name"
                    ]
                )
            )

            idx = row.index[0]

            df.at[
                idx,
                "last_run"
            ] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            save_connectors(df)
            save_connector_run_history(
                connector_id=connector_id,
                connector_name=connector[
                    "connector_name"
                ],
                status="success"
            )

            return {

                "status":
                "success",

                "connector_type":
                "instagram_account",

                "records":
                len(
                    instagram_df
                ),

                "file":
                output_file
            }
        

            # ==========================================
        # INSTAGRAM HASHTAG
        # ==========================================

        elif (
            connector_type
            == "instagram_hashtag"
        ):

            instagram_df = (
                run_instagram_hashtag_connector(
                    config
                )
            )
            if instagram_df.empty:
                
                raise Exception(
                    "No records returned"
                )

            output_file = (
                save_raw_dataframe(
                    dataframe=instagram_df,
                    platform="instagram_hashtag",
                    dataset_type="posts",
                    connector_name=connector[
                        "connector_name"
                    ]
                )
            )

            idx = row.index[0]

            df.at[
                idx,
                "last_run"
            ] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            save_connectors(df)
            save_connector_run_history(
                connector_id=connector_id,
                connector_name=connector[
                    "connector_name"
                ],
                status="success"
            )

            return {

                "status":
                "success",

                "connector_type":
                "instagram_hashtag",

                "records":
                len(
                    instagram_df
                ),

                "file":
                output_file
            }
        elif connector_type == "campaignindia":

            campaign_df = (
                run_campaign_india_connector(
                    config
                )
            )
            if campaign_df.empty:
                raise Exception(
                "No records returned"
            )

            output_file = (
                save_raw_dataframe(
                    dataframe=campaign_df,
                    platform="campaignindia",
                    dataset_type="articles",
                    connector_name=connector[
                        "connector_name"
                    ]
                )
            )

            idx = row.index[0]

            df.at[
                idx,
                "last_run"
            ] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            save_connectors(df)
            save_connector_run_history(
                connector_id=connector_id,
                connector_name=connector[
                    "connector_name"
                ],
                status="success"
            )

            return {

                "status":
                "success",

                "connector_type":
                "campaignindia",

                "records":
                len(
                    campaign_df
                ),

                "file":
                output_file

            }
            # ==========================================
        # GOOGLE NEWS
        # ==========================================

        elif (
            connector_type
            == "googlenews"
        ):

            news_df = (
                run_google_news_connector(
                    config
                )
            )
            if news_df.empty:
                raise Exception(
                "No records returned"
            )

            output_file = (
                save_raw_dataframe(
                    dataframe=news_df,
                    platform="googlenews",
                    dataset_type="articles",
                    connector_name=connector[
                        "connector_name"
                    ]
                )
            )

            idx = row.index[0]

            df.at[
                idx,
                "last_run"
            ] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            save_connectors(df)
            save_connector_run_history(
                connector_id=connector_id,
                connector_name=connector[
                    "connector_name"
                ],
                status="success"
            )

            return {

                "status":
                "success",

                "connector_type":
                "googlenews",

                "records":
                len(
                    news_df
                ),

                "file":
                output_file
            }
        
            # ==========================================
        # NEWS API
        # ==========================================

            # ==========================================
        # NEWS API
        # ==========================================
        elif (
            connector_type
            == "newsapi"
        ):

            news_df = (
                run_newsapi_connector(
                    config
                )
            )
            if news_df.empty:
                raise Exception(
                "No records returned"
            )

            output_file = (
                save_raw_dataframe(
                    dataframe=news_df,
                    platform="newsapi",
                    dataset_type="articles",
                    connector_name=connector[
                        "connector_name"
                    ]
                )
            )

            idx = row.index[0]

            df.at[
                idx,
                "last_run"
            ] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            save_connectors(df)
            save_connector_run_history(
                connector_id=connector_id,
                connector_name=connector[
                    "connector_name"
                ],
                status="success"
            )

            return {

                "status":
                "success",

                "connector_type":
                "newsapi",

                "records":
                len(news_df),

                "file":
                output_file
            }

        # ==========================================
        # RSS REVIEWS
        # ==========================================

        elif (
            connector_type
            == "rss_reviews"
        ):

            rss_df = (
                run_rss_reviews_connector(
                    config
                )
            )
            if rss_df.empty:
                raise Exception(
                "No records returned"
            )

            output_file = (
                save_raw_dataframe(
                    dataframe=rss_df,
                    platform="rss_reviews",
                    dataset_type="reviews",
                    connector_name=connector[
                        "connector_name"
                    ]
                )
            )

            idx = row.index[0]

            df.at[
                idx,
                "last_run"
            ] = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            save_connectors(df)
            save_connector_run_history(
                connector_id=connector_id,
                connector_name=connector[
                    "connector_name"
                ],
                status="success"
            )

            return {

                "status":
                "success",

                "connector_type":
                "rss_reviews",

                "records":
                len(rss_df),

                "file":
                output_file
            }
    except Exception as e:

        print(
            "CONNECTOR FAILED"
        )

        print(
            str(e)
        )

        save_connector_run_history(
            connector_id=connector_id,
            connector_name=connector[
                "connector_name"
            ],
            status=f"failed: {str(e)}"
        )

        return {

            "status": "failed",

            "message": str(e)

        }

        # ==========================================
        # UNSUPPORTED
        # ==========================================

    return {

        "status": "error",

        "message":
        f"Unsupported connector: "
        f"{connector_type}"
    }


