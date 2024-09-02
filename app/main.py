import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
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

def fetch_stock_data(tickers, start_date, end_date):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        data[ticker] = stock.history(start=start_date, end=end_date)
    return data

def fetch_market_index(index_ticker, start_date, end_date):
    index = yf.Ticker(index_ticker)
    return index.history(start=start_date, end=end_date)

# Function Definitions
@st.cache_data
def load_and_process_data(tickers, index_ticker, start_date, end_date):
    # Load data
    # Fetch stock data
    loader = DataLoader(tickers, start_date, end_date)
    loader_spy = DataLoader(index_ticker, start_date, end_date)

    data = loader.load_data()
    data_spy = loader_spy.load_data()
       
      
    # Clean data
    cleaner = DataCleaner()
    cleaned_data = {ticker: cleaner.clean_data(df) for ticker, df in data.items()}
    cleaned_data_spy = {ticker: cleaner.clean_data(df) for ticker, df in data_spy.items()}
    # Ensure index is datetime
    for ticker, df in cleaned_data.items():
        df.index = pd.to_datetime(df['Date'])
    for ticker, df in cleaned_data_spy.items():
        df.index = pd.to_datetime(df['Date'])
    
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
    # market_data = pd.read_csv(market_index_path, index_col='Date', parse_dates=True)
    market_returns = data_spy['SPY']['Close'].pct_change().dropna()
    
   
       
    return cleaned_data, market_returns

@st.cache_data
def filter_data(data, start_date, end_date):
    return {ticker: df[(df.index.date >= start_date) & (df.index.date <= end_date)] for ticker, df in data.items()}

@st.cache_data
def create_comparative_plots_per_ticker(data, ticker_selection):
    # Prepare data
    data = data[ticker_selection]
    stats = data[['RSI', 'MA', 'MACD', 'MACD_signal']].describe().loc[['mean', 'std']]
    
    # Set up the plot style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # 1. Bar Plot with Error Bars
    fig1, ax = plt.subplots(figsize=(10, 6))
    fig1.suptitle('Technical Indicators Statistics', fontsize=16, color='#E0E0E0')
    fig1.patch.set_facecolor('#2C2C2C')

    indicators = ['RSI', 'MA', 'MACD', 'MACD_signal']
    means = stats.loc['mean', indicators]
    stds = stats.loc['std', indicators]
    x = range(len(means))
    
    ax.bar(x, means.values, yerr=stds.values, capsize=5, color='#BB86FC')
    ax.set_title('Mean with Standard Deviation', color='#E0E0E0')
    ax.set_ylabel('Value', color='#E0E0E0')
    ax.set_xticks(x)
    ax.set_xticklabels(indicators, rotation=45, ha='right', color='#E0E0E0')
    
    ax.set_facecolor('#1E1E1E')
    ax.tick_params(colors='#E0E0E0')

    plt.tight_layout()
    
    # 2. Box Plot
    fig2, ax1 = plt.subplots(figsize=(10, 6))
    fig2.suptitle('Distribution of Technical Indicators', fontsize=16, color='#E0E0E0')
    fig2.patch.set_facecolor('#2C2C2C')
    
   
    # Prepare data for the boxplot
    data_melted = pd.melt(data[indicators].reset_index(drop=True), var_name='Indicator', value_name='Value')

    
    sns.boxplot(x='Indicator', y='Value', data=data_melted, ax=ax1, palette='coolwarm')

    # Customize the plot
    ax1.set_ylabel('Value', color='#E0E0E0')
    ax1.set_xlabel('Indicator', color='#E0E0E0')
    
    ax1.set_facecolor('#1E1E1E')
    ax1.tick_params(colors='#E0E0E0')

    plt.tight_layout()

    return fig1, fig2

