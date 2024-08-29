# src/publisher_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from urllib.parse import urlparse
import seaborn as sns


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder

class PublisherAnalysis:
    def __init__(self, df: pd.DataFrame):
        
        self.df = df
        self.model = None
        self.vectorizer = None
        self.label_encoder = None

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
        If email addresses are used as publisher names, identify unique domains to see if certain organizations contribute more frequently.
        """
        # Ensure 'publisher' column exists
        if 'publisher' not in self.df.columns:
            raise ValueError("DataFrame must contain a 'publisher' column.")

        # Extract domains from email addresses or URLs
        if self.df['publisher'].str.contains('@').any():
            # Extract domains from email addresses
            self.df['domain'] = self.df['publisher'].apply(lambda x: x.split('@')[1] if '@' in x else None)
        else:
            # Extract domains from URLs if they exist in the 'publisher' field
            self.df['domain'] = self.df['publisher'].apply(lambda x: urlparse(x).netloc if '.' in x else None)

        # Drop rows where domain extraction failed
        self.df.dropna(subset=['domain'], inplace=True)

        # Count occurrences of each domain
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


    def prepare_data(self):
        """
        Prepare data for training by encoding labels and splitting into train/test sets.
        This step requires a dataset with predefined categories.
        """
        # Ensure 'news_type' column exists with default value 'Other'
        if 'news_type' not in self.df.columns:
            self.df['news_type'] = 'Other'
        
        # Example: Load a sample dataset with predefined categories (replace with actual data source)
        sample_data = pd.DataFrame({
            'headline': [
                'Election results', 'Stock market rally', 'New tech breakthrough',
                'Sports team wins championship', 'Health tips for the flu season'
            ],
            'news_type': ['Politics', 'Economy', 'Technology', 'Sports', 'Health']
        })
        
        # Define all possible categories
        categories = ['Politics', 'Economy', 'Health', 'Technology', 'Sports', 'Other']
        
        # Encode labels
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(categories)  # Fit on all possible categories

        sample_data['news_type'] = self.label_encoder.transform(sample_data['news_type'])
        self.df['news_type'] = self.label_encoder.transform(self.df['news_type'])

        X = sample_data['headline']
        y = sample_data['news_type']
        
        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        return X_train, X_test, y_train, y_test

    def train_model(self):
        """
        Train a model to categorize news headlines using sample data.
        """
        X_train, X_test, y_train, y_test = self.prepare_data()

        # Create a pipeline with TF-IDF vectorizer and Logistic Regression
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.model = make_pipeline(self.vectorizer, LogisticRegression())
        
        # Train the model
        self.model.fit(X_train, y_train)

        # Evaluate model accuracy
        accuracy = self.model.score(X_test, y_test)
        print(f'Model accuracy: {accuracy:.2f}')

    def categorize_headline(self, headline):
        """
        Categorize a single headline using the trained model.
        """
        if self.model:
            prediction = self.model.predict([headline])[0]
            return self.label_encoder.inverse_transform([prediction])[0]  # Convert label back to original category
        else:
            return 'Other'

    def analyze_news_type(self):
        """
        Analyze the type of news reported by each publisher using the trained model.
        """
        # Ensure the model is trained
        if self.model is None:
            print("Training the model...")
            self.train_model()

        # Apply model to categorize headlines
        if self.model:
            self.df['news_type'] = self.df['headline'].apply(self.categorize_headline)

            # Count the number of articles for each news type per publisher
            news_type_counts = self.df.groupby(['publisher', 'news_type']).size().unstack().fillna(0)

            # Plot a heatmap to visualize the distribution of news types per publisher
            plt.figure(figsize=(12, 8))
            sns.heatmap(news_type_counts, cmap="YlGnBu", linewidths=0.5, annot=True, fmt="g")
            plt.title('Distribution of News Types per Publisher')
            plt.xlabel('News Type')
            plt.ylabel('Publisher')
            plt.show()

            return news_type_counts
        else:
            print("Model is not trained. Please train the model first.")
            return None
