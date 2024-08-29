# scripts/analyze_news.py
from src.data_loader import DataLoader
from src.eda import EDA
from src.text_analysis import TextAnalysis
from src.time_series_analysis import TimeSeriesAnalysis
from src.publisher_analysis import PublisherAnalysis

def main():
    # Load and clean data
    data_loader = DataLoader("../data/raw_analyst_ratings/raw_analyst_ratings.csv")
    df = data_loader.load_data()
    df = data_loader.clean_data(df)

    # Perform EDA
    eda = EDA(df)
    print(eda.describe_statistics())
    print(eda.count_articles_by_publisher())
    print(eda.analyze_publication_dates())

    # Perform Text Analysis
    text_analysis = TextAnalysis(df)
    print(text_analysis.perform_sentiment_analysis())

    # Perform Time Series Analysis
    time_series_analysis = TimeSeriesAnalysis(df)
    print(time_series_analysis.publication_frequency_over_time())

    # Perform Publisher Analysis
    publisher_analysis = PublisherAnalysis(df)
    print(publisher_analysis.top_publishers())

if __name__ == "__main__":
    main()
