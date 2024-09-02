import unittest
import pandas as pd
import os
import tempfile
import sys

# Add the src directory to the Python path
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, src_dir)

from data_cleaner import DataCleaner

class TestDataCleaner(unittest.TestCase):
    """
    Unit tests for the DataCleaner class.
    """
    def setUp(self):
        """
        Set up the test environment by creating a temporary directory and a mock CSV file.
        """
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Create a mock CSV file
        self.test_file_path = os.path.join(self.test_dir, 'TEST_historical_data.csv')
        self.create_mock_csv()
        
        # Initialize DataCleaner
        self.data_cleaner = DataCleaner()

    def create_mock_csv(self):
        """
        Create a mock CSV file with test data.
        """
        data = {
            'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
            'Open': [100, 101, None, 102, 103],
            'High': [105, 106, None, 107, 108],
            'Low': [98, 99, None, 100, 101],
            'Close': [103, 104, None, 105, 106],
            'Volume': [1000000, 1100000, None, 1200000, 1300000]
        }
        df = pd.DataFrame(data)
        df.to_csv(self.test_file_path, index=False)

    def test_clean_data(self):
        """
        Test the clean_data method of the DataCleaner class.
        """
        # Load the test data
        df = pd.read_csv(self.test_file_path)
        
        # Clean the data
        cleaned_df = self.data_cleaner.clean_data(df)
        
        # Check the cleaned data
        self.assertEqual(len(cleaned_df), 4)
        self.assertTrue(pd.to_datetime(cleaned_df['Date']).dt.tz is not None)
        self.assertTrue(pd.notna(cleaned_df['Open']).all())
        self.assertTrue(pd.notna(cleaned_df['High']).all())
        self.assertTrue(pd.notna(cleaned_df['Low']).all())
        self.assertTrue(pd.notna(cleaned_df['Close']).all())
        self.assertTrue(pd.notna(cleaned_df['Volume']).all())

    def tearDown(self):
        """
        Clean up the temporary directory after the tests are completed.
        """
        # Clean up the temporary directory
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main()