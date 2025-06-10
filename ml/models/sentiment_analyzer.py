from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    def analyze(self, message):
        result = self.analyzer(message)[0]
        return {
            "label": result["label"],
            "score": result["score"],
            "urgency": 1.0 if result["label"] == "POSITIVE" and result["score"] > 0.8 else 0.5
        }