import pandas as pd
import pytz

class DataCleaner:
    def __init__(self):
        pass

    def clean_data(self, df: pd.DataFrame, data_type: str) -> pd.DataFrame:
        if data_type == 'stock':
            return self._clean_stock_data(df)
        elif data_type == 'news':
            return self._clean_news_data(df)
        else:
            raise ValueError("Invalid data_type. Must be 'stock' or 'news'.")

    def _clean_stock_data(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.index.name == 'Date':
            df.reset_index(inplace=True)
            
        if 'Date' not in df.columns:
            raise KeyError("The 'Date' column is missing from the DataFrame")

        df = df.dropna(subset=['Date'])
        df = df.drop_duplicates()
        df['Date'] = pd.to_datetime(df['Date'], utc=True, errors='coerce')
        df = df.dropna(subset=['Date'])

        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Dividends', 'Stock Splits']
        for column in numeric_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors='coerce')

        return df

    def _clean_news_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(subset=['headline', 'date'])
        df = df.drop_duplicates()
        df['date'] = pd.to_datetime(df['date'], utc=True, errors='coerce')
        df['date'] = df['date'].dt.tz_convert('Africa/Nairobi')
        df = df.dropna(subset=['date'])

        if 'headline_length' in df.columns:
            df['headline_length'] = pd.to_numeric(df['headline_length'], errors='coerce')
            df = df.dropna(subset=['headline_length'])

        df['headline'] = df['headline'].str.strip()
        df['publisher'] = df['publisher'].str.strip()

        return df