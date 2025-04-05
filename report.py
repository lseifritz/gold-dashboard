
import pandas as pd
from datetime import datetime

def load_data():
    df = pd.read_csv("data.csv", names=["Date", "Price"])
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d %H:%M:%S")
    df["Price"] = df["Price"].astype(float)
    return df

df = load_data()
