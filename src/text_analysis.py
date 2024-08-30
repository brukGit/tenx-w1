# src/text_analysis.py
import pandas as pd

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
class TextAnalysis:
    def __init__(self, df):
        """
        Initialize the TextAnalysis object with the DataFrame containing the data.
        
        :param df: DataFrame with the data to be analyzed
        """
        self.df = df

    

    def perform_sentiment_analysis(self):
        """
        Perform sentiment analysis on the headlines using VADER's SentimentIntensityAnalyzer.
        
        :return: DataFrame with added 'sentiment' column, where each sentiment is classified as positive, neutral, negative, or strong negative.
        """
        # Initialize VADER sentiment intensity analyzer
        analyzer = SentimentIntensityAnalyzer()
        
        # Function to classify sentiment based on compound score
        def classify_sentiment(compound):
            if compound >= 0.5:
                return 'positive'
            elif 0.05 <= compound < 0.5:
                return 'neutral'
            elif -0.5 < compound < 0.05:
                return 'negative'
            else:
                return 'strong negative'
        
        # Apply VADER sentiment analysis to each headline
        self.df['sentiment'] = self.df['headline'].apply(lambda x: analyzer.polarity_scores(x))
        
        # Extract compound score for simplicity
        self.df['compound'] = self.df['sentiment'].apply(lambda x: x['compound'])
        
        # Classify sentiment based on compound score
        self.df['sentiment_class'] = self.df['compound'].apply(classify_sentiment)
        
        # Separate polarity (compound score) and subjectivity (not provided by VADER, so kept simple)
        self.df['polarity'] = self.df['compound']
        self.df['subjectivity'] = self.df['headline'].apply(lambda x: analyzer.polarity_scores(x)['neu'])  # Approximation using neutrality

        # Plot pie chart
        sentiment_counts = self.df['sentiment_class'].value_counts()
        plt.figure(figsize=(8, 6))
        plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140)
        plt.title('Sentiment Distribution')
        plt.show()

        return self.df[['headline', 'polarity', 'subjectivity', 'sentiment_class']]


    def extract_keywords(self, ngram_range=(2, 3), max_features=100):
        """
        Extract common keywords or phrases from the headlines using TfidfVectorizer.
        
        :param ngram_range: tuple, range of n-grams to consider (default is (2, 3) for unigrams, bigrams, and trigrams)
        :param max_features: int, maximum number of top keywords/phrases to return (default is 100)
        :return: DataFrame with keywords/phrases and their corresponding frequency counts
        """
        # Extend the default stop words list
        custom_stop_words = stopwords.words('english') 
        
        # Initialize TfidfVectorizer with given parameters
        vectorizer = TfidfVectorizer(ngram_range=ngram_range, max_features=max_features, stop_words=custom_stop_words)
        
        # Fit and transform the headlines to extract n-grams
        X = vectorizer.fit_transform(self.df['headline'])
        
        # Convert the matrix to a DataFrame for easier viewing
        phrases_df = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
        
        # Sum up the occurrences of each phrase and sort by frequency
        phrase_counts = phrases_df.sum(axis=0).sort_values(ascending=False)
        
        return phrase_counts

    def topic_modeling(self, n_topics=5, n_top_words=10):
        """
        Perform topic modeling using Latent Dirichlet Allocation (LDA).

        Parameters:
        - n_topics: Number of topics to extract
        - n_top_words: Number of top words to display for each topic
        """
        # Ensure that 'headline' column exists and is not empty
        if 'headline' not in self.df.columns or self.df['headline'].empty:
            raise ValueError("DataFrame must contain a non-empty 'headline' column")

        # Preprocessing and vectorization
        tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.95, min_df=2)
        tfidf = tfidf_vectorizer.fit_transform(self.df['headline'])

        # Fit LDA model
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=42, n_jobs=-1)
        lda.fit(tfidf)

        # Display topics
        feature_names = tfidf_vectorizer.get_feature_names_out()
        topics = []
        for topic_idx, topic in enumerate(lda.components_):
            top_words = [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
            topics.append(f"Topic {topic_idx}: {' '.join(top_words)}")
        
        return topics