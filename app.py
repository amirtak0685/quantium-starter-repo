"""Dash app: Pink Morsel sales from formatted_output.csv (Soul Foods)."""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

DATA_PATH = Path(__file__).resolve().parent / "data" / "formatted_output.csv"
PRICE_CHANGE = pd.Timestamp("2021-01-15")


def load_data() -> pd.DataFrame:
    """Load per-region sales and add a total-across-regions view."""
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    # Add a synthetic "all" region that sums across regions for each date.
    daily_totals = (
        df.groupby("Date", as_index=False)["Sales"]
        .sum()
        .assign(Region="all")
        .rename(columns={"Sales": "TotalSales"})
    )
    per_region = df.rename(columns={"Sales": "TotalSales"})
    combined = pd.concat(
        [per_region, daily_totals], ignore_index=True, sort=False
    ).sort_values(["Region", "Date"])
    return combined


def build_figure(df: pd.DataFrame, region: str) -> go.Figure:
    """Build line chart for a given region or all regions."""
    if region == "all":
        filtered = (
            df[df["Region"] == "all"]
            .sort_values("Date")
        )
        title_suffix = "All regions"
    else:
        filtered = (
            df[df["Region"].str.lower() == region.lower()]
            .sort_values("Date")
        )
        title_suffix = f"{region.capitalize()} region"

    fig = go.Figure(
        data=go.Scatter(
            x=filtered["Date"],
            y=filtered["TotalSales"],
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
        title=dict(
            text=f"Pink Morsel daily sales — {title_suffix}",
            x=0.01,
            xanchor="left",
            font=dict(size=16),
        ),
    )
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Total daily sales (USD)", tickformat=",.0f")
    return fig


def create_app() -> Dash:
    df = load_data()

    app = Dash(__name__)
    app.title = "Soul Foods — Pink Morsel Sales"

    app.layout = html.Div(
        style={
            "maxWidth": "1100px",
            "margin": "0 auto",
            "padding": "28px 22px 44px",
            "fontFamily": "system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
            "background": "linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%)",
        },
        children=[
            html.Header(
                style={
                    "marginBottom": "20px",
                    "paddingBottom": "12px",
                    "borderBottom": "1px solid #ddd",
                },
                children=[
                    html.H1(
                        "Soul Foods Pink Morsel Sales Visualiser",
                        style={"fontSize": "1.9rem", "marginBottom": "6px"},
                    ),
                    html.P(
                        "Explore Pink Morsel daily revenue before and after the "
                        "January 15, 2021 price change.",
                        style={"color": "#444", "margin": 0},
                    ),
                ],
            ),
            html.Section(
                style={
                    "display": "flex",
                    "flexWrap": "wrap",
                    "gap": "16px",
                    "alignItems": "center",
                    "marginBottom": "12px",
                    "padding": "10px 12px",
                    "backgroundColor": "#ffffff",
                    "borderRadius": "10px",
                    "boxShadow": "0 1px 3px rgba(15, 23, 42, 0.08)",
                },
                children=[
                    html.Div(
                        children=[
                            html.Span(
                                "Region filter:",
                                style={
                                    "fontWeight": 600,
                                    "marginRight": "10px",
                                    "fontSize": "0.9rem",
                                },
                            ),
                            dcc.RadioItems(
                                id="region-filter",
                                options=[
                                    {"label": "All", "value": "all"},
                                    {"label": "North", "value": "north"},
                                    {"label": "East", "value": "east"},
                                    {"label": "South", "value": "south"},
                                    {"label": "West", "value": "west"},
                                ],
                                value="all",
                                labelStyle={
                                    "display": "inline-block",
                                    "marginRight": "10px",
                                    "padding": "4px 8px",
                                    "borderRadius": "999px",
                                    "cursor": "pointer",
                                },
                                inputStyle={"marginRight": "4px"},
                                style={"fontSize": "0.9rem"},
                            ),
                        ]
                    )
                ],
            ),
            html.Div(
                style={
                    "backgroundColor": "#ffffff",
                    "borderRadius": "12px",
                    "padding": "8px 10px 4px",
                    "boxShadow": "0 4px 10px rgba(15, 23, 42, 0.10)",
                },
                children=[
                    dcc.Graph(
                        id="sales-chart",
                        figure=build_figure(df, region="all"),
                        config={"displayModeBar": True},
                        style={"height": "520px"},
                    )
                ],
            ),
        ],
    )

    @app.callback(
        Output("sales-chart", "figure"),
        Input("region-filter", "value"),
    )
    def update_chart(selected_region: str):
        return build_figure(df, region=selected_region)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
