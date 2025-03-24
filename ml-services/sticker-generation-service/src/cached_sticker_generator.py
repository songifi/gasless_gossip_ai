"""Cached sticker generator implementation"""

import time
from typing import Dict, Any, Optional, Union, Callable
from .memory_lru_cache import MemoryLRUCache
from .disk_cache import DiskCache


class CachedStickerGenerator:
    """Two-level cached wrapper for sticker generator"""
    
    def __init__(self, generator_func: Callable, memory_cache: Optional[MemoryLRUCache] = None, 
                 disk_cache: Optional[DiskCache] = None):
        """Initialize cached sticker generator
        
        Args:
            generator_func: Function that generates stickers from prompts
            memory_cache: In-memory LRU cache (optional)
            disk_cache: Disk-based cache (optional)
        """
        self.generator_func = generator_func
        self.memory_cache = memory_cache or MemoryLRUCache()
        self.disk_cache = disk_cache or DiskCache()
        
        # Check cache availability
        self.memory_available = self.memory_cache.ping()
        self.disk_available = self.disk_cache.ping()
        
        print(f"Cached sticker generator initialized.")
        print(f"Memory cache available: {self.memory_available}")
        print(f"Disk cache available: {self.disk_available}")
    
    def generate_sticker(self, prompt: str, **kwargs) -> bytes:
        """Generate a sticker with caching
        
        Args:
            prompt: Text prompt for sticker generation
            **kwargs: Additional generation parameters
            
        Returns:
            Generated sticker image as bytes
        """
        start_time = time.time()
        
        # Build cache key
        if self.memory_available:
            cache_key = self.memory_cache.build_key(prompt, **kwargs)
        elif self.disk_available:
            cache_key = self.disk_cache.build_key(prompt, **kwargs)
        else:
            # No caching available
            print("No caching available, generating sticker without caching")
            return self.generator_func(prompt, **kwargs)
        
        # Try memory cache first (fastest)
        if self.memory_available:
            memory_result = self.memory_cache.get(cache_key)
            if memory_result:
                print(f"Memory cache hit for '{prompt}'")
                print(f"Retrieved in {(time.time() - start_time) * 1000:.2f}ms")
                return memory_result
        
        # Try disk cache next
        if self.disk_available:
            disk_result = self.disk_cache.get(cache_key)
            if disk_result:
                print(f"Disk cache hit for '{prompt}'")
                
                # Store in memory cache for faster future access
                if self.memory_available:
                    self.memory_cache.set(cache_key, disk_result)
                    
                print(f"Retrieved in {(time.time() - start_time) * 1000:.2f}ms")
                return disk_result
        
        # Cache miss, generate sticker
        print(f"Cache miss for '{prompt}', generating new sticker")
        generation_start = time.time()
        result = self.generator_func(prompt, **kwargs)
        generation_time = time.time() - generation_start
        
        print(f"Sticker generation took {generation_time * 1000:.2f}ms")
        
        # Store in both caches
        if self.memory_available:
            self.memory_cache.set(cache_key, result)
            
        if self.disk_available:
            self.disk_cache.set(cache_key, result)
        
        total_time = time.time() - start_time
        print(f"Total time including caching: {total_time * 1000:.2f}ms")
        
        return result
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get statistics about the caches"""
        stats = {
            "memory_cache": None,
            "disk_cache": {
                "available": self.disk_available
            }
        }
        
        if self.memory_available:
            stats["memory_cache"] = self.memory_cache.stats()
            
        return stats