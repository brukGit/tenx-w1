import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime, timedelta


import os
import sys
# Define the path to the src directory
src_dir = os.path.abspath(os.path.join(os.getcwd(), '..', 'src'))
sys.path.insert(0, src_dir)

from data_loader import DataLoader

class TestDataLoader(unittest.TestCase):

    @patch('yfinance.Ticker')
    def test_fetch_data(self, MockTicker):
        # Set up mock data
        mock_data = pd.DataFrame({
            'Open': [100, 101],
            'High': [102, 103],
            'Low': [99, 100],
            'Close': [101, 102],
            'Volume': [1000, 1500]
        }, index=pd.date_range(start='2023-01-01', periods=2))
        
        # Mock the history method of yfinance
        mock_ticker_instance = MockTicker.return_value
        mock_ticker_instance.history.return_value = mock_data

        # Initialize DataLoader with mock tickers
        tickers = ['AAPL', 'GOOGL']
        loader = DataLoader(tickers)

        # Fetch data
        data = loader.fetch_data()

        # Verify data for each ticker
        for ticker in tickers:
            df = data[ticker]
            self.assertIsInstance(df, pd.DataFrame)
            self.assertEqual(df.shape[0], 2)
            self.assertTrue('Open' in df.columns)
            self.assertTrue('Close' in df.columns)

    def test_load_data(self):
        with patch('yfinance.Ticker') as MockTicker:
            mock_data = pd.DataFrame({
                'Open': [100, 101],
                'High': [102, 103],
                'Low': [99, 100],
                'Close': [101, 102],
                'Volume': [1000, 1500]
            }, index=pd.date_range(start='2023-01-01', periods=2))

            # Mock the history method of yfinance
            mock_ticker_instance = MockTicker.return_value
            mock_ticker_instance.history.return_value = mock_data

            # Initialize DataLoader with mock tickers
            tickers = ['AAPL', 'GOOGL']
            loader = DataLoader(tickers)

            # Load data
            data = loader.load_data()

            # Verify data for each ticker
            for ticker in tickers:
                df = data[ticker]
                self.assertIsInstance(df, pd.DataFrame)
                self.assertEqual(df.shape[0], 2)
                self.assertEqual(df.index.name, 'Date')
                self.assertTrue('Open' in df.columns)
                self.assertTrue('Close' in df.columns)

if __name__ == '__main__':
    unittest.main()

