# import os
# from datetime import datetime


# def save_raw_dataframe(
#     df,
#     platform,
#     dataset_name
# ):

#     timestamp = datetime.now().strftime(
#         "%Y%m%d_%H%M%S"
#     )

#     folder = (
#         f"storage/raw/{platform}/{dataset_name}"
#     )

#     os.makedirs(
#         folder,
#         exist_ok=True
#     )

#     filename = (
#         f"{platform}_{dataset_name}_{timestamp}.csv"
#     )

#     file_path = (
#         f"{folder}/{filename}"
#     )

#     df.to_csv(
#         file_path,
#         index=False
#     )

#     return file_path




















import os

from datetime import datetime


def save_raw_dataframe(
    dataframe,
    platform,
    dataset_type,
    connector_name
):


    safe_connector_name = (
        str(connector_name)
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
        .replace("*", "_")
        .replace("?", "_")
        .replace('"', "_")
        .replace("<", "_")
        .replace(">", "_")
        .replace("|", "_")
    )

    folder = (
        f"storage/raw/"
        f"{platform}/"
        f"{dataset_type}"
    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    filename = (
        f"{safe_connector_name}.csv"
    )

    file_path = (
        f"{folder}/{filename}"
    )

    dataframe.to_csv(
        file_path,
        index=False
    )

    return file_path