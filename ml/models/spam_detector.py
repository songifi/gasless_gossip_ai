from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

class SpamDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.model = LogisticRegression()
        self.is_trained = False

    def train(self, texts, labels):
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)
        self.is_trained = True

    def is_spam(self, message):
        if not self.is_trained:
            raise ValueError("Model not trained")
        X = self.vectorizer.transform([message])
        return self.model.predict(X)[0] == 1