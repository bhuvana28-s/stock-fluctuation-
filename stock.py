import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# ------------------ Streamlit Page Config ------------------
st.set_page_config(page_title="📈 NSE vs BSE Stock Comparison", layout="wide")

st.title("📊 NSE vs BSE Stock Comparison Dashboard")

# ------------------ Predefined Stock Lists ------------------
# NSE (suffix .NS for Yahoo Finance)
nse_stocks = {
    "Reliance Industries": "RELIANCE.NS",
    "Tata Consultancy Services": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "State Bank of India": "SBIN.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
    "Adani Enterprises": "ADANIENT.NS"
}

# BSE (suffix .BO for Yahoo Finance)
bse_stocks = {
    "Reliance Industries": "500325.BO",
    "Tata Consultancy Services": "532540.BO",
    "Infosys": "500209.BO",
    "HDFC Bank": "500180.BO",
    "ICICI Bank": "532174.BO",
    "State Bank of India": "500112.BO",
    "Bharti Airtel": "532454.BO",
    "Adani Enterprises": "512599.BO"
}

# ------------------ Sidebar Inputs ------------------
st.sidebar.header("🔧 Settings")

nse_choice = st.sidebar.selectbox("Select NSE Stock", list(nse_stocks.keys()), index=0)
bse_choice = st.sidebar.selectbox("Select BSE Stock", list(bse_stocks.keys()), index=1)

ticker1 = nse_stocks[nse_choice]
ticker2 = bse_stocks[bse_choice]

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# ------------------ Fetch & Process Data ------------------
if st.sidebar.button("Compare"):
    try:
        # Download all columns
        data = yf.download([ticker1, ticker2], start=start_date, end=end_date)

        if data.empty:
            st.error("⚠️ No data found. Check tickers or date range.")
        else:
            # ------------------ Data Preview ------------------
            st.subheader("📋 Stock Data (Last 10 Rows)")
            st.dataframe(data.tail(10))

            # ------------------ Select Column to Plot ------------------
            available_columns = data.columns.levels[0]  # ['Open','High','Low','Close','Adj Close','Volume']
            selected_column = st.selectbox("📌 Select Data Column to Plot", available_columns, index=4)

            # Extract the chosen column
            plot_data = data[selected_column]

            # ------------------ Plot ------------------
            st.subheader(f"📈 {selected_column} Comparison")
            fig = go.Figure()
            for ticker in plot_data.columns:
                fig.add_trace(go.Scatter(
                    x=plot_data.index, y=plot_data[ticker],
                    mode='lines', name=ticker
                ))
            fig.update_layout(
                title=f"{selected_column} Comparison ({nse_choice} vs {bse_choice})",
                xaxis_title="Date", yaxis_title=selected_column,
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error: {e}")
