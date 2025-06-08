from sklearn.metrics import accuracy_score, precision_recall_fscore_support

class ModelEvaluator:
    def __init__(self, model):
        self.model = model

    def evaluate(self, X_test, y_test):
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(y_test, predictions, average="binary")
        return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}