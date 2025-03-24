"""Test script for sticker caching system"""
import os
import time
import sys
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)
from src.sticker_generator import StickerGenerator
import hashlib
from src.disk_cache import DiskCache
from src.memory_lru_cache import MemoryLRUCache
import shutil
from src.cached_sticker_generator import CachedStickerGenerator
import io
from PIL import Image



def save_sticker(sticker_data, filename):
    """Save sticker bytes to a file"""
    image = Image.open(io.BytesIO(sticker_data))
    image.save(filename)
    print(f"Saved sticker to {filename}")

def test_sticker_caching():
    """Test the sticker caching implementation"""
    print("=== Testing Sticker Generation Caching System ===\n")
    
    # Initialize components
    base_generator = StickerGenerator()
    memory_cache = MemoryLRUCache(max_items=10, max_size_mb=50)
    disk_cache = DiskCache(cache_dir="test_cache", max_size_gb=0.1, ttl=3600)
    
    # Create cached generator
    cached_generator = CachedStickerGenerator(
        generator_func=base_generator.generate,
        memory_cache=memory_cache,
        disk_cache=disk_cache
    )
    
    # Test prompts
    test_prompts = [
        "A cat wearing a hat",
        "A dog playing basketball",
        "A monkey typing on a computer",
        "An elephant painting a picture"
    ]
    
    # Additional parameters
    test_params = {
        "size": 512,
        "style": "cartoon"
    }
    
    # Run tests
    for prompt in test_prompts:
        print(f"\n=== Testing prompt: '{prompt}' ===")
        
        # First generation (should be a cache miss)
        print("\nFirst generation (cache miss expected):")
        result1 = cached_generator.generate_sticker(prompt, **test_params)
        print(f"Result size: {len(result1)} bytes")
        result1_hash = hashlib.md5(result1).hexdigest()
        print(f"Result hash: {result1_hash}")
        # save the sticker
        save_sticker(result1, f"sticker_{prompt.replace(' ', '_')}.png")

        # Second generation (should hit memory cache)
        print("\nSecond generation (memory cache hit expected):")
        result2 = cached_generator.generate_sticker(prompt, **test_params)
        print(f"Result size: {len(result2)} bytes")
        result2_hash = hashlib.md5(result2).hexdigest()
        print(f"Result hash: {result2_hash}")
        print(f"Results match: {'✅ Yes' if result1_hash == result2_hash else '❌ No'}")
        # save the sticker
        save_sticker(result1, f"sticker_{prompt.replace(' ', '_')}.png")
    
    # Test disk cache fallback by bypassing memory cache
    print("\n\n=== Testing disk cache fallback ===")
    # Use a new prompt
    new_prompt = "A giraffe riding a bicycle"
    
    # Generate and store in both caches
    print("\nInitial generation to populate caches:")
    result3 = cached_generator.generate_sticker(new_prompt, **test_params)
    result3_hash = hashlib.md5(result3).hexdigest()
    
    # Create a new generator that skips memory cache
    print("\nCreating new generator with empty memory cache:")
    new_memory_cache = MemoryLRUCache(max_items=0)  # Effectively disabled
    new_cached_generator = CachedStickerGenerator(
        generator_func=base_generator.generate,
        memory_cache=new_memory_cache,
        disk_cache=disk_cache  # Reuse the same disk cache
    )
    
    # Should hit disk cache
    print("\nGeneration with new generator (disk cache hit expected):")
    result4 = new_cached_generator.generate_sticker(new_prompt, **test_params)
    result4_hash = hashlib.md5(result4).hexdigest()
    print(f"Result hash: {result4_hash}")
    print(f"Results match original: {'✅ Yes' if result3_hash == result4_hash else '❌ No'}")
    
    # Get cache statistics
    print("\n=== Cache Statistics ===")
    stats = cached_generator.get_cache_stats()
    if stats["memory_cache"]:
        print(f"Memory cache: {stats['memory_cache']['items']} items, " 
              f"{stats['memory_cache']['size_bytes'] / 1024:.2f} KB, "
              f"{stats['memory_cache']['utilization_percent']}% utilization")
    
    print("\n=== Test completed successfully ✅ ===")
    
    shutil.rmtree("test_cache", ignore_errors=True)


if __name__ == "__main__":
    test_sticker_caching()