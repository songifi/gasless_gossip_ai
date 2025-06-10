from .real_time_processor import RealTimeProcessor

class BatchProcessor:
    def __init__(self, wallet_address):
        self.processor = RealTimeProcessor(wallet_address)

    def process_batch(self, messages, recipients):
        return [self.processor.process_message(msg, recip) for msg, recip in zip(messages, recipients)]