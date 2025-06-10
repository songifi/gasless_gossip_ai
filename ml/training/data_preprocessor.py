import pandas as pd
import numpy as np

class DataPreprocessor:
    def __init__(self):
        self.stop_words = set(["the", "is", "and"])  # Simplified example

    def preprocess(self, texts: list) -> list:
        return [self._clean_text(text) for text in texts]

    def _clean_text(self, text: str) -> str:
        words = text.lower().split()
        return " ".join(word for word in words if word not in self.stop_words)