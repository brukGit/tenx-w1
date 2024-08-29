# tests/test_data_loader.py
import unittest
import pandas as pd
from src.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    def setUp(self):
        self.file_path = "path/to/test_file.csv"  # Use a test CSV file
        self.data_loader = DataLoader(self.file_path)

    def test_load_data(self):
        df = self.data_loader.load_data()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)

    def test_clean_data(self):
        df = self.data_loader.load_data()
        df = self.data_loader.clean_data(df)
        # Add assertions to check if data cleaning is correct
        self.assertFalse(df.isnull().values.any())

if __name__ == "__main__":
    unittest.main()
