"""Load and prepare robot telemetry data."""

from pathlib import Path

import pandas as pd


def load_telemetry(csv_path: str | Path, time_column: str = "Time") -> pd.DataFrame:
    """Read a CSV, remove fully empty columns, and convert its time column."""
    dataframe = pd.read_csv(csv_path)

    empty_columns = dataframe.columns[dataframe.isna().all()].tolist()
    if empty_columns:
        print(f"Removed completely empty columns: {empty_columns}")
        dataframe = dataframe.drop(columns=empty_columns)

    if time_column not in dataframe.columns:
        raise KeyError(f"Required column '{time_column}' was not found.")

    dataframe[time_column] = pd.to_datetime(
        dataframe[time_column], errors="coerce"
    )
    dataframe = dataframe.dropna(subset=[time_column]).sort_values(time_column)
    return dataframe.reset_index(drop=True)


def simulate_stream(dataframe: pd.DataFrame, record_limit: int = 100) -> pd.DataFrame:
    """Return the first records one at a time to imitate a data stream."""
    records = []

    for _, row in dataframe.head(record_limit).iterrows():
        records.append(row.to_dict())

    streamed_data = pd.DataFrame(records, columns=dataframe.columns)
    print(f"Records streamed: {len(streamed_data)}")
    return streamed_data
