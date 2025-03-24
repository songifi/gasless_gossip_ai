import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from src.cache import RedisCache
from src.predictor import Predictor
from src.cached_predictor import CachedPredictor

# Test basic Redis connectivity
cache = RedisCache()
print(f"Redis connectivity: {'✅ Connected' if cache.ping() else '❌ Not connected'}")


# Use the CachedPredictor, not the base Predictor
base_predictor = Predictor()
predictor = CachedPredictor(base_predictor, cache)

# Test with a simple prediction
test_input = "I would like to"
cache_key = cache.build_key(2, 3, test_input)
print(f"Cache key being used: {cache_key}")

print(f"\nRunning first prediction for: '{test_input}'")
# First run - should be a cache miss
start_time = __import__('time').time()
result1 = predictor.gen_m_words_n_predictions(2, 3, test_input)
end_time = __import__('time').time()
print(f"Results: {result1}")
print(f"Time taken: {end_time - start_time:.2f} seconds")
cached_value = cache.get(cache_key)
print(f"After first prediction, cache has value: {cached_value is not None}")

print(f"\nRunning second prediction (should be cached):")
# Second run - should be a cache hit and much faster
start_time = __import__('time').time()
result2 = predictor.gen_m_words_n_predictions(2, 3, test_input)
end_time = __import__('time').time()
print(f"Results: {result2}")
print(f"Time taken: {end_time - start_time:.2f} seconds")

# Verify results are the same
print(f"\nResults match: {'✅ Yes' if result1 == result2 else '❌ No'}")