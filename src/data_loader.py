import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pytz

class DataLoader:
    def __init__(self, source_type, **kwargs):
        self.source_type = source_type
        if source_type == 'stock':
            self.tickers = kwargs.get('tickers', [])
            self.dateRange = 50
            self.start_date = kwargs.get('start_date') or datetime.now() - timedelta(days=365 * self.dateRange)
            self.end_date = kwargs.get('end_date') or datetime.now()
        elif source_type == 'news':
            self.file_path = kwargs.get('file_path', '')
        else:
            raise ValueError("Invalid source_type. Must be 'stock' or 'news'.")

    def load_data(self):
        if self.source_type == 'stock':
            return self._fetch_stock_data()
        elif self.source_type == 'news':
            return self._load_news_data()

    def _fetch_stock_data(self):
        dataframes = {}
        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            df = stock.history(start=self.start_date, end=self.end_date)
            
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns {missing_columns} for ticker {ticker}")
            
            df.dropna(inplace=True)
            df.reset_index(inplace=True)
            df['Date'] = pd.to_datetime(df['Date'], utc=True, errors='coerce')
            # Convert the timezone to EAT
            df['Date'] = df['Date'].dt.tz_convert('Africa/Nairobi')
            df.set_index('Date', inplace=True)
            dataframes[ticker] = df
        return dataframes

    def _load_news_data(self):
        df = pd.read_csv(self.file_path)
        df['date'] = pd.to_datetime(df['date'], utc=True, errors='coerce')
        # Convert the timezone to EAT
        df['date'] = df['date'].dt.tz_convert('Africa/Nairobi')

        df.set_index('date', inplace=True)
        return df