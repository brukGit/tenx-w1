import unittest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock

import os
import sys
# Define the path to the src directory
src_dir = os.path.abspath(os.path.join(os.getcwd(), '..', 'src'))
sys.path.insert(0, src_dir)

from src.financial_metrics import FinancialMetrics

class TestFinancialMetrics(unittest.TestCase):

    def setUp(self):
        # Create mock data for testing
        self.data = {
            'AAPL': pd.DataFrame({
                'Date': pd.date_range(start='2023-01-01', periods=100),
                'Close': np.random.rand(100) * 100  # Random close prices
            })
        }
        self.market_returns = pd.Series(np.random.rand(100) * 0.01, index=pd.date_range(start='2023-01-01', periods=100))
        self.metrics = FinancialMetrics(self.data)

    def test_calculate_sharpe_ratio(self):
        # Test Sharpe Ratio calculation
        sharpe_ratios = self.metrics.calculate_sharpe_ratio(risk_free_rate=0.01)
        self.assertIn('AAPL', sharpe_ratios)
        self.assertIsInstance(sharpe_ratios['AAPL'], float)

    def test_calculate_volatility(self):
        # Test volatility calculation
        volatilities = self.metrics.calculate_volatility(period=20)
        self.assertIn('AAPL', volatilities)
        self.assertIsInstance(volatilities['AAPL'], float)

    def test_calculate_beta(self):
        # Test beta calculation
        betas = self.metrics.calculate_beta(market_returns=self.market_returns)
        self.assertIn('AAPL', betas)
        self.assertIsInstance(betas['AAPL'], float)
        self.assertFalse(np.isnan(betas['AAPL']))  # Ensure beta is not NaN

if __name__ == '__main__':
    unittest.main()
