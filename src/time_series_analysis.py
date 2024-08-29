# src/time_series_analysis.py
import matplotlib.pyplot as plt

class TimeSeriesAnalysis:
    def __init__(self, df):
        self.df = df

    def publication_frequency_over_time(self):
        self.df['publication_date'] = pd.to_datetime(self.df['date'])
        return self.df['publication_date'].resample('D').count()

    def analyze_publishing_times(self):
        self.df['publication_time'] = pd.to_datetime(self.df['time']).dt.time
        return self.df['publication_time'].value_counts().sort_index()