def create_comparative_plots(data):
    # Prepare data
    stats = {}
    for ticker, df in data.items():
        stats[ticker] = df[['RSI', 'MA', 'MACD', 'MACD_signal']].describe().loc[['mean', 'std']]
    
    combined_stats = pd.concat(stats, axis=1)

    # Set up the figure and axes
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    fig.patch.set_facecolor('#2C2C2C')
    fig.suptitle('Comparative Technical Indicators Across Stocks', fontsize=16, color='#E0E0E0')

    indicators = ['RSI', 'MA', 'MACD', 'MACD_signal']
    colors = ['#BB86FC', '#03DAC6', '#FF0266', '#CF6679']

    for i, indicator in enumerate(indicators):
        ax = axes[i // 2, i % 2]
        means = combined_stats.loc['mean', (slice(None), indicator)]
        stds = combined_stats.loc['std', (slice(None), indicator)]
        x = range(len(means))
        ax.bar(x, means.values, yerr=stds.values, capsize=5, color=colors[i])
        ax.set_title(f'{indicator} - Mean with Standard Deviation', color='#E0E0E0')
        ax.set_ylabel('Value', color='#E0E0E0')
        ax.set_xticks(x)
        ax.set_xticklabels(means.index.get_level_values(0), rotation=45, ha='right')
        ax.set_facecolor('#1E1E1E')
        ax.tick_params(colors='#E0E0E0')

    plt.tight_layout()

    # Box Plot
    fig2, ax1 = plt.subplots(figsize=(15, 8))
    fig2.patch.set_facecolor('#2C2C2C')
    fig2.suptitle('Distribution of Technical Indicators Across Stocks', fontsize=16, color='#E0E0E0')

    # Prepare data for the box plot
    data_melted = pd.melt(pd.concat([df[indicators].assign(Ticker=ticker) for ticker, df in data.items()]), 
                          id_vars=['Ticker'], var_name='Indicator', value_name='Value')
    
    # Create a secondary y-axis
    ax2 = ax1.twinx()

    # Plot RSI and MA on primary y-axis
    sns.boxplot(x='Indicator', y='Value', hue='Ticker', 
                data=data_melted[data_melted['Indicator'].isin(['RSI', 'MA'])], 
                ax=ax1, palette=[colors[0], colors[1]])
    
    # Plot MACD and MACD_signal on secondary y-axis
    sns.boxplot(x='Indicator', y='Value', hue='Ticker', 
                data=data_melted[data_melted['Indicator'].isin(['MACD', 'MACD_signal'])], 
                ax=ax2, palette=[colors[2], colors[3]])

    # Customize the plot
    ax1.set_ylabel('RSI and MA Values', color=colors[0])
    ax2.set_ylabel('MACD and MACD_signal Values', color=colors[2])
    ax1.legend(title='Ticker', bbox_to_anchor=(1.05, 1), loc='upper left', facecolor='#2C2C2C', edgecolor='#BB86FC', labelcolor='#E0E0E0')
    ax2.legend_.remove()  # Remove the second legend
    ax1.set_facecolor('#1E1E1E')
    ax1.tick_params(colors='#E0E0E0')
    ax2.tick_params(colors=colors[2])

    plt.xticks(range(4), ['RSI', 'MA', 'MACD', 'MACD_signal'], color='#E0E0E0')
    
    plt.tight_layout()

    return fig, fig2


@st.cache_data
def plot_stock_indicators(ticker_data, ticker_selection):
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 16), sharex=True)
    fig.patch.set_facecolor('#2C2C2C')
    
    ax1.plot(ticker_data.index, ticker_data['Close'], label='Close Price', color='#BB86FC')
    ax1.plot(ticker_data.index, ticker_data['MA'], label='Moving Average', color='#03DAC6')
    ax1.set_title(f'{ticker_selection} Stock Price and Indicators', color='#E0E0E0')
    ax1.set_ylabel('Price (USD)', color='#E0E0E0')
    ax1.legend(facecolor='#2C2C2C', edgecolor='#BB86FC', labelcolor='#E0E0E0')
    ax1.set_facecolor('#1E1E1E')
    ax1.tick_params(colors='#E0E0E0')

   
    
    ax2.plot(ticker_data.index, ticker_data['Close'], label='Close Price', color='#BB86FC')
    ax2.plot(ticker_data.index, ticker_data['RSI'], label='RSI', color='#CF6679')
    ax2.axhline(y=70, color='#03DAC6', linestyle='--', label='Overbought (70)')
    ax2.axhline(y=30, color='#03DAC6', linestyle='--', label='Oversold (30)')
    ax2.set_ylabel('Price (USD)', color='#E0E0E0')
    ax2.legend(facecolor='#2C2C2C', edgecolor='#BB86FC', labelcolor='#E0E0E0')
    ax2.set_facecolor('#1E1E1E')
    ax2.tick_params(colors='#E0E0E0')
    
     # Secondary y-axis on ax1 (RSI)
    ax2b = ax2.twinx()
    ax2b.plot(ticker_data.index, ticker_data['RSI'], label='RSI', color='#FF0266')
    ax2b.set_ylabel('RSI', color='#FF0266')
    ax2b.tick_params(colors='#FF0266')


    ax3.plot(ticker_data.index, ticker_data['Close'], label='Close Price', color='#BB86FC')
    ax3.plot(ticker_data.index, ticker_data['MACD'], label='MACD', color='#BB86FC')
    ax3.plot(ticker_data.index, ticker_data['MACD_signal'], label='Signal Line', color='#03DAC6')
    ax3.bar(ticker_data.index, ticker_data['MACD'] - ticker_data['MACD_signal'], label='MACD Histogram', color='#CF6679')
    ax3.set_ylabel('Price (USD)', color='#E0E0E0')
    ax3.set_xlabel('Date', color='#E0E0E0')
    ax3.legend(facecolor='#2C2C2C', edgecolor='#BB86FC', labelcolor='#E0E0E0')
    ax3.set_facecolor('#1E1E1E')
    ax3.tick_params(colors='#E0E0E0')

         # Secondary y-axis on ax1 (RSI)
    ax3b = ax3.twinx()
    ax3b.plot(ticker_data.index, ticker_data['RSI'], label='RSI', color='#FF0266')
    ax3b.set_ylabel('MACD, MACD Signal, MACD Histogram', color='#FF0266')
    ax3b.tick_params(colors='#FF0266')
    
    plt.tight_layout()
    return fig
