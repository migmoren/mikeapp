import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

st.title("📈 Stock Market Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
ticker = st.sidebar.text_input("Stock Ticker", value="AAPL")
start_date = st.sidebar.date_input("Start Date", value=date.today() - timedelta(days=365))
end_date = st.sidebar.date_input("End Date", value=date.today())
interval = st.sidebar.selectbox("Interval", ["1d", "1wk", "1mo"], index=0)

# Download data
@st.cache_data(ttl=86400)
def load_data(ticker, start, end, interval):
    data = yf.download(ticker, start=start, end=end, interval=interval, progress=False)
    data.reset_index(inplace=True)
    return data

if ticker:
    data = load_data(ticker, start_date, end_date + timedelta(days=1), interval)

    # Flatten MultiIndex columns if present
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]

    required_cols = {"Open", "High", "Low", "Close"}
    if not data.empty and required_cols.issubset(data.columns):
        data = data.dropna(subset=["Open", "High", "Low", "Close"])

        date_col = None
        for col in ["Date", "Datetime", "index"]:
            if col in data.columns:
                date_col = col
                break

        if date_col is None:
            x_axis = data.index
        else:
            x_axis = pd.to_datetime(data[date_col])

        if not data.empty:
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=x_axis,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlestick'
            ))
            fig.update_layout(xaxis_rangeslider_visible=False, height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for chart after cleaning. Try another ticker or date range.")

        # Data Table
        st.subheader("Historical Data")
        st.dataframe(data, use_container_width=True)

        # Export features
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f"{ticker}_data.csv",
            mime='text/csv'
        )
    else:
        st.warning("No OHLC data found for the selected ticker and date range. Please try another ticker or adjust the date range.")
else:
    st.info("Please enter a stock ticker symbol to begin.")