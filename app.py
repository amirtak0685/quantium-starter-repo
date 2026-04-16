"""Dash app: Pink Morsel sales from formatted_output.csv (Soul Foods)."""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html

DATA_PATH = Path(__file__).resolve().parent / "data" / "formatted_output.csv"
PRICE_CHANGE = pd.Timestamp("2021-01-15")


def load_daily_totals() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    totals = (
        df.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
        .rename(columns={"Sales": "TotalSales"})
    )
    return totals


def build_figure(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(
        data=go.Scatter(
            x=df["Date"],
            y=df["TotalSales"],
            mode="lines",
            name="Total daily sales",
            line=dict(color="#c2185b", width=2),
            hovertemplate="Date=%{x|%Y-%m-%d}<br>Total sales=$%{y:,.0f}<extra></extra>",
        )
    )
    fig.add_shape(
        type="line",
        xref="x",
        yref="paper",
        x0=PRICE_CHANGE,
        x1=PRICE_CHANGE,
        y0=0,
        y1=1,
        line=dict(color="#333333", width=2, dash="dash"),
    )
    fig.add_annotation(
        x=PRICE_CHANGE,
        xref="x",
        yref="paper",
        y=1.02,
        text="Pink Morsel price increase ($3 → $5)",
        showarrow=False,
        xanchor="left",
        font=dict(size=12),
    )
    fig.update_layout(
        margin=dict(l=48, r=24, t=56, b=48),
        plot_bgcolor="#fafafa",
        paper_bgcolor="#ffffff",
        hovermode="x unified",
        showlegend=False,
        yaxis=dict(gridcolor="#e0e0e0"),
        xaxis=dict(gridcolor="#e0e0e0"),
    )
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Total daily sales (USD)", tickformat=",.0f")
    return fig


def create_app() -> Dash:
    df = load_daily_totals()
    fig = build_figure(df)

    app = Dash(__name__)
    app.title = "Soul Foods — Pink Morsel Sales"

    app.layout = html.Div(
        style={
            "maxWidth": "1000px",
            "margin": "0 auto",
            "padding": "24px 20px 40px",
            "fontFamily": "system-ui, sans-serif",
        },
        children=[
            html.Header(
                style={"marginBottom": "20px"},
                children=[
                    html.H1(
                        "Soul Foods Pink Morsel Sales Visualiser",
                        style={"fontSize": "1.75rem", "marginBottom": "8px"},
                    ),
                    html.P(
                        "Daily revenue from Pink Morsels across all regions, "
                        "derived from combined transaction data.",
                        style={"color": "#444", "margin": 0},
                    ),
                ],
            ),
            dcc.Graph(id="sales-chart", figure=fig, config={"displayModeBar": True}),
        ],
    )
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
