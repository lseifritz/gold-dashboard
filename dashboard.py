import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
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

# Create the Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Gold Live Dashboard"

app.layout = html.Div([
    html.H1(
        "Prix Gold - Live Scraping"),
        dcc.Graph(id="price-graph"),
        dcc.Interval(
            id="interval-component",
            interval=5*1000,  # updates every 5 minutes
            n_intervals=0
        ),
    html.H2("Daily report"),  # generate the report
    html.Pre(id="daily-report", style={"whiteSpace": "pre-wrap", "fontFamily": "monospace"}),
    dcc.Interval(
        id="report-update",
        interval=10*60*1000,  # Update every 10 minutes
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
    })

# Update the plot
@app.callback(
    Output("price-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_graph(n):
    df = load_data()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Date"],
        y=df["Price"],
        mode="lines+markers",
        line=dict(color='gold'),
        marker=dict(color='gold')
    ))
    fig.update_layout(
        title="Live Price",
        xaxis_title="Date",
        yaxis_title="Price",
        paper_bgcolor='#2a2a2a',
        plot_bgcolor='#2a2a2a',
        font=dict(color='white')
    )
    return fig

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
