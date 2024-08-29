import pandas as pd

class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        return pd.read_csv(self.file_path)

    def clean_data(self, df):
        """
        Clean the data by handling missing values, removing duplicates, and
        ensuring correct data types.
        """
        # 1. Drop rows where the 'headline' or 'date' is missing, as these are essential fields
        df = df.dropna(subset=['headline', 'date'])

        # 2. Remove duplicates
        df = df.drop_duplicates()

        # 3. Ensure 'date' column is in datetime format and contains timezone information
        df['date'] = pd.to_datetime(df['date'], utc=True, errors='coerce')

        # 4. Remove rows with invalid dates
        df = df.dropna(subset=['date'])

        # 5. Convert 'headline_length' to an integer type (assuming it's already numeric)
        if 'headline_length' in df.columns:
            df['headline_length'] = pd.to_numeric(df['headline_length'], errors='coerce')
            df = df.dropna(subset=['headline_length'])  # Remove rows with invalid headline lengths

        # 6. Additional cleaning: Remove any whitespace from string columns
        df['headline'] = df['headline'].str.strip()
        df['publisher'] = df['publisher'].str.strip()

        return df
