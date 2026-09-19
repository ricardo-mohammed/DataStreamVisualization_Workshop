"""Interactive Plotly charts for robot telemetry."""

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure


def find_axis_columns(dataframe: pd.DataFrame) -> list[str]:
    """Find populated numeric columns whose names begin with 'Axis #'."""
    return [
        column
        for column in dataframe.columns
        if column.startswith("Axis #")
        and dataframe[column].notna().any()
        and pd.api.types.is_numeric_dtype(dataframe[column])
    ]


def plot_robot_telemetry(
    dataframe: pd.DataFrame,
    time_column: str = "Time",
    output_html: str | None = "robot_telemetry.html",
) -> Figure:
    """Plot each populated robot axis against time and optionally save HTML."""
    axis_columns = find_axis_columns(dataframe)
    if not axis_columns:
        raise ValueError("No populated numeric columns beginning with 'Axis #' were found.")

    telemetry = dataframe[[time_column, *axis_columns]].melt(
        id_vars=time_column,
        var_name="Axis",
        value_name="Value",
    ).dropna(subset=["Value"])

    figure = px.line(
        telemetry,
        x=time_column,
        y="Value",
        color="Axis",
        title="Robot Hand Activity Over Time",
        labels={time_column: "Time", "Value": "Axis value"},
    )
    figure.update_layout(hovermode="x unified", template="plotly_white")
    figure.update_xaxes(rangeslider_visible=True)

    if output_html:
        figure.write_html(output_html)
        print(f"Interactive graph saved as '{output_html}'.")

    figure.show()
    return figure
