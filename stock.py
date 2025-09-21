import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# ------------------ Streamlit Page Config ------------------
st.set_page_config(page_title="📈 Stock Comparison Dashboard", layout="wide")
st.title("📊 Stock Market Viewer & Comparison")

# ------------------ Define Stock Market & Tickers ------------------
stock_markets = {
    "NSE": {
        "Reliance Industries": "RELIANCE.NS",
        "Infosys": "INFY.NS",
        "Tata Consultancy Services": "TCS.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "ICICI Bank": "ICICIBANK.NS",
        "State Bank of India": "SBIN.NS",
        "Bharti Airtel": "BHARTIARTL.NS"
    },
    "BSE": {
        "Reliance Industries": "500325.BO",
        "Infosys": "500209.BO",
        "Tata Consultancy Services": "532540.BO",
        "HDFC Bank": "500180.BO",
        "ICICI Bank": "532174.BO",
        "State Bank of India": "500112.BO",
        "Bharti Airtel": "532454.BO"
    }
}

# ------------------ Sidebar Inputs ------------------
st.sidebar.header("🔧 Settings")

# Select Market
market = st.sidebar.selectbox("Select Stock Market", list(stock_markets.keys()))

# Select Stocks
stock_list = stock_markets[market]
ticker1_name = st.sidebar.selectbox("Select First Stock", list(stock_list.keys()), index=0)
ticker2_name = st.sidebar.selectbox("Select Second Stock", list(stock_list.keys()), index=1)

ticker1 = stock_list[ticker1_name]
ticker2 = stock_list[ticker2_name]

# Date Range
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# ------------------ Fetch & Process Data ------------------
if st.sidebar.button("Compare"):
    try:
        # Download stock data
        data = yf.download([ticker1, ticker2], start=start_date, end=end_date)

        if data.empty:
            st.error("⚠️ No data found. Check tickers or date range.")
        else:
            # Show Preview
            st.subheader("📋 Stock Data (Last 10 Rows)")
            st.dataframe(data.tail(10))

            # Select Column to Plot
            available_columns = data.columns.levels[0]  # ['Open','High','Low','Close','Adj Close','Volume']
            selected_column = st.selectbox("📌 Select Data Column to Plot", available_columns, index=4)

            # Extract chosen column
            plot_data = data[selected_column]

            # Plot Graph
            st.subheader(f"📈 {selected_column} Comparison")
            fig = go.Figure()
            for ticker in plot_data.columns:
                fig.add_trace(go.Scatter(
                    x=plot_data.index, y=plot_data[ticker],
                    mode='lines', name=ticker
                ))
            fig.update_layout(
                title=f"{selected_column} Comparison: {ticker1_name} vs {ticker2_name} ({market})",
                xaxis_title="Date", yaxis_title=selected_column,
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error: {e}")