@st.cache_data
def plot_returns_comparison(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#2C2C2C')
    ax.set_facecolor('#1E1E1E')
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(data)))
    for (ticker, stock_data), color in zip(data.items(), colors):
        ax.plot(stock_data.index, stock_data['Cumulative Returns'], label=ticker, color=color)
    
    ax.set_title('Cumulative Returns Comparison', color='#E0E0E0')
    ax.set_xlabel('Date', color='#E0E0E0')
    ax.set_ylabel('Cumulative Returns', color='#E0E0E0')
    ax.legend(facecolor='#2C2C2C', edgecolor='#BB86FC', labelcolor='#E0E0E0')
    ax.tick_params(colors='#E0E0E0')
    return fig
@st.cache_data
def plot_correlation_heatmap(data):
    returns = pd.DataFrame({ticker: stock_data['Returns'] for ticker, stock_data in data.items()})
    corr_matrix = returns.corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor('#2C2C2C')
    
    heatmap = sns.heatmap(corr_matrix, annot=True, cmap='viridis', vmin=-1, vmax=1, center=0, ax=ax,
                cbar_kws={'label': 'Correlation'},
                annot_kws={'color': '#E0E0E0'})
    
    ax.set_title('Correlation Heatmap of Stock Returns', color='#E0E0E0')
    ax.tick_params(colors='#E0E0E0')

    # Style the colorbar label
    cbar = heatmap.collections[0].colorbar
    cbar.set_label('Correlation', color='#E0E0E0')
    cbar.ax.yaxis.set_tick_params(color='#E0E0E0')
    cbar.outline.set_edgecolor('#E0E0E0')
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='#E0E0E0')

    return fig

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

def plot_indicator_returns_correlation(ticker_data, ticker_selection):
    columns_of_interest = ['RSI', 'MA', 'MACD', 'MACD_signal', 'Close', 'Returns']
    corr_matrix = ticker_data[columns_of_interest].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor('#2C2C2C')
    
    sns.heatmap(corr_matrix, annot=True, cmap='viridis', vmin=-1, vmax=1, center=0, ax=ax,
                cbar_kws={'label': 'Correlation'},
                annot_kws={'color': '#E0E0E0'})
    
    ax.set_title(f'Correlation Heatmap for {ticker_selection}', color='#E0E0E0')
    ax.tick_params(colors='#E0E0E0')
    return fig

