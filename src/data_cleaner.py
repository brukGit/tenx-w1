import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.text_analysis import TextAnalysis

class DataCleaner:
    def __init__(self):
        pass

    def clean_data(self, df: pd.DataFrame, data_type: str) -> pd.DataFrame:
        if data_type == 'stock':
            return self._clean_stock_data(df)
        elif data_type == 'news':
            return self._clean_news_data(df)
        else:
            raise ValueError("Invalid data_type. Must be 'stock' or 'news'.")

    def _clean_stock_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna()
        df = df.drop_duplicates()

        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        for column in numeric_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(df[column], errors='coerce')

        df['Returns'] = df['Close'].pct_change()
        df['Cumulative_Returns'] = (1 + df['Returns']).cumprod()
        
        return df

    def _clean_news_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna()
        df = df.drop_duplicates()

        df['headline'] = df['headline'].str.strip()
        df['publisher'] = df['publisher'].str.strip()

            # Perform sentiment analysis
        text_analyzer = TextAnalysis(df)
        df = text_analyzer.perform_sentiment_analysis()

        # Merge the sentiment analysis results with the original dataframe
        # df = df.merge(sentiment_df, on='headline', how='left')

        
        return df
        # return df
    
    def align_data(self, stock_data: dict, news_data: pd.DataFrame) -> dict:
        aligned_data = {}
        
        # Ensure the 'date' column in news_data is in datetime format and remove time information
        news_data.index = pd.to_datetime(news_data.index).normalize()

        for ticker, stock_df in stock_data.items():
            # Ensure the 'Date' index in stock_data is in datetime format and remove time information
            stock_df.index = pd.to_datetime(stock_df.index).normalize()

            # Resample stock data to daily frequency (keep the last value of each day)
            stock_daily = stock_df.resample('D').last()

            # Merge stock data with news data on the date index
            merged = pd.merge(stock_daily, news_data, left_index=True, right_index=True, how='inner')

            # Forward fill stock data
            merged[['Close', 'Returns', 'Cumulative_Returns']] = merged[['Close', 'Returns', 'Cumulative_Returns']].ffill()

            # Aggregate news sentiment for each day
            merged['Daily_Sentiment'] = merged.groupby(merged.index)['polarity'].transform('mean')

            # Classify daily sentiment
            def classify_daily_sentiment(score):
                if score >= 0.5:
                    return 'positive'
                elif 0.05 <= score < 0.5:
                    return 'neutral'
                elif -0.5 < score < 0.05:
                    return 'negative'
                else:
                    return 'strong negative'

            merged['Daily_Sentiment_Class'] = merged['Daily_Sentiment'].apply(classify_daily_sentiment)
            
            # Drop rows without both stock and news data
            merged = merged.dropna(subset=['Close', 'Daily_Sentiment'])

            # Ensure the index is unique
            merged = merged[~merged.index.duplicated(keep='last')]

            aligned_data[ticker] = merged

        return aligned_data

    def prepare_for_correlation(self, aligned_data: dict) -> pd.DataFrame:
        correlation_data = {}
        for ticker, df in aligned_data.items():
            # Ensure the DataFrame has a hierarchical column index
            df = df[['Returns', 'Daily_Sentiment', 'Daily_Sentiment_Class']]
            df.columns = pd.MultiIndex.from_product([[ticker], df.columns])
            correlation_data[ticker] = df
        
        # Concatenate along the columns axis
        return pd.concat(correlation_data.values(), axis=1)
    
    # Perform correlation analysis
    def perform_correlation_analysis(self,correlation_data: pd.DataFrame) -> pd.DataFrame:
        correlation_results = {}
        
        for ticker in correlation_data.columns.levels[0]:  # Iterate over tickers
            returns = correlation_data[ticker]['Returns']
            sentiment = correlation_data[ticker]['Daily_Sentiment']
            correlation = returns.corr(sentiment)  # Calculate correlation between Returns and Daily_Sentiment
            correlation_results[ticker] = correlation
        
        return pd.Series(correlation_results)
    
    def calculate_and_plot_correlation(self,correlation_data: pd.DataFrame) -> pd.Series:
        correlation_results = {}
        
        for ticker in correlation_data.columns.levels[0]:  # Iterate over tickers
            returns = correlation_data[ticker]['Returns']
            sentiment = correlation_data[ticker]['Daily_Sentiment']
            correlation = returns.corr(sentiment)  # Calculate Pearson correlation
            correlation_results[ticker] = correlation
        
        # Convert results to a Series
        correlation_series = pd.Series(correlation_results, name='Pearson Correlation')
        
        # Plot the heatmap
        plt.figure(figsize=(10, 6))
        sns.heatmap(correlation_series.to_frame(), annot=True, cmap='coolwarm', cbar=True, linewidths=0.5)
        plt.title('Correlation between Daily Sentiment and Stock Returns')
        plt.show()
        
        return correlation_series
    


    def time_series_aggregate_returns_and_sentiment(self,aligned_data: dict):
        # Initialize DataFrames to store aggregate returns and sentiment
        all_returns = pd.DataFrame()
        all_sentiment = pd.DataFrame()

        # Loop through aligned data and aggregate returns and sentiment
        for ticker, df in aligned_data.items():
            all_returns[ticker] = df['Returns']
            all_sentiment[ticker] = df['Daily_Sentiment']

        # Aggregate returns and sentiment by taking the mean for each day
        aggregate_returns = all_returns.mean(axis=1)
        aggregate_sentiment = all_sentiment.mean(axis=1)

        # Plotting the time series with dual y-axes
        fig, ax1 = plt.subplots(figsize=(12, 6))

        ax1.set_xlabel('Date')
        ax1.set_ylabel('Aggregate Returns', color='tab:blue')
        ax1.plot(aggregate_returns.index, aggregate_returns, color='tab:blue', label='Aggregate Returns')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        ax2 = ax1.twinx()  # Instantiate a second y-axis that shares the same x-axis
        ax2.set_ylabel('Aggregate Daily Sentiment', color='tab:red')
        ax2.plot(aggregate_sentiment.index, aggregate_sentiment, color='tab:red', label='Aggregate Daily Sentiment')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        # Title and legend
        plt.title('Aggregate Returns and Daily Sentiment Over Time')
        fig.tight_layout()  # Adjust layout to make room for labels

        # Show plot
        plt.show()


   
