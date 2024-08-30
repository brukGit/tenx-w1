"""
This script loads, cleans, and analyzes stock data by applying technical indicators
and calculating financial metrics.

Usage:
------
Simply run the script in your terminal or IDE.

Outputs:
--------
The script prints the calculated Sharpe Ratios and Volatilities for each stock.
"""
import os
import sys
# Define the path to the src directory
src_dir = os.path.abspath(os.path.join(os.getcwd(), '..', 'src'))
sys.path.insert(0, src_dir)

if 'data_loader' in sys.modules:
    del sys.modules['data_loader']
if 'data_cleaner' in sys.modules:
    del sys.modules['data_cleaner']
if 'indicators' in sys.modules:
    del sys.modules['indicators']
if 'financial_metrics' in sys.modules:
    del sys.modules['financial_metrics']

from data_loader import DataLoader
from data_cleaner import DataCleaner
from indicators import TechnicalIndicators
from financial_metrics import FinancialMetrics


# Define file paths for the stock data CSV files
file_paths = [
    "../data/yfinance_data/AAPL_historical_data.csv",
    "../data/yfinance_data/AMZN_historical_data.csv",
    "../data/yfinance_data/GOOG_historical_data.csv",
    "../data/yfinance_data/META_historical_data.csv",
    "../data/yfinance_data/MSFT_historical_data.csv",
    "../data/yfinance_data/NVDA_historical_data.csv",
    "../data/yfinance_data/TSLA_historical_data.csv",
]

def main():
    # Load and clean data
    loader = DataLoader(file_paths)
    data = loader.load_data()

    # Clean each data frame
    cleaner = DataCleaner()
    cleaned_data = {ticker: cleaner.clean_data(df) for ticker, df in data.items()}
    data = cleaned_data
    # Apply technical indicators
    indicators = TechnicalIndicators(data)
    indicators.calculate_moving_average()
    indicators.calculate_rsi()
    indicators.calculate_macd()
    for ticker, df in data.items():
        print(ticker, ' indicators calculated..')
        print(df[['Close','RSI','MACD', 'MACD_signal', 'MACD_hist']].tail(5))
        

    # Calculate financial metrics
    metrics = FinancialMetrics(data)
    sharpe_ratios = metrics.calculate_sharpe_ratio()
    volatilities = metrics.calculate_volatility()

    # Output results
    print("Sharpe Ratios:", sharpe_ratios)
    print("Volatilities:", volatilities)

if __name__ == "__main__":
    main()