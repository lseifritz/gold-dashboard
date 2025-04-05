
import pandas as pd
from datetime import datetime

def load_data():
    df = pd.read_csv("data.csv", names=["Date", "Price"])
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d %H:%M:%S")
    df["Price"] = df["Price"].astype(float)
    return df

df = load_data()

# Filtrer les données du jour
today = datetime.today().date()
df_today = df[df["Date"].dt.date == today]

if not df_today.empty:
    open_price = df_today["Price"].iloc[0]
    close_price = df_today["Price"].iloc[-1]
    volatility = df_today["Price"].std()

    report = f"""Report of {today} :
- Open : {open_price}
- Close : {close_price}
- Volatility : {volatility:.2f}
"""

    with open("report.txt", "w") as f:
        f.write(report)
else:
    with open("report.txt", "w") as f:
        f.write(f"No data available for {today}")
