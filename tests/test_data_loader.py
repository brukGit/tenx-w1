import unittest
import pandas as pd
import os
import tempfile
import sys

# Add the src directory to the Python path
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, src_dir)

from data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        
        # Create a mock CSV file
        self.test_file_path = os.path.join(self.test_dir, 'TEST_historical_data.csv')
        self.create_mock_csv()
        
        # Initialize DataLoader with the test file
        self.data_loader = DataLoader([self.test_file_path])

    def create_mock_csv(self):
        data = {
            'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'Open': [100, 101, 102],
            'High': [105, 106, 107],
            'Low': [98, 99, 100],
            'Close': [103, 104, 105],
            'Volume': [1000000, 1100000, 1200000]
        }
        df = pd.DataFrame(data)
        df.to_csv(self.test_file_path, index=False)

    def test_load_data(self):
        # Test the load_data method
        data = self.data_loader.load_data()
        
        # Check if the data is loaded correctly
        self.assertIn('TEST', data)
        self.assertIsInstance(data['TEST'], pd.DataFrame)
        self.assertEqual(len(data['TEST']), 3)
        self.assertEqual(list(data['TEST'].columns), ['Open', 'High', 'Low', 'Close', 'Volume'])
        self.assertEqual(data['TEST'].index.name, 'Date')

    def test_missing_column(self):
        # Create a CSV file with a missing required column
        incomplete_file_path = os.path.join(self.test_dir, 'INCOMPLETE_historical_data.csv')
        incomplete_data = {
            'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'Open': [100, 101, 102],
            'High': [105, 106, 107],
            'Low': [98, 99, 100],
            'Close': [103, 104, 105]
            # 'Volume' is missing
        }
        pd.DataFrame(incomplete_data).to_csv(incomplete_file_path, index=False)
        
        incomplete_loader = DataLoader([incomplete_file_path])
        
        # Test that ValueError is raised when a required column is missing
        with self.assertRaises(ValueError):
            incomplete_loader.load_data()

    def tearDown(self):
        # Clean up the temporary directory
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main()