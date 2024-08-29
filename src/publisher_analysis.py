# src/publisher_analysis.py

class PublisherAnalysis:
    def __init__(self, df):
        self.df = df

    def top_publishers(self):
        return self.df['publisher'].value_counts().head(10)

    def analyze_publisher_domains(self):
        self.df['domain'] = self.df['publisher'].apply(lambda x: x.split('@')[-1])
        return self.df['domain'].value_counts()
