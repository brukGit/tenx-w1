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
        plt.xlabel('Hour of Day, EAT(UTC+3)')
        plt.ylabel('Number of Articles')
        plt.grid(True)
        plt.show()

    def identify_spikes(self, threshold=2.0):
        """
        Identify spikes in article publications where the number of articles is significantly higher than average.
        
        :param threshold: float, multiplier of standard deviation above the mean to consider a spike
        :return: DataFrame of spike dates and their counts
        """
        # Ensure the 'date' column is set as the index and is a DatetimeIndex
        if not isinstance(self.df.index, pd.DatetimeIndex):
            self.df['date'] = pd.to_datetime(self.df['date'], utc=True)
            self.df.set_index('date', inplace=True)

        # Resample by day and count the number of articles
        daily_counts = self.df.resample('D').size()
        
        # Calculate mean and standard deviation of daily article counts
        mean_count = daily_counts.mean()
        std_count = daily_counts.std()

        # Identify spikes as days with counts greater than mean + threshold * std_dev
        spike_days = daily_counts[daily_counts > mean_count + threshold * std_count]
        
        # Sort the spike days in descending order of counts
        spike_days_sorted = spike_days.sort_values(ascending=False)
        
        return spike_days_sorted
