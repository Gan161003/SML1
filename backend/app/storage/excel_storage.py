# import pandas as pd
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parents[3]

# CONNECTOR_FILE = (
#     BASE_DIR /
#     "storage" /
#     "config" /
#     "connectors.xlsx"
# )

# COLUMNS = [
#     "connector_id",
#     "connector_type",
#     "connector_name",
#     "status",
#     "config_json",
#     "created_at"
# ]


# def initialize_connector_file():

#     if not CONNECTOR_FILE.exists():

#         CONNECTOR_FILE.parent.mkdir(
#             parents=True,
#             exist_ok=True
#         )

#         df = pd.DataFrame(columns=COLUMNS)

#         df.to_excel(
#             CONNECTOR_FILE,
#             index=False
#         )


# def load_connectors():

#     initialize_connector_file()

#     return pd.read_excel(CONNECTOR_FILE)


# def save_connectors(df):

#     df.to_excel(
#         CONNECTOR_FILE,
#         index=False
#     )













import os
import json
import pandas as pd
from datetime import datetime

RUN_HISTORY_FILE = (
    "storage/config/connector_run_history.xlsx"
)

RUN_HISTORY_COLUMNS = [
    "history_id",
    "connector_id",
    "connector_name",
    "run_time",
    "status"
]
CONNECTOR_FILE = "storage/config/connectors.xlsx"

COLUMNS = [
    "connector_id",
    "connector_type",
    "connector_name",
    "status",

    "refresh_type",

    "schedule_frequency",
    "schedule_start_date",
    "schedule_start_time",

    "last_run",
    "next_run",

    "config_json",

    "created_at"
]


def initialize_connector_file():

    os.makedirs("storage/config", exist_ok=True)

    if not os.path.exists(CONNECTOR_FILE):

        df = pd.DataFrame(columns=COLUMNS)

        df.to_excel(
            CONNECTOR_FILE,
            index=False
        )


def get_connectors():

    initialize_connector_file()

    return pd.read_excel(CONNECTOR_FILE)


def save_connectors(df):

    df.to_excel(
        CONNECTOR_FILE,
        index=False
    )


def create_connector(data):

    df = get_connectors()

    connector_id = 1

    if not df.empty:
        connector_id = int(df["connector_id"].max()) + 1

    new_row = {
        "connector_id": connector_id,
        "connector_type": data["connector_type"],
        "connector_name": data["connector_name"],
        "status": "active",

        "refresh_type": data["refresh_type"],

        "schedule_frequency": data.get("schedule_frequency"),
        "schedule_start_date": data.get("schedule_start_date"),
        "schedule_start_time": data.get("schedule_start_time"),

        "last_run": None,
        "next_run": None,

        "config_json": json.dumps(data["config"]),

        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    df = pd.concat(
        [df, pd.DataFrame([new_row])],
        ignore_index=True
    )

    save_connectors(df)

    return new_row


def delete_connector(connector_id):

    df = get_connectors()

    df = df[
        df["connector_id"] != connector_id
    ]

    save_connectors(df)


def update_connector(connector_id, payload):

    df = get_connectors()

    idx = df[
        df["connector_id"] == connector_id
    ].index

    if len(idx) == 0:
        return None

    idx = idx[0]

    df.at[idx, "connector_name"] = payload["connector_name"]

    df.at[idx, "refresh_type"] = payload["refresh_type"]

    df.at[idx, "schedule_frequency"] = payload.get(
        "schedule_frequency"
    )

    df.at[idx, "schedule_start_date"] = payload.get(
        "schedule_start_date"
    )

    df.at[idx, "schedule_start_time"] = payload.get(
        "schedule_start_time"
    )

    df.at[idx, "config_json"] = json.dumps(
        payload["config"]
    )

    save_connectors(df)

    return True

def get_connector_history(
    connector_id
):

    history_file = (
        "storage/config/connector_history.xlsx"
    )

    if not os.path.exists(
        history_file
    ):
        return []

    df = pd.read_excel(
        history_file
    )

    df = df[
        df["connector_id"]
        == connector_id
    ]

    return (
        df.to_dict(
            orient="records"
        )
    )

def initialize_run_history_file():
    
    os.makedirs(
        "storage/config",
        exist_ok=True
    )

    if not os.path.exists(
        RUN_HISTORY_FILE
    ):

        df = pd.DataFrame(
            columns=RUN_HISTORY_COLUMNS
        )

        df.to_excel(
            RUN_HISTORY_FILE,
            index=False
        )


def get_run_history():

    initialize_run_history_file()

    return pd.read_excel(
        RUN_HISTORY_FILE
    )


def save_run_history_df(df):

    df.to_excel(
        RUN_HISTORY_FILE,
        index=False
    )


def save_connector_run_history(
    connector_id,
    connector_name,
    status
):

    df = get_run_history()

    history_id = 1

    if not df.empty:

        history_id = (
            int(
                df["history_id"].max()
            ) + 1
        )

    new_row = {

        "history_id":
            history_id,

        "connector_id":
            connector_id,

        "connector_name":
            connector_name,

        "run_time":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "status":
            status
    }

    df = pd.concat(
        [
            df,
            pd.DataFrame(
                [new_row]
            )
        ],
        ignore_index=True
    )
    print(
        "WRITING HISTORY"
    )

    print(
        connector_id,
        connector_name,
        status
    )

    save_run_history_df(df)


def get_connector_history(
    connector_id
):

    df = get_run_history()

    df = df[
        df["connector_id"]
        == connector_id
    ]

    return df.to_dict(
        orient="records"
    )