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
        # Download full data (not just Adj Close)
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
                title=f"{selected_column} Comparison of {ticker1} vs {ticker2}",
                xaxis_title="Date", yaxis_title=selected_column,
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error: {e}")
