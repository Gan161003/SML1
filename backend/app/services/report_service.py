from pathlib import Path
import pandas as pd
from fastapi.responses import FileResponse
from tempfile import NamedTemporaryFile
CLEANED_PATH = Path("storage/cleaned")


def load_all_data():

    dfs = []

    for file in CLEANED_PATH.rglob("*.csv"):

        try:

            df = pd.read_csv(file)

            df["source_file"] = file.name

            dfs.append(df)

        except Exception as e:

            print(e)

    if not dfs:

        return pd.DataFrame()

    return pd.concat(
        dfs,
        ignore_index=True
    )


def apply_filters(
    df,
    platform=None,
    sentiment=None,
    brand=None,
    keyword=None
):

    if platform and "platform" in df.columns:

        df = df[
            df["platform"]
            .astype(str)
            .str.lower()
            == platform.lower()
        ]

    sentiment_col = None

    for col in [
        "sentiment_label",
        "sentiment"
    ]:

        if col in df.columns:

            sentiment_col = col

            break

    if sentiment and sentiment_col:

        df = df[
            df[sentiment_col]
            .astype(str)
            .str.lower()
            == sentiment.lower()
        ]

    if keyword:

        search_cols = [
            "title",
            "content",
            "caption",
            "comment_text",
            "review_text"
        ]

        mask = None

        for col in search_cols:

            if col in df.columns:

                current_mask = (
                    df[col]
                    .astype(str)
                    .str.contains(
                        keyword,
                        case=False,
                        na=False
                    )
                )

                if mask is None:

                    mask = current_mask

                else:

                    mask = mask | current_mask

        if mask is not None:

            df = df[mask]

    return df


def get_report_preview(
    platform=None,
    sentiment=None,
    brand=None,
    keyword=None
):

    df = load_all_data()

    if df.empty:

        return []

    df = apply_filters(
        df,
        platform,
        sentiment,
        brand,
        keyword
    )

    return (
        df.head(100)
        .fillna("")
        .to_dict(
            orient="records"
        )
    )

def export_csv(
    platform=None,
    sentiment=None,
    brand=None,
    keyword=None
):

    df = load_all_data()

    df = apply_filters(
        df,
        platform,
        sentiment,
        brand,
        keyword
    )

    temp_file = NamedTemporaryFile(
        delete=False,
        suffix=".csv"
    )

    df.to_csv(
        temp_file.name,
        index=False
    )

    return temp_file.name


def export_excel(
    platform=None,
    sentiment=None,
    brand=None,
    keyword=None
):

    df = load_all_data()

    df = apply_filters(
        df,
        platform,
        sentiment,
        brand,
        keyword
    )

    temp_file = NamedTemporaryFile(
        delete=False,
        suffix=".xlsx"
    )

    df.to_excel(
        temp_file.name,
        index=False
    )

    return temp_file.name