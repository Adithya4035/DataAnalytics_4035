import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import scipy
import joblib
import os
import random

class SarcasmDetector:
    def __init__(self, train_data_path=None, test_data_path=None, model=None, vectorizer=None):
        self.train_data_path = train_data_path
        self.test_data_path = test_data_path
        self.train_data = None
        self.test_data = None
        self.vectorizer = vectorizer if vectorizer else TfidfVectorizer(max_features=1000)
        self.model = model if model else LogisticRegression()

    def load_data(self):
        try:
            self.train_data = pd.read_csv(self.train_data_path, encoding='ISO-8859-1')
            self.test_data = pd.read_csv(self.test_data_path, encoding='ISO-8859-1')
        except Exception as e:
            raise ValueError(f"Error loading data: {e}")

    def preprocess_text(self, text):
        if pd.isnull(text):
            return ''
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(text.lower())
        tokens = [word for word in tokens if word.isalpha() and word not in stop_words and word not in string.punctuation]
        return ' '.join(tokens)

    def preprocess_data(self):
        if self.train_data is None or self.test_data is None:
            raise ValueError("Data not loaded.")
        
        self.train_data['clean_text'] = self.train_data['body'].apply(self.preprocess_text)
        self.test_data['clean_text'] = self.test_data['body'].apply(self.preprocess_text)
        
        self.train_data['clean_text'] = self.train_data['clean_text'].fillna('')
        self.test_data['clean_text'] = self.test_data['clean_text'].fillna('')

    def vectorize_data(self):
        if self.train_data is None or self.test_data is None:
            raise ValueError("Data not loaded.")
        
        X_train = self.vectorizer.fit_transform(self.train_data['clean_text'])
        X_test = self.vectorizer.transform(self.test_data['clean_text'])
        
        if not isinstance(X_train, scipy.sparse.csr_matrix) or not isinstance(X_test, scipy.sparse.csr_matrix):
            raise ValueError("Vectorized data is not a valid sparse matrix.")
        
        return X_train, X_test

    def train_model(self):
        X_train, _ = self.vectorize_data()
        self.model.fit(X_train, self.train_data['sarcasm_tag'])

    def calculate_sarcasm_score(self, text):
        sarcasm_score = random.uniform(0.0000,1.0000)
        return sarcasm_score

    def evaluate_model(self):
        _, X_test = self.vectorize_data()
        y_pred = self.model.predict(X_test)
        report = classification_report(self.test_data['sarcasm_tag'], y_pred, zero_division=1)
        accuracy = accuracy_score(self.test_data['sarcasm_tag'], y_pred)
        print("Classification Report:")
        print(report)
        print("Accuracy:", accuracy)

    def save_model(self):
        os.makedirs(os.path.dirname('models/sarcasm_detector_model.pkl'), exist_ok=True)
        joblib.dump(self.model, 'models/sarcasm_detector_model.pkl')
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.vectorizer, 'models/tfidf_vectorizer.pkl')

    def run(self):
        self.load_data()
        self.preprocess_data()
        self.train_model()
        self.evaluate_model()
        self.save_model()

# Example usage:
if __name__ == "__main__":
    sarcasm_detector = SarcasmDetector(r"D:\Sarcasm\reddit_training.csv", r"D:\Sarcasm\reddit_test.csv")
    sarcasm_detector.run()
