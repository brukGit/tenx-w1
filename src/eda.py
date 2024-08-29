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
        # Convert the 'date' column to datetime with timezone awareness
        self.df['date'] = pd.to_datetime(self.df['date'], utc=True)
        
        # Convert to the original timezone if needed (here it converts back to UTC-4)
        self.df['date'] = self.df['date'].dt.tz_convert('America/New_York')
        
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
