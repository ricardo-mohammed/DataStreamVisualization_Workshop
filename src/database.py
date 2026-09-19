"""PostgreSQL operations for robot telemetry."""

import os

import pandas as pd
from sqlalchemy import Engine, create_engine, text


def create_database_engine() -> Engine:
    """Create an engine using DATABASE_URL from the environment."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is missing. Copy .env.example to .env and add your URL."
        )
    return create_engine(database_url)


def test_connection(engine: Engine) -> None:
    """Confirm that PostgreSQL accepts the connection."""
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    print("Database connection successful!")


def save_telemetry(
    dataframe: pd.DataFrame,
    engine: Engine,
    table_name: str = "robot_telemetry",
) -> None:
    """Replace a PostgreSQL table with the supplied telemetry."""
    dataframe.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
        chunksize=1000,
        method="multi",
    )
    print(f"Data successfully stored in PostgreSQL table '{table_name}'.")


def count_records(engine: Engine, table_name: str = "robot_telemetry") -> int:
    """Count stored records. The table name is restricted to safe characters."""
    if not table_name.replace("_", "").isalnum():
        raise ValueError("Invalid table name.")

    with engine.connect() as connection:
        result = connection.execute(text(f'SELECT COUNT(*) FROM "{table_name}"'))
        return int(result.scalar_one())
