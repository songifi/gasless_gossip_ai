from .models.spam_detector import SpamDetector
from .models.sentiment_analyzer import SentimentAnalyzer
from .models.routing_optimizer import RoutingOptimizer

class RealTimeProcessor:
    def __init__(self, wallet_address):
        self.spam_detector = SpamDetector()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.routing_optimizer = RoutingOptimizer(network_graph={})  # Placeholder graph
        self.wallet = wallet_address

    def process_message(self, message, recipient):
        if self.spam_detector.is_spam(message):
            return {"status": "blocked", "reason": "spam_detected"}
        
        sentiment = self.sentiment_analyzer.analyze(message)
        optimal_route = self.routing_optimizer.find_path(
            sender=self.wallet, recipient=recipient, message_priority=sentiment["urgency"]
        )
        return {"status": "processed", "route": optimal_route, "sentiment": sentiment}