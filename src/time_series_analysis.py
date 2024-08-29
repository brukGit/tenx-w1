# src/time_series_analysis.py
import pandas as pd
import matplotlib.pyplot as plt

class TimeSeriesAnalysis:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.df['date'] = pd.to_datetime(self.df['date'])

    def analyze_publication_frequency(self):
        """
        Analyzes publication frequency over time and identifies spikes in article publications.
        """
        # Resample by day and count the number of articles
        daily_counts = self.df.resample('D', on='date').size()

        # Plot the daily counts
        plt.figure(figsize=(12, 6))
        daily_counts.plot()
        plt.title('Number of Articles Published Per Day')
        plt.xlabel('Date')
        plt.ylabel('Number of Articles')
        plt.grid(True)
        plt.show()

    def analyze_publishing_times(self):
        """
        Analyzes the time of day when articles are most frequently published.
        """
        # Extract the hour from the publication date
        self.df['hour'] = self.df['date'].dt.hour

        # Group by hour and count the number of articles
        hourly_counts = self.df.groupby('hour').size()

        # Plot the hourly counts
        plt.figure(figsize=(12, 6))
        hourly_counts.plot(kind='bar')
        plt.title('Number of Articles Published by Hour')
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Articles')
        plt.grid(True)
        plt.show()
