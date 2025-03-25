"""Redis cache implementation for text prediction service"""

import os
import json
import redis
from typing import List, Optional, Any


class RedisCache:
    """Redis cache client for the text prediction service"""
    
    def __init__(self):
        """Initialize Redis connection from environment variables"""
        host = os.getenv("REDIS_HOST", "localhost")
        port = int(os.getenv("REDIS_PORT", 6379))
        self.ttl = int(os.getenv("REDIS_TTL", 3600))  # Default 1 hour
        
        # Initialize Redis client
        self.redis_client = redis.Redis(
            host=host,
            port=port,
            decode_responses=True  # Automatically decode responses to Python strings
        )
        
    def get(self, key: str) -> Optional[List[str]]:
        """Get cached prediction results by key"""
        try:
            cached_value = self.redis_client.get(key)
            if cached_value:
                return json.loads(cached_value)
            return None
        except Exception as e:
            # Log the error but don't fail if cache is unavailable
            print(f"Cache error on get: {str(e)}")
            return None
    
    def set(self, key: str, value: List[str]) -> bool:
        """Set prediction results in cache with TTL"""
        try:
            self.redis_client.setex(
                key,
                self.ttl,
                json.dumps(value)
            )
            return True
        except Exception as e:
            # Log the error but don't fail if cache is unavailable
            print(f"Cache error on set: {str(e)}")
            return False
    
    def build_key(self, tokens: int, predictions: int, text: str) -> str:
        """Build a consistent cache key based on input parameters"""
        # Create a standardized key with all parameters to ensure uniqueness
        return f"pred:{text}:{tokens}:{predictions}"
    
    def ping(self) -> bool:
        """Check if Redis is available"""
        try:
            return self.redis_client.ping()
        except:
            return False