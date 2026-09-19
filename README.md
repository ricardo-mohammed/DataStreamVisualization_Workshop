# Modular Robot Telemetry Project

The program is separated by responsibility:

- `data_loader.py` loads, cleans, and simulates streaming CSV records.
- `database.py` connects to PostgreSQL and stores/counts records.
- `visualization.py` builds the interactive Plotly time-series graph.
- `main.py` imports and calls the other modules.

## Setup

1. Open a terminal in this folder.
2. Install packages: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`.
4. Put the newly rotated Neon connection URL in `.env` as `DATABASE_URL=...`.
5. Check that `CSV_PATH` in `main.py` points to your CSV.
6. Run: `python main.py`

The chart opens interactively and is also saved as `robot_telemetry.html`.

## Why Plotly?

Plotly fits this data better than a static Matplotlib or Seaborn chart because
you can hover over exact timestamps, hide/show individual axes, zoom into a
movement interval, and use the range slider to inspect long recordings.
