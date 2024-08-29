# src/publisher_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from urllib.parse import urlparse
import seaborn as sns

class PublisherAnalysis:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def most_active_publishers(self):
        """
        Identifies which publishers contribute most to the news feed.
        """
        publisher_counts = self.df['publisher'].value_counts()

        # Plot the top publishers
        plt.figure(figsize=(12, 6))
        publisher_counts.head(10).plot(kind='bar')
        plt.title('Top 10 Most Active Publishers')
        plt.xlabel('Publisher')
        plt.ylabel('Number of Articles')
        plt.grid(True)
        plt.show()

        return publisher_counts

    def analyze_publisher_domains(self):
        """
        If email addresses are used as publisher names, identifies unique domains to see if certain organizations contribute more frequently.
        """
        if self.df['publisher'].str.contains('@').any():
            # Extract domains from email addresses
            self.df['domain'] = self.df['publisher'].apply(lambda x: x.split('@')[1] if '@' in x else x)
        else:
            # Extract domains from URLs if they exist in the 'publisher' field
            self.df['domain'] = self.df['publisher'].apply(lambda x: urlparse(x).netloc if '.' in x else x)

        domain_counts = self.df['domain'].value_counts()

        # Plot the top domains
        plt.figure(figsize=(12, 6))
        domain_counts.head(10).plot(kind='bar')
        plt.title('Top 10 Most Frequent Publisher Domains')
        plt.xlabel('Domain')
        plt.ylabel('Number of Articles')
        plt.grid(True)
        plt.show()

        return domain_counts

    def analyze_news_type_per_publisher(self):
        """
        Analyzes the type of news reported by each publisher, if applicable.
        This requires a column in your DataFrame that categorizes the type of news.
        """
        # Assuming there's a 'news_type' column categorizing the type of news
        if 'news_type' in self.df.columns:
            news_type_counts = self.df.groupby('publisher')['news_type'].value_counts().unstack().fillna(0)

            # Plot a heatmap to visualize the distribution of news types per publisher
            plt.figure(figsize=(12, 8))
            sns.heatmap(news_type_counts, cmap="YlGnBu", linewidths=0.5, annot=True, fmt="g")
            plt.title('Distribution of News Types per Publisher')
            plt.xlabel('News Type')
            plt.ylabel('Publisher')
            plt.show()

            return news_type_counts
        else:
            print("No 'news_type' column found in the DataFrame.")
            return None
