import pandas as pd
import os

class DataLoader:
    """
    A class to load and preprocess stock price data from CSV files.
    
    Attributes:
    -----------
    file_paths : list
        List of file paths to the historical data CSV files.
        
    Methods:
    --------
    load_data() -> dict:
        Loads data from CSV files into a dictionary of DataFrames indexed by ticker symbols.
        
    clean_data(df: pd.DataFrame) -> pd.DataFrame:
        Cleans the provided DataFrame by handling missing values, duplicates, and ensuring proper data types.
    """
    
    def __init__(self, file_paths):
        """
        Initializes the DataLoader with a list of file paths.
        
        Parameters:
        -----------
        file_paths : list
            List of file paths to the historical data CSV files.
        """
        self.file_paths = file_paths

    def load_data(self):
        """
        Loads the stock price data from the specified CSV files into a dictionary of DataFrames.
        
        This method performs the following checks:
        1. Ensures required columns are present.
        2. Loads data from each file into a DataFrame.
        
        Returns:
        --------
        dict:
            A dictionary of DataFrames indexed by ticker symbols.
        """
        dataframes = {}
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

        for file_path in self.file_paths:
            # Extract the ticker symbol from the file name
            ticker = os.path.basename(file_path).split('_')[0]

            # Load the CSV data into a DataFrame
            df = pd.read_csv(file_path)

            # Check if the required columns are present
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns {missing_columns} in file {file_path}")

            # Optionally set 'Date' as the index for time series analysis (can be done later)
            df.set_index('Date', inplace=True)

            # Add the DataFrame to the dictionary
            dataframes[ticker] = df

        return dataframes

