import pandas as pd
from collections import defaultdict, Counter
from typing import List, Tuple

def preprocess_dates(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df["year"] = df[date_col].dt.year
    df["month"] = df[date_col].dt.to_period("M").dt.to_timestamp()
    return df

def extract_adj_noun_by_time(df: pd.DataFrame, time_col: str = "month") -> dict:
    monthly_pair_counts = defaultdict(Counter)
    valid_rows = df[df["pos_title_with_deps"].apply(lambda x: isinstance(x, list))]
    for _, row in valid_rows.iterrows():
        timestamp = row[time_col]
        tokens = row["pos_title_with_deps"]
        for (w1, tag1, _), (w2, tag2, _) in zip(tokens, tokens[1:]):
            if tag1 == "ADJ" and tag2 == "NOUN":
                monthly_pair_counts[timestamp][(w1.lower(), w2.lower())] += 1
    return monthly_pair_counts

def build_timeseries_df(monthly_counts: dict, pairs_to_track: List[Tuple[str, str]]) -> pd.DataFrame:
    ts_df = pd.DataFrame()
    for pair in pairs_to_track:
        ts_df[pair] = pd.Series({month: counter[pair] for month, counter in monthly_counts.items()})
    return ts_df.sort_index().fillna(0)

def extract_temporal_trends(df: pd.DataFrame,
                             pairs_to_track: List[Tuple[str, str]],
                             date_col: str = "date",
                             time_col: str = "month") -> pd.DataFrame:
    df = preprocess_dates(df, date_col)
    monthly_counts = extract_adj_noun_by_time(df, time_col)
    ts_df = build_timeseries_df(monthly_counts, pairs_to_track)
    return ts_df
