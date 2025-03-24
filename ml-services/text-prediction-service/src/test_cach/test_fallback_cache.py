"""Test script to verify both Redis and in-memory fallback caching"""
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)
from src.predictor import Predictor
from src.cache import RedisCache
from src.memory_cache import MemoryCache
from src.cached_predictor import CachedPredictor
import time

# First, test Redis connectivity
redis_cache = RedisCache()
redis_available = redis_cache.ping()
print(f"Redis connectivity: {'✅ Connected' if redis_available else '❌ Not connected'}")

# Create the predictor components
base_predictor = Predictor()
cached_predictor = CachedPredictor(base_predictor, redis_cache)

# Test the prediction pipeline
test_input = "I would like to"
cache_key = redis_cache.build_key(2, 3, test_input)
print(f"Cache key being used: {cache_key}")

# Run predictions and time them
def run_prediction(prompt, message):
    print(f"\n{message}: '{prompt}'")
    start_time = time.time()
    result = cached_predictor.gen_m_words_n_predictions(2, 3, prompt)
    end_time = time.time()
    print(f"Results: {result}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    return result

# First run - should be a cache miss in both caches
result1 = run_prediction(test_input, "First prediction (cache miss expected)")

# Check if stored in Redis
redis_value = redis_cache.get(cache_key) if redis_available else None
print(f"After first prediction, Redis cache has value: {redis_value is not None}")

# Second run - should hit one of the caches
result2 = run_prediction(test_input, "Second prediction (cache hit expected)")

# Verify results match
print(f"\nResults match: {'✅ Yes' if result1 == result2 else '❌ No'}")

# Test with Redis unavailable (if it was available before)
if redis_available:
    print("\n===== Testing fallback cache behavior =====")
    # Create a new predictor with a non-working Redis cache
    class NonWorkingRedisCache(RedisCache):
        def ping(self):
            return False
        def get(self, key):
            return None
    
    # Create predictor with non-working Redis
    non_working_redis = NonWorkingRedisCache()
    fallback_predictor = CachedPredictor(base_predictor, non_working_redis)
    
    # Run predictions with fallback
    print("\nFirst prediction with fallback cache only:")
    start_time = time.time()
    fallback_result1 = fallback_predictor.gen_m_words_n_predictions(2, 3, test_input + " test")
    end_time = time.time()
    print(f"Results: {fallback_result1}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    print("\nSecond prediction with fallback cache only (should be faster):")
    start_time = time.time()
    fallback_result2 = fallback_predictor.gen_m_words_n_predictions(2, 3, test_input + " test")
    end_time = time.time()
    print(f"Results: {fallback_result2}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    print(f"\nFallback results match: {'✅ Yes' if fallback_result1 == fallback_result2 else '❌ No'}")

print("\nCaching implementation test completed ✅")