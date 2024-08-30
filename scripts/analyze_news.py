# scripts/analyze_news.py
import sys
import os

# Define the path to the src directory
src_dir = os.path.abspath(os.path.join(os.getcwd(), '..', 'src'))
sys.path.insert(0, src_dir)

# Delete the eda and data_loader modules if they exist
if 'eda' in sys.modules:
    del sys.modules['eda']
if 'data_loader' in sys.modules:
    del sys.modules['data_loader']
if 'text_analysis' in sys.modules:
    del sys.modules['text_analysis']
if 'time_series_analysis' in sys.modules:
    del sys.modules['time_series_analysis']
if 'publisher_analysis' in sys.modules:
    del sys.modules['publisher_analysis']

from eda import EDA
from data_loader import DataLoader
from text_analysis import TextAnalysis
from time_series_analysis import TimeSeriesAnalysis
from publisher_analysis import PublisherAnalysis

def main():
    # -----------  Load and clean data  ------------- #
    data_loader = DataLoader("../data/raw_analyst_ratings/raw_analyst_ratings.csv")
    df = data_loader.load_data()
    df = data_loader.clean_data(df)

    # -----------  Perform EDA  ------------- #
    print("\nPerforming EDA...")
    eda = EDA(df)
    print("\nAnalyzing textual lengths...")
    print(eda.get_textual_lengths_stats())
    print("\nCounting articles by publisher...")
    print(eda.count_articles_per_publisher())
    print("\nAnalyzing publication dates...")
    eda.analyze_publication_dates()
    print("\nAnalyzing publications by day of the week...")
    eda.plot_day_of_week_frequency()
    print("\nIdentifying publication spike days..")
    print(eda.identify_spikes())

    # -----------  Perform Text Analysis  ------------- #
   
    # sentiment analysis
    print("Performing sentiment analysis...")
    ta = TextAnalysis(df)
    sentiment_analysis = ta.perform_sentiment_analysis()
    print("Headline sentiments:")
    print(sentiment_analysis.head())

    #phrase analysis
    phrases_analysis = ta.extract_keywords()
    print("Headline keywords count:")
    print(phrases_analysis)   

    # -----------  Perform Time Series Analysis  ------------- #
    
    print("Performing time series analysis...")
    tsa = TimeSeriesAnalysis(df)
    print("Analyzing publication frequency...")
    tsa.analyze_publication_frequency()
    print("Identifying publication spikes...")
    tsa.identify_spikes()
    print("Analyzing publishing times...")
    tsa.analyze_publishing_times()


    # -----------  Perform Publisher Analysis  ------------- #
    # most active publishers
    print("Performing publisher analysis...")
    pa = PublisherAnalysis(df)
    print("Analyzing most active publishers...")
    publisher_counts = pa.most_active_publishers()
    print("Most active publishers:")
    print(publisher_counts)

    # publisher domains
    print("Analyzing publisher domains...")
    publisher_domains = pa.analyze_publisher_domains()
    print("Publisher domains:")
    print(publisher_domains)

    # news type
    print("Analyzing news type...")
    news_type_counts = pa.analyze_news_type()
    print("News type counts:")
    print(news_type_counts)

    # top publishers and news types
    print("Analyzing top publishers and news types...")
    top_publishers_news_types = pa.analyze_top_publishers_news_types(5)
    print("Top publishers and news types:")
    print(top_publishers_news_types)


if __name__ == "__main__":
    main()
