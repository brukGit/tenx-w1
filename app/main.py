# app/main.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.data_loader import DataLoader
from src.data_cleaner import DataCleaner
from src.indicators import TechnicalIndicators
from src.financial_metrics import FinancialMetrics

# Optimize Streamlit configuration
st.set_page_config(layout="wide")

@st.cache_data
def load_stock_data(file_paths):
    loader = DataLoader(file_paths)
    data = loader.load_data()
    cleaner = DataCleaner()
    cleaned_data = {ticker: cleaner.clean_data(df) for ticker, df in data.items()}
    return cleaned_data

@st.cache_data
def calculate_indicators(data):
    indicators = TechnicalIndicators(data)
    indicators.calculate_moving_average()
    indicators.calculate_rsi()
    indicators.calculate_macd()
    return data

@st.cache_data
def calculate_returns(data):
    for ticker in data.keys():
        data[ticker]['Returns'] = data[ticker]['Close'].pct_change()
        data[ticker]['Cumulative Returns'] = (1 + data[ticker]['Returns']).cumprod()
    return data

@st.cache_data
def load_market_data(market_index_path):
    market_data = pd.read_csv(market_index_path, index_col='Date', parse_dates=True)
    market_returns = market_data['Close'].pct_change().dropna()
    return market_returns

@st.cache_data
def filter_data(df, start_date, end_date):
    return df[(df.index >= start_date) & (df.index <= end_date)]

def plot_stock_price(data, ticker):
    stock_data = data[ticker]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    ax1.plot(stock_data.index, stock_data['Close'], label='Close Price')
    ax1.set_title(f'{ticker} Stock Price and Volume')
    ax1.set_ylabel('Price')
    ax1.legend()
    
    ax2.bar(stock_data.index, stock_data['Volume'], label='Volume')
    ax2.set_ylabel('Volume')
    ax2.set_xlabel('Date')
    ax2.legend()
    
    plt.tight_layout()
    return fig

def plot_technical_indicators(data, ticker):
    stock_data = data[ticker]
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    
    ax1.plot(stock_data.index, stock_data['Close'], label='Close Price')
    ax1.plot(stock_data.index, stock_data['MA_50'], label='50-day MA')
    ax1.set_title(f'{ticker} Technical Indicators')
    ax1.set_ylabel('Price')
    ax1.legend()
    
    ax2.plot(stock_data.index, stock_data['RSI'], label='RSI')
    ax2.axhline(y=70, color='r', linestyle='--', label='Overbought (70)')
    ax2.axhline(y=30, color='g', linestyle='--', label='Oversold (30)')
    ax2.set_ylabel('RSI')
    ax2.legend()
    
    ax3.plot(stock_data.index, stock_data['MACD'], label='MACD')
    ax3.plot(stock_data.index, stock_data['Signal'], label='Signal Line')
    ax3.bar(stock_data.index, stock_data['MACD_hist'], label='MACD Histogram')
    ax3.set_ylabel('MACD')
    ax3.set_xlabel('Date')
    ax3.legend()
    
    plt.tight_layout()
    return fig

def plot_returns_comparison(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    for ticker, stock_data in data.items():
        ax.plot(stock_data.index, stock_data['Cumulative Returns'], label=ticker)
    
    ax.set_title('Cumulative Returns Comparison')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Returns')
    ax.legend()
    return fig

def plot_correlation_heatmap(data):
    returns = pd.DataFrame({ticker: stock_data['Returns'] for ticker, stock_data in data.items()})
    corr_matrix = returns.corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0, ax=ax)
    ax.set_title('Correlation Heatmap of Stock Returns')
    return fig

def app():
    st.title("Stock Analysis Dashboard")
    st.write("This dashboard analyzes stock data for multiple companies.")
    st.write(("Link to GitHub repo: [https://github.com/brukGit/tenx-w1/tree/task-2](https://github.com/brukGit/tenx-w1/tree/task-2)"))

    # File paths (you may need to adjust these based on your project structure)
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
    data = load_stock_data(file_paths)
    data = calculate_indicators(data)
    data = calculate_returns(data)
    market_returns = load_market_data(market_index_path)

    # Create three columns
    left_column, middle_column, right_column = st.columns([1, 2, 2])

    # Left column for navigation
    with left_column:
        st.subheader("Navigation")
        ticker_selection = st.selectbox("Select a stock", list(data.keys()))
        
        min_date = min(df.index.min() for df in data.values())
        max_date = max(df.index.max() for df in data.values())
        
        st.write("Select Date Range:")
        start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
        end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date)
        
        all_time = st.checkbox("Select All Time Range")
        
        if all_time:
            start_date = min_date
            end_date = max_date

    if ticker_selection:
        filtered_data = {ticker: filter_data(df, pd.Timestamp(start_date), pd.Timestamp(end_date)) for ticker, df in data.items()}
        
        # Middle column for summary statistics and plots
        with middle_column:
            st.subheader(f"Summary Statistics - {ticker_selection}")
            st.dataframe(filtered_data[ticker_selection].describe())
            
            st.subheader("Stock Price and Volume")
            if st.button("Generate Stock Price Plot"):
                price_fig = plot_stock_price(filtered_data, ticker_selection)
                st.pyplot(price_fig)
            
            st.subheader("Technical Indicators")
            if st.button("Generate Technical Indicators Plot"):
                indicators_fig = plot_technical_indicators(filtered_data, ticker_selection)
                st.pyplot(indicators_fig)

        # Right column for comparison plots
        with right_column:
            st.subheader("Returns Comparison")
            if st.button("Generate Returns Comparison"):
                returns_fig = plot_returns_comparison(filtered_data)
                st.pyplot(returns_fig)
            
            st.subheader("Correlation Heatmap")
            if st.button("Generate Correlation Heatmap"):
                heatmap_fig = plot_correlation_heatmap(filtered_data)
                st.pyplot(heatmap_fig)
            
            st.subheader("Financial Metrics")
            if st.button("Calculate Financial Metrics"):
                metrics = FinancialMetrics(filtered_data)
                sharpe_ratios = metrics.calculate_sharpe_ratio()
                volatilities = metrics.calculate_volatility()
                betas = metrics.calculate_beta(market_returns)
                
                metrics_df = pd.DataFrame({
                    'Sharpe Ratio': sharpe_ratios,
                    'Volatility': volatilities,
                    'Beta': betas
                })
                st.dataframe(metrics_df)

if __name__ == "__main__":
    app()