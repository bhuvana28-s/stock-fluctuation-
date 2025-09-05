import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

st.set_page_config(page_title="📈 Stock Comparison Viewer", layout="wide")

st.title("📊 Stock Data Viewer & Comparison")

# Sidebar: Market selection
market = st.sidebar.selectbox(
    "Select Market",
    ["US Market", "Indian Market", "Crypto"]
)

if market == "US Market":
    default_tickers = ["AAPL", "MSFT", "GOOGL", "TSLA"]
elif market == "Indian Market":
    default_tickers = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "TATASTEEL.NS", "HONOR.NS"]
else:
    default_tickers = ["BTC-USD", "ETH-USD", "DOGE-USD"]

tickers = st.sidebar.multiselect(
    "Select Tickers to Compare",
    options=default_tickers,
    default=default_tickers[:2]
)

# Sidebar: Time controls
period = st.sidebar.selectbox(
    "Select Period",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"],
    index=1
)
interval = st.sidebar.selectbox(
    "Select Interval",
    ["1d", "1wk", "1mo"],
    index=0
)

if tickers:
    try:
        df = yf.download(tickers, period=period, interval=interval, progress=False)

        if df.empty:
            st.error("⚠️ No data found. Try different tickers or period/interval.")
        else:
            # Flatten MultiIndex columns if multiple tickers
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [' '.join(col).strip() for col in df.columns.values]

            # Show full table
            st.subheader("📋 Full Stock Data Table")
            st.dataframe(df.tail(10))  # last 10 rows

            # Dynamically detect available columns
            available_columns = [col for col in df.columns if any(key in col for key in ["Open","High","Low","Close","Adj Close","Volume"])]

            # Sidebar: column selection based on actual data
            column_to_plot = st.sidebar.selectbox(
                "Select Data Column to Plot",
                available_columns
            )

            # Plot graph
            fig = go.Figure()
            if isinstance(df[column_to_plot], pd.DataFrame):  # multiple tickers
                for col in df[column_to_plot].columns:
                    fig.add_trace(go.Scatter(
                        x=df.index,
                        y=df[column_to_plot][col],
                        mode="lines",
                        name=col
                    ))
            else:  # single ticker
                fig.add_trace(go.Scatter(
                    x=df.index,
                    y=df[column_to_plot],
                    mode="lines",
                    name=column_to_plot
                ))

            fig.update_layout(
                title=f"{column_to_plot} Over Time",
                xaxis_title="Date",
                yaxis_title=column_to_plot,
                template="plotly_dark",
                legend=dict(x=0, y=1, bgcolor="rgba(0,0,0,0)")
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")

