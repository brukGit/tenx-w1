import pandas as pd

class DataLoader:
    def __init__(self, file_paths):
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        self.file_paths = file_paths

    def load_data(self):
        dataframes = []
        for file_path in self.file_paths:
            df = pd.read_csv(file_path)
            dataframes.append(df)
        return pd.concat(dataframes, ignore_index=True)

    def clean_data(self, df):
        """
        Clean the data by handling missing values, removing duplicates, and
        ensuring correct data types.
        """
        # 1. Drop rows where 'Date' is missing
        df = df.dropna(subset=['Date'])

        # 2. Remove duplicates
        df = df.drop_duplicates()

        # 3. Ensure 'Date' column is in datetime format and contains timezone information
        df['Date'] = pd.to_datetime(df['Date'], utc=True, errors='coerce')

        # 4. Remove rows with invalid dates
        df = df.dropna(subset=['Date'])

        # 5. Convert numerical columns to the appropriate data type (if needed)
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Dividends', 'Stock Splits']
        for column in numeric_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors='coerce')

        return df
