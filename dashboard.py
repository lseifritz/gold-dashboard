import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Charger les données
def load_data():
    try:
        df = pd.read_csv("data.csv", names=["Date", "Price"])
        df["Date"] = pd.to_datetime(df["Date"],format="%Y-%m-%d %H:%M:%S")
        df["Price"] = df["Price"].astype(float)
        return df
    except:
        return pd.DataFrame(columns=["Date", "Price"])

# Créer l'application Dash
app = dash.Dash(__name__)
app.title = "Gold Live Dashboard"

app.layout = html.Div([
    html.H1("Prix Gold - Live Scraping"),
    dcc.Graph(id="price-graph"),
    dcc.Interval(
        id="interval-component",
        interval=5*1000,  # 5 minutes
        n_intervals=0)])

# Mise à jour du graph
@app.callback(
    Output("price-graph", "figure"),
    Input("interval-component", "n_intervals")
)
def update_graph(n):
    df = load_data()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Price"], mode="lines+markers"))
    fig.update_layout(title="Prix en temps réel", xaxis_title="Date", yaxis_title="Prix")
    return fig

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
