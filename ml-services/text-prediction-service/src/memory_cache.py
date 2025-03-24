"""In-memory cache implementation for text prediction service"""

import time
from typing import List, Optional, Dict, Any, Tuple


class MemoryCache:
    """In-memory cache client that serves as a fallback when Redis is unavailable"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        """Initialize in-memory cache
        
        Args:
            max_size: Maximum number of items to store in cache
            ttl: Time-to-live in seconds (default 1 hour)
        """
        self.cache: Dict[str, Tuple[List[str], float]] = {}  # {key: (value, timestamp)}
        self.max_size = max_size
        self.ttl = ttl
        print(f"Initialized in-memory cache with max_size={max_size}, ttl={ttl}")
    
    def _clean_expired_entries(self) -> None:
        """Remove expired entries from cache"""
        current_time = time.time()
        expired_keys = [
            k for k, (_, timestamp) in self.cache.items() 
            if current_time - timestamp > self.ttl
        ]
        for key in expired_keys:
            del self.cache[key]
    
    def _evict_if_needed(self) -> None:
        """Remove oldest entries if cache exceeds max size"""
        if len(self.cache) >= self.max_size:
            # Sort by timestamp (oldest first) and remove oldest items
            sorted_items = sorted(self.cache.items(), key=lambda x: x[1][1])
            # Remove 10% of oldest items
            items_to_remove = max(1, int(self.max_size * 0.1))
            for i in range(items_to_remove):
                if i < len(sorted_items):
                    del self.cache[sorted_items[i][0]]
    
    def get(self, key: str) -> Optional[List[str]]:
        """Get cached prediction results by key"""
        self._clean_expired_entries()
        if key in self.cache:
            value, _ = self.cache[key]
            print(f"In-memory cache hit for key: {key}")
            return value
        print(f"In-memory cache miss for key: {key}")
        return None
    
    def set(self, key: str, value: List[str]) -> bool:
        """Set prediction results in cache with timestamp"""
        self._evict_if_needed()
        self.cache[key] = (value, time.time())
        print(f"Stored in in-memory cache: {key}")
        return True
    
    def build_key(self, tokens: int, predictions: int, text: str) -> str:
        """Build a consistent cache key based on input parameters"""
        return f"pred:{text}:{tokens}:{predictions}"
    
    def ping(self) -> bool:
        """Always returns True as in-memory cache is always available"""
        return True