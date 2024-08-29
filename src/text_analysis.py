# src/text_analysis.py
import pandas as pd
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

class TextAnalysis:
    def __init__(self, df):
        """
        Initialize the TextAnalysis object with the DataFrame containing the data.
        
        :param df: DataFrame with the data to be analyzed
        """
        self.df = df

    def perform_sentiment_analysis(self):
        """
        Perform sentiment analysis on the headlines using TextBlob.
        
        :return: DataFrame with added 'sentiment' column, where each sentiment is a tuple of polarity and subjectivity
        """
        # Apply TextBlob to each headline to calculate sentiment
        self.df['sentiment'] = self.df['headline'].apply(lambda x: TextBlob(x).sentiment)
        
        # Optional: Separate polarity and subjectivity for easier analysis
        self.df['polarity'] = self.df['sentiment'].apply(lambda x: x.polarity)
        self.df['subjectivity'] = self.df['sentiment'].apply(lambda x: x.subjectivity)
        
        return self.df[['headline', 'polarity', 'subjectivity']]

    def extract_keywords(self, ngram_range=(1, 2), max_features=100):
        """
        Extract common keywords or phrases from the headlines using CountVectorizer.
        
        :param ngram_range: tuple, range of n-grams to consider (default is (1, 2) for unigrams and bigrams)
        :param max_features: int, maximum number of top keywords/phrases to return (default is 100)
        :return: DataFrame with keywords/phrases and their corresponding frequency counts
        """
        # Initialize CountVectorizer with given parameters
        vectorizer = CountVectorizer(ngram_range=ngram_range, max_features=max_features, stop_words='english')
        
        # Fit and transform the headlines to extract n-grams
        X = vectorizer.fit_transform(self.df['headline'])
        
        # Convert the matrix to a DataFrame for easier viewing
        keywords_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
        
        # Sum up the occurrences of each keyword/phrase and sort by frequency
        keyword_counts = keywords_df.sum(axis=0).sort_values(ascending=False)
        
        return keyword_counts

    def topic_modeling(self, n_topics=5, n_top_words=10):
        """
        Perform topic modeling using Latent Dirichlet Allocation (LDA) on the headlines.
        
        :param n_topics: int, the number of topics to extract (default is 5)
        :param n_top_words: int, the number of top words to display per topic (default is 10)
        :return: None, prints the top words for each topic
        """
        # Initialize CountVectorizer
        vectorizer = CountVectorizer(stop_words='english')
        
        # Fit and transform the headlines to get the document-term matrix
        X = vectorizer.fit_transform(self.df['headline'])
        
        # Initialize Latent Dirichlet Allocation model
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
        
        # Fit the LDA model on the data
        lda.fit(X)
        
        # Print the top words for each topic
        feature_names = vectorizer.get_feature_names_out()
        for topic_idx, topic in enumerate(lda.components_):
            print(f"Topic #{topic_idx + 1}:")
            print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
            print()

