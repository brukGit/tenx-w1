# src/eda.py

import pandas as pd
import matplotlib.pyplot as plt

class EDA:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        # Ensure the headline_length column is present
        if 'headline_length' not in self.df.columns:
            self.df['headline_length'] = self.df['headline'].apply(len)
    
    def get_textual_lengths_stats(self):
        """
        Obtain basic statistics for textual lengths, such as headline length.
        """
        stats = {
            'mean_headline_length': self.df['headline_length'].mean(),
            'median_headline_length': self.df['headline_length'].median(),
            'std_headline_length': self.df['headline_length'].std(),
            'max_headline_length': self.df['headline_length'].max(),
            'min_headline_length': self.df['headline_length'].min()
        }
        return stats
    
    def count_articles_per_publisher(self):
        """
        Count the number of articles per publisher to identify the most active publishers.
        """
        publisher_counts = self.df['publisher'].value_counts()
        return publisher_counts
    
    def analyze_publication_dates(self):
        """
        Analyze publication dates to see trends over time.
        """
        # Set the publication date as index
        self.df.set_index('date', inplace=True)
        
        # Resample by day and count the number of articles
        daily_counts = self.df.resample('D').size()
        daily_counts.plot(figsize=(12, 6))
        plt.title('Number of Articles Published Per Day')
        plt.xlabel('Date')
        plt.ylabel('Number of Articles')
        plt.grid(True)
        plt.show()

    def plot_day_of_week_frequency(self):
        """
        Plot the frequency of articles published on each day of the week.
        """
        # Extract the day of the week (Monday=0, Sunday=6)
        self.df['day_of_week'] = self.df.index.dayofweek
        
        # Map the numbers to actual day names
        day_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 
                     4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        self.df['day_of_week'] = self.df['day_of_week'].map(day_names)
        
        # Count the number of articles published on each day of the week
        day_counts = self.df['day_of_week'].value_counts().reindex(day_names.values())
        
        # Plot the results
        day_counts.plot(kind='bar', figsize=(10, 6), color='skyblue')
        plt.title('Number of Articles Published by Day of the Week')
        plt.xlabel('Day of the Week')
        plt.ylabel('Number of Articles')
        plt.xticks(rotation=45)
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


