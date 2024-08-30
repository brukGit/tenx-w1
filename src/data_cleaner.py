import pandas as pd

class DataCleaner:
    """
    A class to handle the cleaning of stock price data.
    """
    
    def __init__(self):
        """
        Initializes the DataCleaner class.
        """
        pass

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans the provided DataFrame by handling missing values, duplicates, and ensuring proper data types.

        Parameters:
        -----------
        df : pd.DataFrame
            The DataFrame to be cleaned.

        Returns:
        --------
        pd.DataFrame:
            The cleaned DataFrame.
        """

         # Reset index if 'Date' is the index
        if df.index.name == 'Date':
            df.reset_index(inplace=True)
            
        # Check if 'Date' column exists
        if 'Date' not in df.columns:
            raise KeyError("The 'Date' column is missing from the DataFrame")

        # 1. Drop rows where 'Date' is missing
        df = df.dropna(subset=['Date'])

        # 2. Remove duplicates
        df = df.drop_duplicates()

        # 3. Ensure 'Date' column is in datetime format and contains timezone information
        df['Date'] = pd.to_datetime(df['Date'], utc=True, errors='coerce')

        # 4. Remove rows with invalid dates
        df = df.dropna(subset=['Date'])

        # 5. Ensure numeric columns are properly formatted
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Dividends', 'Stock Splits']
        for column in numeric_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors='coerce')

        return df
