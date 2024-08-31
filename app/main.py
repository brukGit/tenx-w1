import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from datetime import datetime, timedelta
import yfinance as yf

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.indicators import TechnicalIndicators
from src.financial_metrics import FinancialMetrics

# Streamlit configuration
st.set_page_config(layout="wide", page_title="Stock Analysis Dashboard")

# Cache data loading and processing
@st.cache_data
def load_and_process_data(file_paths, market_index_path):
    # Load data
    loader = DataLoader(file_paths)
    data = loader.load_data()
    
    # Clean data
    cleaner = DataCleaner()
    cleaned_data = {ticker: cleaner.clean_data(df) for ticker, df in data.items()}
    
    # Ensure index is datetime
    for ticker, df in cleaned_data.items():
        df.index = pd.to_datetime(df.index)
    
    # Calculate indicators
    indicators = TechnicalIndicators(cleaned_data)
    indicators.calculate_moving_average()
    indicators.calculate_rsi()
    indicators.calculate_macd()
    
    # Calculate returns
    for ticker, df in cleaned_data.items():
        df['Returns'] = df['Close'].pct_change()
        df['Cumulative Returns'] = (1 + df['Returns']).cumprod()
    
    # Load market data
    market_data = pd.read_csv(market_index_path, index_col='Date', parse_dates=True)
    market_returns = market_data['Close'].pct_change().dropna()
    
    return cleaned_data, market_returns

# File paths
file_paths = [
    "../data/yfinance_data/AAPL_historical_data.csv",
    "../data/yfinance_data/AMZN_historical_data.csv",
    "../data/yfinance_data/GOOG_historical_data.csv",
    "../data/yfinance_data/META_historical_data.csv",
    "../data/yfinance_data/MSFT_historical_data.csv",
    "../data/yfinance_data/NVDA_historical_data.csv",
    "../data/yfinance_data/TSLA_historical_data.csv",
]
market_index_path = "../data/yfinance_data/SPY_historical_data.csv"

# Load and process data
data, market_returns = load_and_process_data(file_paths, market_index_path)

# Sidebar for user input
st.sidebar.title("Stock Analysis Dashboard")
ticker_selection = st.sidebar.selectbox("Select a stock", list(data.keys()))

# Date range selection
min_date = min(df.index.min() for df in data.values()).date()
max_date = max(df.index.max() for df in data.values()).date()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# Filter data based on date range
@st.cache_data
def filter_data(data, start_date, end_date):
    return {ticker: df[(df.index.date >= start_date) & (df.index.date <= end_date)] for ticker, df in data.items()}

filtered_data = filter_data(data, start_date, end_date)

# Main content
st.title("Stock Analysis Dashboard")

# Plot stock price and indicators
def plot_stock_indicators(ticker_data):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 16), sharex=True)
    
    ax1.plot(ticker_data.index, ticker_data['Close'], label='Close Price')
    ax1.plot(ticker_data.index, ticker_data['MA'], label='Moving Average')
    ax1.set_title(f'{ticker_selection} Stock Price and Indicators')
    ax1.set_ylabel('Price (USD)')
    ax1.legend()
    
    ax2.plot(ticker_data.index, ticker_data['RSI'], label='RSI')
    ax2.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')
    ax2.axhline(y=30, color='g', linestyle='--', label='Oversold (30)')
    ax2.set_ylabel('RSI')
    ax2.legend()
    
    ax3.plot(ticker_data.index, ticker_data['MACD'], label='MACD')
    ax3.plot(ticker_data.index, ticker_data['MACD_signal'], label='Signal Line')
    ax3.bar(ticker_data.index, ticker_data['MACD'] - ticker_data['MACD_signal'], label='MACD Histogram')
    ax3.set_ylabel('MACD')
    ax3.set_xlabel('Date')
    ax3.legend()
    
    plt.tight_layout()
    return fig

st.subheader("Stock Price and Technical Indicators")
fig = plot_stock_indicators(filtered_data[ticker_selection])
st.pyplot(fig)

# Plot returns comparison
def plot_returns_comparison(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    for ticker, stock_data in data.items():
        ax.plot(stock_data.index, stock_data['Cumulative Returns'], label=ticker)
    
    ax.set_title('Cumulative Returns Comparison')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Returns')
    ax.legend()
    return fig

st.subheader("Returns Comparison")
fig = plot_returns_comparison(filtered_data)
st.pyplot(fig)

# Correlation heatmap
def plot_correlation_heatmap(data):
    returns = pd.DataFrame({ticker: stock_data['Returns'] for ticker, stock_data in data.items()})
    corr_matrix = returns.corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0, ax=ax)
    ax.set_title('Correlation Heatmap of Stock Returns')
    return fig

st.subheader("Correlation Heatmap")
fig = plot_correlation_heatmap(filtered_data)
st.pyplot(fig)

# Financial metrics
@st.cache_data
def calculate_financial_metrics(data, market_returns):
    metrics = FinancialMetrics(data)
    sharpe_ratios = metrics.calculate_sharpe_ratio()
    volatilities = metrics.calculate_volatility()
    betas = metrics.calculate_beta(market_returns)
    
    metrics_df = pd.DataFrame({
        'Sharpe Ratio': sharpe_ratios,
        'Volatility': volatilities,
        'Beta': betas
    })
    return metrics_df

st.subheader("Financial Metrics")
metrics_df = calculate_financial_metrics(filtered_data, market_returns)
st.dataframe(metrics_df)

# Correlation between indicators and returns
def plot_indicator_returns_correlation(ticker_data):
    columns_of_interest = ['RSI', 'MA', 'MACD', 'MACD_signal', 'Close', 'Returns']
    corr_matrix = ticker_data[columns_of_interest].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0, ax=ax)
    ax.set_title(f'Correlation Heatmap for {ticker_selection}')
    return fig

st.subheader("Indicator-Returns Correlation")
fig = plot_indicator_returns_correlation(filtered_data[ticker_selection])
st.pyplot(fig)