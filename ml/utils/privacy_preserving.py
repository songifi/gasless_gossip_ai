import numpy as np

class PrivacyPreserving:
    def __init__(self, epsilon=1.0):
        self.epsilon = epsilon  # Differential privacy parameter

    def add_noise(self, data: np.ndarray) -> np.ndarray:
        # Simple Laplace noise for differential privacy
        noise = np.random.laplace(0, 1.0 / self.epsilon, data.shape)
        return data + noise