import pandas as pd
import re


def safe_fillna(df):
    return df.fillna("")


def remove_duplicates(df):
    return df.drop_duplicates()


def clean_text(text):
    if pd.isna(text):
        return ""

    text = str(text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_word_count(text):
    if not text:
        return 0

    return len(str(text).split())