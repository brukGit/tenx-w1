import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

import os
import sys
# Define the path to the src directory
src_dir = os.path.abspath(os.path.join(os.getcwd(), '..', 'src'))
sys.path.insert(0, src_dir)

from src.indicators import TechnicalIndicators
class TestTechnicalIndicators(unittest.TestCase):

    def setUp(self):
        # Create mock data for testing
        self.data = {
            'AAPL': pd.DataFrame({
                'Date': pd.date_range(start='2023-01-01', periods=30),
                'Close': np.random.rand(30) * 100  # Random close prices
            })
        }
        self.indicators = TechnicalIndicators(self.data)

    def test_calculate_moving_average(self):
        # Test moving average calculation
        self.indicators.calculate_moving_average(window=5)
        df = self.data['AAPL']
        self.assertIn('MA', df.columns)
        self.assertEqual(df['MA'].isna().sum(), 0)  # Ensure no NaNs due to backfill

    def test_calculate_rsi(self):
        # Test RSI calculation
        self.indicators.calculate_rsi(period=14)
        df = self.data['AAPL']
        self.assertIn('RSI', df.columns)
        self.assertEqual(df['RSI'].isna().sum(), 0)  # Ensure no NaNs due to backfill

    def test_calculate_macd(self):
        # Test MACD calculation
        self.indicators.calculate_macd()
        df = self.data['AAPL']
        self.assertIn('MACD', df.columns)
        self.assertIn('MACD_signal', df.columns)
        self.assertIn('MACD_Histogram', df.columns)
        self.assertEqual(df['MACD'].isna().sum(), 0)  # Ensure no NaNs due to backfill
        self.assertEqual(df['MACD_signal'].isna().sum(), 0)
        self.assertEqual(df['MACD_Histogram'].isna().sum(), 0)

if __name__ == '__main__':
    unittest.main()
