# import json
# from datetime import datetime

# from app.storage.excel_storage import (
#     load_connectors,
#     save_connectors
# )


# def get_all_connectors():

#     df = load_connectors()

#     return df.to_dict(
#         orient="records"
#     )


# def create_connector(data):

#     df = load_connectors()

#     if len(df) == 0:
#         connector_id = 1
#     else:
#         connector_id = int(
#             df["connector_id"].max()
#         ) + 1

#     new_row = {
#         "connector_id": connector_id,
#         "connector_type": data["connector_type"],
#         "connector_name": data["connector_name"],
#         "status": "Connected",
#         "config_json": json.dumps(
#             data["config"]
#         ),
#         "created_at": datetime.now().isoformat()
#     }

#     df.loc[len(df)] = new_row

#     save_connectors(df)

#     return new_row

















from app.storage.excel_storage import (
    get_connectors,
    create_connector,
    delete_connector,
    update_connector
)
from app.storage.excel_storage import (
    get_connector_history
)

def get_connector_run_history(
    connector_id
):

    return get_connector_history(
        connector_id
    )

def get_all_connectors():

    df = get_connectors()

    return df.fillna("").to_dict(
        orient="records"
    )


def create_new_connector(payload):

    return create_connector(payload)


def delete_existing_connector(
    connector_id
):

    delete_connector(connector_id)


def update_existing_connector(
    connector_id,
    payload
):

    return update_connector(
        connector_id,
        payload
    )