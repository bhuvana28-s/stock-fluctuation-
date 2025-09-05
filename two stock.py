import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# ------------------ Streamlit Page Config ------------------
st.set_page_config(page_title="📈 Stock Comparison Dashboard", layout="wide")

st.title("📊 Interactive Stock Comparison Dashboard")

# ------------------ Sidebar Inputs ------------------
st.sidebar.header("🔧 Settings")
ticker1 = st.sidebar.text_input("Enter First Stock Ticker", "AAPL")
ticker2 = st.sidebar.text_input("Enter Second Stock Ticker", "GOOGL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# ------------------ Fetch & Process Data ------------------
if st.sidebar.button("Compare"):
    try:
        # Download adjusted close prices
        data = yf.download([ticker1, ticker2], start=start_date, end=end_date)['Adj Close']

        if data.empty:
            st.error("⚠️ No data found. Check tickers or date range.")
        else:
            # ------------------ Data Preview ------------------
            st.subheader("📋 Stock Prices (Last 10 Rows)")
            st.dataframe(data.tail(10))

            # ------------------ Adjusted Close Prices ------------------
            st.subheader("📈 Adjusted Close Price Comparison")
            fig = go.Figure()
            for ticker in data.columns:
                fig.add_trace(go.Scatter(
                    x=data.index, y=data[ticker], mode='lines', name=ticker
                ))
            fig.update_layout(
                title="Adjusted Close Prices",
                xaxis_title="Date", yaxis_title="Price",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)

            # ------------------ Daily Returns ------------------
            returns = data.pct_change().dropna()
            st.subheader("📉 Daily Returns")
            fig = go.Figure()
            for ticker in returns.columns:
                fig.add_trace(go.Scatter(
                    x=returns.index, y=returns[ticker], mode='lines', name=f"{ticker} Daily Return"
                ))
            fig.update_layout(
                title="Daily Returns",
                xaxis_title="Date", yaxis_title="Return",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)

            # ------------------ Cumulative Returns ------------------
            cum_returns = (1 + returns).cumprod() - 1
            st.subheader("📊 Cumulative Returns")
            fig = go.Figure()
            for ticker in cum_returns.columns:
                fig.add_trace(go.Scatter(
                    x=cum_returns.index, y=cum_returns[ticker], mode='lines', name=f"{ticker} Cumulative Return"
                ))
            fig.update_layout(
                title="Cumulative Returns",
                xaxis_title="Date", yaxis_title="Cumulative Return",
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)

            # ------------------ Volatility ------------------
            volatility = returns.std()
            st.subheader("📌 Volatility (Standard Deviation of Daily Returns)")
            vol_table = pd.DataFrame(volatility, columns=["Volatility"]).T
            st.table(vol_table.style.format("{:.4f}"))

    except Exception as e:
        st.error(f"❌ Error: {e}")
