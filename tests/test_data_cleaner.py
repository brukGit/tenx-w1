import unittest
import pandas as pd
from datetime import datetime

import os
import sys
# Define the path to the src directory
src_dir = os.path.abspath(os.path.join(os.getcwd(), '..', 'src'))
sys.path.insert(0, src_dir)

from data_cleaner import DataCleaner
class TestDataCleaner(unittest.TestCase):

    def setUp(self):
        self.cleaner = DataCleaner()

    def test_clean_data(self):
        # Create a DataFrame with various issues
        data = {
            'Date': ['2023-01-01', '2023-01-02', None, '2023-01-02', '2023-01-03', 'not_a_date'],
            'Open': [100, 101, 102, 103, None, 105],
            'High': [102, 103, 104, 105, 106, 'NaN'],
            'Low': [99, 100, None, 101, 102, 103],
            'Close': [101, 102, 103, None, 105, 106],
            'Volume': [1000, 1500, None, 2000, 2500, 3000]
        }
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Clean the data
        cleaned_df = self.cleaner.clean_data(df)

        # Verify the results
        self.assertEqual(len(cleaned_df), 3)  # Should drop 3 rows
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(cleaned_df['Date']))
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_df['Open']))
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_df['High']))
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_df['Low']))
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_df['Close']))
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_df['Volume']))

        # Check that invalid dates are removed
        self.assertTrue(pd.to_datetime('2023-01-01') in cleaned_df['Date'].values)
        self.assertTrue(pd.to_datetime('2023-01-02') in cleaned_df['Date'].values)
        self.assertTrue(pd.to_datetime('2023-01-03') in cleaned_df['Date'].values)

        # Check that 'not_a_date' and None entries are removed
        self.assertNotIn(pd.NaT, cleaned_df['Date'].values)

    def test_missing_date_column(self):
        # Create a DataFrame missing the 'Date' column
        data = {
            'Open': [100, 101],
            'High': [102, 103],
            'Low': [99, 100],
            'Close': [101, 102],
            'Volume': [1000, 1500]
        }
        df = pd.DataFrame(data)
        with self.assertRaises(KeyError):
            self.cleaner.clean_data(df)

if __name__ == '__main__':
    unittest.main()
