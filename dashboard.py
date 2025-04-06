import pandas as pd
import dash
from dash import dcc, html
from dash import no_update
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

# Load the data
def load_data():
    try:
        df = pd.read_csv("data.csv", names=["Date", "Price"])
        df["Date"] = pd.to_datetime(df["Date"],format="%Y-%m-%d %H:%M:%S")
        df["Price"] = df["Price"].astype(float)
        return df
    except:
        return pd.DataFrame(columns=["Date", "Price"])

# Compute our RSI indicator
def compute_rsi(series, period=48):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Create the Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Gold Live Dashboard"
app.layout = html.Div(
    [
        html.H1("Gold Price - Live Scraping"),
        html.H6("Gold Live Dashboard updated every 5 minutes",
            style={
                "color": "gray",
                "fontStyle": "italic",
                "marginTop": "-10px",
                "marginBottom": "20px"
        }),
        dbc.Row([
            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H5("Last Price", className="card-title"),
                    html.H2(id="last-price", className="card-text")
                ]),
                style={
                    "backgroundColor": "#2b2b2b",
                    "borderRadius": "10px",
                    "boxShadow": "0 4px 8px rgba(255, 215, 0, 0.2)"
                }
            ), width=4),

            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H5("Change", className="card-title"),
                    html.H2(id="price-change", className="card-text")
                ]),
                style={
                    "backgroundColor": "#2b2b2b",
                    "borderRadius": "10px",
                    "boxShadow": "0 4px 8px rgba(255, 215, 0, 0.2)"
                }
            ), width=4),

            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H5("Volatility", className="card-title"),
                    html.H2(id="volatility", className="card-text")
                ]),
                style={
                    "backgroundColor": "#2b2b2b",
                    "borderRadius": "10px",
                    "boxShadow": "0 4px 8px rgba(255, 215, 0, 0.2)"
                }
            ), width=4)
        ], className="mb-4"),

        dcc.Graph(id="price-graph"),

        dcc.Interval(
            id="interval-component",
            interval=5 * 60 * 1000,  # updates every 5 minutes
            n_intervals=0
        ),

        dbc.Row([
            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H5("Max Price", className="card-title"),
                    html.H2(id="max-price", className="card-text")
                ]),
                style={
                    "backgroundColor": "#2b2b2b",
                    "borderRadius": "10px",
                    "boxShadow": "0 4px 8px rgba(255, 215, 0, 0.2)"
                }
            ), width=4),

            dbc.Col(dbc.Card(
                dbc.CardBody([
                    html.H5("Min Price", className="card-title"),
                    html.H2(id="min-price", className="card-text")
                ]),
                style={
                    "backgroundColor": "#2b2b2b",
                    "borderRadius": "10px",
                    "boxShadow": "0 4px 8px rgba(255, 215, 0, 0.2)"
                }
            ), width=4)
        ]),

        html.H2("Daily report"),  # generate the report
        html.Pre(id="daily-report", style={
            "whiteSpace": "pre-wrap",
            "fontFamily": "monospace"
        }),

        dcc.Interval(
            id="report-update",
            interval=10 * 60 * 1000,  # Update every 10 minutes
            n_intervals=0
        )
    ],
    style={
        "backgroundColor": "#1a1a1a",
        "padding": "20px",
        "borderRadius": "15px",
        "boxShadow": "0 4px 10px rgba(0, 0, 0, 0.5)",
        "fontFamily": "Arial, sans-serif",
        "color": "white"
    }
)

@app.callback(
    [
        Output("price-graph", "figure"),
        Output("last-price", "children"),
        Output("price-change", "children"),
        Output("volatility", "children"),
        Output("max-price", "children"),
        Output("min-price", "children"),
    ],
    Input("interval-component", "n_intervals")
)

# Update the Graph
def update_graph(n):
    df = load_data()

    if df.empty:
        return go.Figure(), "-", "-", "-", "-", "-"

    # SMA (moving average)
    df["SMA"] = df["Price"].rolling(window=48).mean()

    # RSI
    df["RSI"] = compute_rsi(df["Price"])

    # KPIs
    last_price = f"{df['Price'].iloc[-1]:.2f}" if not df.empty else "-"

    raw_change = df['Price'].iloc[-1] - df['Price'].iloc[0] if len(df) >= 2 else None
    if raw_change is not None:
        arrow = "⬆️" if raw_change > 0 else "⬇️"
        color = "green" if raw_change > 0 else "red"
        price_change = html.Div([
            html.Span(arrow, style={"color": color, "marginRight": "6px"}),
            html.Span(f"{raw_change:+.2f}", style={"color": color, "fontWeight": "bold"})
        ])
    else:
        price_change = "-"
    volatility = f"{df['Price'].std():.2f}" if not df.empty else "-"
    max_price = f"{df['Price'].max():.2f}" if not df.empty else "-"
    min_price = f"{df['Price'].min():.2f}" if not df.empty else "-"

    # Graph with two subplots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.7, 0.3],
                        vertical_spacing=0.05,
                        subplot_titles=("Gold Price", "RSI (4H)"))

    # Price with SMA
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Price"],
                             mode="lines+markers", name="Price",
                             line=dict(color="yellow")),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=df["Date"], y=df["SMA"],
                             mode="lines", name="SMA (4H)",
                             line=dict(color="lime")),
                  row=1, col=1)

    # RSI plot
    fig.add_trace(go.Scatter(x=df["Date"], y=df["RSI"],
                             mode="lines", name="RSI (4H)",
                             line=dict(color="purple")),
                  row=2, col=1)

    # Add 30/70 lines to the RSI plot
    fig.add_shape(type="line", x0=df["Date"].min(), x1=df["Date"].max(),
                  y0=70, y1=70, line=dict(dash="dash", color="gray"), row=2, col=1)
    fig.add_shape(type="line", x0=df["Date"].min(), x1=df["Date"].max(),
                  y0=30, y1=30, line=dict(dash="dash", color="gray"), row=2, col=1)

    # Layout
    fig.update_layout(
        height=600,
        paper_bgcolor="#1e1e1e",
        plot_bgcolor="#1e1e1e",
        font=dict(color="white"),
        showlegend=True
    )
    return fig, last_price, price_change, volatility, max_price, min_price

@app.callback(
    Output("daily-report", "children"),
    Input("report-update", "n_intervals")
)

def update_daily_report(n):
    return read_daily_report()

def read_daily_report():
    try:
        with open("report.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Report unavailable."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
