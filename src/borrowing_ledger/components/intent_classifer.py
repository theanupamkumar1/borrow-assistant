import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, ne_chunk

class IntentClassifier:
    def __init__(self):
        # Download necessary NLTK data
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('maxent_ne_chunker', quiet=True)
        nltk.download('words', quiet=True)

        self.pipeline = None

    @staticmethod
    def clean_text(text):
        """
        Clean the text data by removing non-alphanumeric characters,
        converting to lowercase, removing stop words and named entities,
        and applying lemmatization.
        """
        text = re.sub(r"[^a-zA-Z\s]", ' ', text)
        custom_stop_words = ["ka", "ke", "ki", "unka", "unke", "se", "de", "do"]
        words = word_tokenize(text.lower())
        pos_tags = pos_tag(words)
        named_entities = ne_chunk(pos_tags, binary=True)
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word, tag in named_entities.leaves()
                 if word.lower() not in custom_stop_words and tag != 'NE']
        return ' '.join(words)

    class TextCleaner:
        def fit(self, X, y=None):
            return self

        def transform(self, X):
            return [IntentClassifier.clean_text(text) for text in X]

    def train(self, data_path):
        # Load the data
        df = pd.read_csv(data_path)
        df.columns = ['text', 'intent']
        X = df['text']
        y = df['intent']

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

        # Create the pipeline
        self.pipeline = Pipeline([
            ('cleaner', self.TextCleaner()),
            ('vectorizer', CountVectorizer(max_features=5000)),
            ('classifier', MultinomialNB())
        ])

        # Fit the pipeline
        self.pipeline.fit(X_train, y_train)

        # Evaluate the model
        y_pred = self.pipeline.predict(X_test)
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

    def predict_intent(self, phrase):
        if self.pipeline is None:
            raise ValueError("Model not trained. Call train() method first.")
        return self.pipeline.predict([phrase])[0]

    def save_model(self, filepath):
        if self.pipeline is None:
            raise ValueError("Model not trained. Call train() method first.")
        joblib.dump(self.pipeline, filepath)
        print(f"Model saved as '{filepath}'")

    def load_model(self, filepath):
        self.pipeline = joblib.load(filepath)
        print(f"Model loaded from '{filepath}'")

# Example usage
if __name__ == "__main__":
   
    
    # Train the model
    classifier.train(r"C:\Users\anupam kumar\Downloads\borrow-assistant\artifacts\intent-classifier_data.csv")

    # Save the model
    classifier.save_model('intent_classification_pipeline.joblib')

    # Test phrases
    test_phrases = [
        "subham ka total kitna hai",
        "meena ke 40 rupee kaat do",
        "Hata do 30 rupaye wali entry",
        "40 rupee likh do mina ke",
        "aau ke 30 rupee jama kar do",
        "bhvaesh ke 20 rupee likh do"
    ]

    # Test the classifier on the phrases
    print("\nTesting classifier on new phrases:")
    for phrase in test_phrases:
        intent = classifier.predict_intent(phrase)
        print(f"Phrase: {phrase}")
        print(f"Predicted Intent: {intent}\n")