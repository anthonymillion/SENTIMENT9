import streamlit as st
import pandas as pd
import datetime

# -- Simulated Stock Data
stocks = sorted(set([
    "NVDA", "MSFT", "AAPL", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "AVGO", "COST", "AMD", "NFLX",
    "ABNB", "ADBE", "ADI", "ADP", "ADSK", "AEP", "AMAT", "AMGN", "APP", "ANSS", "ARM", "ASML", "AXON", "AZN",
    "BIIB", "BKNG", "BKR", "CCEP", "CDNS", "CDW", "CEG", "CHTR", "CMCSA", "CPRT", "CSGP", "CSCO", "CSX",
    "CTAS", "CTSH", "CRWD", "DASH", "DDOG", "DXCM", "EA", "EXC", "FAST", "FANG", "FTNT", "GEHC", "GILD",
    "GFS", "HON", "IDXX", "INTC", "INTU", "ISRG", "KDP", "KHC", "KLAC", "LIN", "LRCX", "LULU", "MAR",
    "MCHP", "MDLZ", "MELI", "MNST", "MRVL", "MSTR", "MU", "NXPI", "ODFL", "ON", "ORLY", "PANW", "PAYX",
    "PYPL", "PDD", "PEP", "PLTR", "QCOM", "REGN", "ROP", "ROST", "SHOP", "SBUX", "SNPS", "TTWO", "TMUS",
    "TXN", "TTD", "VRSK", "VRTX", "WBD", "WDAY", "XEL", "ZS"
]))

timeframes = ["1s", "5s", "15s", "30s", "M1", "M5", "M15", "M30", "1H", "4H", "Daily", "Weekly", "Monthly"]
selected_tf = st.sidebar.selectbox("Select Timeframe", timeframes, index=6)

# Simulate scoring
def simulate_score(symbol, tf):
    base = (hash(symbol + tf + str(datetime.date.today())) % 9) - 4
    return round(base + (hash(tf) % 3 - 1), 2)

def classify_sentiment(score):
    if score > 1.5:
        return "🟢 Bullish"
    elif score < -1.5:
        return "🔴 Bearish"
    return "🟡 Neutral"

# Build dataframe
df = pd.DataFrame([{
    "Symbol": sym,
    "Score": (s := simulate_score(sym, selected_tf)),
    "Sentiment": classify_sentiment(s)
} for sym in stocks])

# Sort: Bullish first, then Bearish, then Neutral
sentiment_order = {"🟢 Bullish": 0, "🔴 Bearish": 1, "🟡 Neutral": 2}
df["SortOrder"] = df["Sentiment"].map(sentiment_order)
df = df.sort_values(["SortOrder", "Score"], ascending=[True, False]).drop(columns=["SortOrder"])

# Layout
st.set_page_config(layout="wide")
st.title("📊 Stock Sentiment Dashboard")

st.markdown("### 🧠 AI Stock Sentiment – Sorted by Bullish > Bearish > Neutral")
st.dataframe(df, use_container_width=True)
