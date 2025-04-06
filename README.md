# Gold Live Dashboard

A real-time dashboard that tracks the price of gold, featuring technical indicators, key metrics, and an automatically generated daily report.

---

## Features

- **Live scraping** of gold prices every 5 minutes
- **Interactive chart** with:
  - Price
  - 48-period (4H) **Simple Moving Average (SMA)** in green
  - 48-period (4H) **Relative Strength Index (RSI)** in violet (on the same plot)
- **KPI Cards**:
  - Last Price
  - Price Change (with color and dynamic arrows 🔼🔽)
  - Volatility
  - Daily Max / Min
- **Daily Report** generated automatically at 8 PM and displayed on the dashboard

---

## Project Structure
<pre>
.
├── data.csv          # Scraped gold price data
├── report.txt        # Auto-generated daily report
├── scrapper.sh       # Bash script that scrapes gold price
├── rapport.py        # Generates the daily report from data.csv
└── dashboard.py      # Main Dash application 
</pre>
