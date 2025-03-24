"""Module for Cached Predictor implementation with Redis and in-memory fallback"""

from typing import List, Optional, Any
from .memory_cache import MemoryCache

class CachedPredictor:
    '''Cached version of the Predictor with Redis and in-memory fallback'''
    def __init__(self, predictor, primary_cache=None):
        self.predictor = predictor
        self.primary_cache = primary_cache
        self.fallback_cache = MemoryCache()  # In-memory fallback cache
        
        # Check if primary cache is available
        self.primary_available = False
        if self.primary_cache:
            self.primary_available = self.primary_cache.ping()
            if self.primary_available:
                print("Primary cache (Redis) is available and will be used for predictions")
            else:
                print("Primary cache (Redis) is not available, using in-memory fallback cache")

    def gen_m_words_n_predictions(self, m: int, n: int, input_text: str) -> List[str]:
        '''Cached version of N-Word Predictions with fallback'''
        cache_key = None
        
        # Try primary cache first (if available)
        if self.primary_available:
            cache_key = self.primary_cache.build_key(m, n, input_text)
            cached_result = self.primary_cache.get(cache_key)
            if cached_result:
                print(f"Primary cache hit for input: {input_text}")
                return cached_result
        
        # If primary cache misses or isn't available, try fallback cache
        if not cache_key:
            cache_key = self.fallback_cache.build_key(m, n, input_text)
        
        fallback_result = self.fallback_cache.get(cache_key)
        if fallback_result:
            print(f"Fallback cache hit for input: {input_text}")
            return fallback_result

        # Both caches missed, generate prediction
        result = self.predictor.gen_m_words_n_predictions(m, n, input_text)
        
        # Store in both caches for future use
        if self.primary_available:
            self.primary_cache.set(cache_key, result)
            print(f"Stored in primary cache: {input_text}")
        
        # Always store in fallback cache
        self.fallback_cache.set(cache_key, result)
        
        return result