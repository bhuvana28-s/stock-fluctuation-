import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

st.set_page_config(page_title="📈 Stock Comparison", layout="wide")

st.title("📊 Compare Two Stocks (Interactive with Plotly)")

# Sidebar inputs
ticker1 = st.sidebar.text_input("Enter First Stock Ticker", "AAPL")
ticker2 = st.sidebar.text_input("Enter Second Stock Ticker", "GOOGL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

if st.sidebar.button("Compare"):
    try:
        # Fetch data
        data = yf.download([ticker1, ticker2], start=start_date, end=end_date)['Adj Close']

        if data.empty:
            st.error("⚠️ No data found for given tickers/dates.")
        else:
            st.subheader("📋 Stock Prices (Last 10 Rows)")
            st.dataframe(data.tail(10))

            # Price trends
            st.subheader("📈 Adjusted Close Price Comparison")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data[ticker1], mode='lines', name=ticker1))
            fig.add_trace(go.Scatter(x=data.index, y=data[ticker2], mode='lines', name=ticker2))
            fig.update_layout(title="Adjusted Close Price Comparison", xaxis_title="Date", yaxis_title="Price", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

            # Daily returns
            returns = data.pct_change().dropna()
            st.subheader("📉 Daily Returns")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=returns.index, y=returns[ticker1], mode='lines', name=f"{ticker1} Daily Return"))
            fig.add_trace(go.Scatter(x=returns.index, y=returns[ticker2], mode='lines', name=f"{ticker2} Daily Return"))
            fig.update_layout(title="Daily Returns", xaxis_title="Date", yaxis_title="Return", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

            # Cumulative returns
            cum_returns = (1 + returns).cumprod() - 1
            st.subheader("📊 Cumulative Returns")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=cum_returns.index, y=cum_returns[ticker1], mode='lines', name=f"{ticker1} Cumulative Return"))
            fig.add_trace(go.Scatter(x=cum_returns.index, y=cum_returns[ticker2], mode='lines', name=f"{ticker2} Cumulative Return"))
            fig.update_layout(title="Cumulative Returns", xaxis_title="Date", yaxis_title="Cumulative Return", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

            # Volatility
            volatility = returns.std()
            st.subheader("📌 Volatility (Std Dev of Daily Returns)")
            st.write(f"{ticker1}: {volatility[ticker1]:.4f}")
            st.write(f"{ticker2}: {volatility[ticker2]:.4f}")

    except Exception as e:
        st.error(f"❌ Error: {e}")
