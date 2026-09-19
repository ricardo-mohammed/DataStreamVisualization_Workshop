from pathlib import Path

from dotenv import load_dotenv

from data_loader import load_telemetry, simulate_stream
from database import (
    count_records,
    create_database_engine,
    save_telemetry,
    test_connection,
)
from visualization import plot_robot_telemetry


# Locate the parent datavisualisation folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(ENV_PATH)

CSV_PATH = PROJECT_ROOT / "data" / "RMBR4-2_export_test.csv"

TABLE_NAME = "robot_telemetry"


def main():
    telemetry = load_telemetry(CSV_PATH)
    streamed_data = simulate_stream(telemetry, record_limit=100)

    engine = create_database_engine()

    try:
        test_connection(engine)
        save_telemetry(telemetry, engine, TABLE_NAME)

        record_count = count_records(engine, TABLE_NAME)
        print("Records in database:", record_count)
    finally:
        engine.dispose()

    plot_robot_telemetry(telemetry)


if __name__ == "__main__":
    main()