# Main App
def main():
    

    # Custom CSS for dark mode styling and layout
    st.markdown("""
    <style>
        /* Main page background */
        .stApp {
            background-color: #1E1E1E;
            color: #E0E0E0;
        }
        
        /* Header styling */
        .stApp header {
            background-color: #252526;
            color: #BB86FC;
        }
                 .fixed-header {
        position: fixed;
        top: 10%;
        right: 2%;
        width: 100%;
        background-color: #252526;
        z-index: 9999;
        border-bottom: 1px solid #ddd;
    }
        
        /* Sidebar styling */
        [data-testid=stSidebar] {
            background-color: #252526;
        }
        
        /* Other styles remain unchanged */
        h1, h2, h3 {
            color: #BB86FC;
        }
        
        .stButton>button, .stSelectbox>div>div>select {
            background-color: #3700B3;
            color: #E0E0E0;
            border: none;
        }
        
        .stDateInput>div>div>input {
            background-color: #2C2C2C;
            color: #E0E0E0;
            border: 1px solid #BB86FC;
        }
        
        .dataframe {
            background-color: #2C2C2C;
            color: #E0E0E0;
        }
        
        .stPlot {
            background-color: #2C2C2C !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Create a container for the main content
    main_container = st.container()

    # Add header
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col2:
            st.markdown("<div class='fixed-header' style='text-align: right;'><p>Author: Biruke Tadesse<p><p>GitHub: <a href='https://github.com/brukGit/tenx-w1/tree/task-2' target='_blank' style='color: #bb86fc;'>https://github.com/brukGit/tenx-w1</a></p></div>", unsafe_allow_html=True)
            

    # Sidebar for user input
    st.sidebar.title("Controls")
    ticker_selection = st.sidebar.selectbox("Select a stock", list(data.keys()))

    # Date range selection based on selected ticker
    selected_data = data[ticker_selection]
    min_date = selected_data.index.min().date()
    max_date = selected_data.index.max().date()

    start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
    end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

    # Create a placeholder for the processing message
    processing_message = st.empty()

    # Display styled processing message
    processing_message.markdown("""
    <div style="
        background-color: rgba(187, 134, 252, 0.1);
        border: 1px solid #f5f5f5;
        color: #E0E0E0;
        padding: 20px 40px;
        border-radius: 10px;
        text-align: center;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1000;
    ">
        <div style="margin-top: 10px; font-size: 36px; animation: spin 1s linear infinite;">⚙️</div>
    </div>
    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """, unsafe_allow_html=True)

    filtered_data = filter_data(data, start_date, end_date)

    # Main content
    with main_container:
        # Use columns to create a 95% width effect
        _, center_col, _ = st.columns([1, 18, 1])
        
        with center_col:
            
            st.title("Stock Analysis Dashboard")

            # # Descriptive statistics of indicators
            # st.subheader("Descriptive Statistics of Indicators for All Tickers")
            # fig1, fig2 = create_comparative_plots(data)
            # st.pyplot(fig1)
            # st.pyplot(fig2)
             # Descriptive statistics of indicators
            st.subheader(f"Descriptive Statistics of Indicators for {ticker_selection}".format(ticker_selection=ticker_selection))
            fig1, fig2 = create_comparative_plots_per_ticker(filtered_data, ticker_selection)
            st.pyplot(fig1)
            st.pyplot(fig2)

            # Plot stock price and indicators
            st.subheader(f"Stock Price and Technical Indicators for {ticker_selection}".format(ticker_selection=ticker_selection))
            fig = plot_stock_indicators(filtered_data[ticker_selection], ticker_selection)
            st.pyplot(fig)

            # Correlation between indicators and returns
            st.subheader(f"Indicators to Returns Correlation for {ticker_selection}".format(ticker_selection=ticker_selection))
            fig = plot_indicator_returns_correlation(filtered_data[ticker_selection], ticker_selection)
            st.pyplot(fig)

            # Plot returns comparison
            st.subheader("Returns Comparison of All Tickers")
            fig = plot_returns_comparison(filtered_data)
            st.pyplot(fig)

            # Correlation heatmap
            st.subheader("Correlation Heatmap of All Tickers")
            fig = plot_correlation_heatmap(filtered_data)
            st.pyplot(fig)

            # Financial metrics
            st.subheader("Financial Metrics of All Tickers")
            metrics_df = calculate_financial_metrics(filtered_data, market_returns)
            st.dataframe(metrics_df.style.background_gradient(cmap='viridis', axis=0))

           

    # Remove the processing message after all plots are generated
    processing_message.empty()

# Load data (this should be outside the main function as it's used globally)
# file_paths = [
#     "../data/yfinance_data/AAPL_historical_data.csv",
#     "../data/yfinance_data/AMZN_historical_data.csv",
#     "../data/yfinance_data/GOOG_historical_data.csv",
#     "../data/yfinance_data/META_historical_data.csv",
#     "../data/yfinance_data/MSFT_historical_data.csv",
#     "../data/yfinance_data/NVDA_historical_data.csv",
#     "../data/yfinance_data/TSLA_historical_data.csv",
# ]
# market_index_path = "../data/yfinance_data/SPY_historical_data.csv"

# data, market_returns = load_and_process_data(file_paths, market_index_path)

tickers = ['AAPL', 'AMZN', 'GOOG', 'META', 'MSFT', 'NVDA', 'TSLA']
index_ticker = ['SPY']
end_date = datetime.now()
start_date = end_date - timedelta(days=365 * 54)  # 5 years of data

data, market_returns = load_and_process_data(tickers, index_ticker, start_date, end_date)

if __name__ == "__main__":
    main()