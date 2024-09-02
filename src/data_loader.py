import pandas as pd
import pytz

import yfinance as yf
from datetime import datetime, timedelta

class DataLoader:
    def __init__(self, tickers, start_date=None, end_date=None):
        self.tickers = tickers
        self.dateRange = 50
        self.start_date = start_date or datetime.now() - timedelta(days=365 * self.dateRange)  # Default to 50 years
        self.end_date = end_date or datetime.now()

    def fetch_data(self):
        """
        Fetches stock price data for the specified tickers using yfinance.
        
        Returns:
        --------
        dict:
            A dictionary of DataFrames indexed by ticker symbols.
        """
        dataframes = {}
        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            df = stock.history(start=self.start_date, end=self.end_date)
            
            # Ensure required columns are present
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns {missing_columns} for ticker {ticker}")
            
            # Drop rows with NaN values
            df.dropna(inplace=True)
            
            # Optionally reset index to have 'Date' as a column
            df.reset_index(inplace=True)
            
            dataframes[ticker] = df

        return dataframes


    def load_data(self):
        """
        Loads and processes the stock price data.
        
        This method performs the following:
        1. Fetches data using yfinance.
        2. Ensures required columns are present.
        3. Drops rows with NaN values.
        4. Sets 'Date' as the index.
        
        Returns:
        --------
        dict:
            A dictionary of processed DataFrames indexed by ticker symbols.
        """
        dataframes = self.fetch_data()
        processed_dataframes = {}

        for ticker, df in dataframes.items():
            
                # Check if 'Date' column exists
                if 'Date' not in df.columns:
                    raise KeyError(f"The 'Date' column is missing from the DataFrame for ticker {ticker}")
                
                # Set 'Date' as the index for time series analysis
                df.set_index('Date', inplace=True)
                
                # Add the processed DataFrame to the dictionary
                processed_dataframes[ticker] = df

        return processed_dataframes

