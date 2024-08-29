# src/eda.py
import pandas as pd

class EDA:
    def __init__(self, df):
        self.df = df

    def describe_statistics(self):
        # Example: Describe headline lengths
        self.df['headline_length'] = self.df['headline'].apply(len)
        return self.df['headline_length'].describe()

    def count_articles_by_publisher(self):
        return self.df['publisher'].value_counts()

    def analyze_publication_dates(self):
        self.df['publication_date'] = pd.to_datetime(self.df['date'])
        return self.df['publication_date'].dt.date.value_counts()
