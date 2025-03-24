"""In-memory LRU cache implementation for sticker generation service"""

import hashlib
import time
from typing import Optional, Dict, Any, Tuple, List
from collections import OrderedDict


class MemoryLRUCache:
    """In-memory LRU cache for storing frequently accessed stickers"""
    
    def __init__(self, max_items: int = 100, max_size_mb: int = 100, ttl: int = 3600):
        """Initialize in-memory LRU cache
        
        Args:
            max_items: Maximum number of items to store
            max_size_mb: Maximum cache size in megabytes
            ttl: Time-to-live in seconds (default 1 hour)
        """
        self.cache: OrderedDict[str, Tuple[bytes, int, int]] = OrderedDict()  # {key: (data, timestamp, size)}
        self.max_items = max_items
        self.max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
        self.ttl = ttl
        self.current_size_bytes = 0
        
        print(f"Initialized in-memory LRU cache with max_items={max_items}, max_size={max_size_mb}MB, ttl={ttl}s")
    
    def _clean_expired_entries(self) -> None:
        """Remove expired entries from cache"""
        current_time = time.time()
        expired_keys = [
            k for k, (_, timestamp, _) in self.cache.items() 
            if current_time - timestamp > self.ttl
        ]
        
        for key in expired_keys:
            _, _, size = self.cache[key]
            del self.cache[key]
            self.current_size_bytes -= size
            
        if expired_keys:
            print(f"Removed {len(expired_keys)} expired entries from memory cache")
    
    def build_key(self, prompt: str, **kwargs) -> str:
        """Build a cache key from the sticker generation parameters
        
        Args:
            prompt: The text prompt used to generate the sticker
            **kwargs: Additional generation parameters
        
        Returns:
            A cache key string
        """
        # Create a deterministic representation of generation parameters
        param_str = prompt
        for k in sorted(kwargs.keys()):
            param_str += f"|{k}:{kwargs[k]}"
            
        # Create a hash to use as the key
        return f"sticker:{hashlib.md5(param_str.encode()).hexdigest()}"
    
    def get(self, key: str) -> Optional[bytes]:
        """Get cached sticker image by key
        
        Args:
            key: Cache key
            
        Returns:
            Image data as bytes or None if not in cache
        """
        self._clean_expired_entries()
        
        if key not in self.cache:
            print(f"Memory cache miss for {key}")
            return None
            
        # Move to end (most recently used)
        data, timestamp, size = self.cache.pop(key)
        self.cache[key] = (data, time.time(), size)  # Update timestamp
        
        print(f"Memory cache hit for {key}")
        return data
    

    def set(self, key: str, data: bytes) -> bool:
        """Store sticker image in cache"""
        # If max_items is 0, don't store anything
        if self.max_items <= 0:
            print(
                f"Memory cache disabled (max_items={self.max_items}), not storing")
            return False

        self._clean_expired_entries()

        # Calculate size of new item
        data_size = len(data)

        # If item is larger than max size, don't cache it
        if data_size > self.max_size_bytes:
            print(f"Item too large for memory cache: {data_size} bytes")
            return False

        # Remove existing item if present
        if key in self.cache:
            _, _, old_size = self.cache[key]
            self.current_size_bytes -= old_size
            del self.cache[key]

        # Make room if needed (by size)
        while self.cache and self.current_size_bytes + data_size > self.max_size_bytes:
            # Remove least recently used (first item)
            if self.cache:  # Make sure cache isn't empty
                removed_key, (_, _, removed_size) = next(iter(self.cache.items()))
                del self.cache[removed_key]
                self.current_size_bytes -= removed_size
                print(
                    f"Evicted item from memory cache to make room: {removed_key}")

        # Make room if needed (by count)
        while self.cache and len(self.cache) >= self.max_items:
            # Remove least recently used (first item)
            removed_key, (_, _, removed_size) = next(iter(self.cache.items()))
            del self.cache[removed_key]
            self.current_size_bytes -= removed_size
            print(f"Evicted item from memory cache (count limit): {removed_key}")

        # Add to cache
        self.cache[key] = (data, time.time(), data_size)
        self.current_size_bytes += data_size

        print(f"Stored in memory cache: {key}")
        return True
    
    def ping(self) -> bool:
        """Always returns True as in-memory cache is always available"""
        return True
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "items": len(self.cache),
            "size_bytes": self.current_size_bytes,
            "max_items": self.max_items,
            "max_size_bytes": self.max_size_bytes,
            "utilization_percent": round(self.current_size_bytes / self.max_size_bytes * 100, 2) if self.max_size_bytes > 0 else 0
        }