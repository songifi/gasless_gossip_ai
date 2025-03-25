"""Disk-based cache implementation for sticker generation service"""

import os
import json
import hashlib
import time
from typing import Optional, Dict, Any, Union
from pathlib import Path


class DiskCache:
    """Disk-based cache for storing generated sticker images"""
    
    def __init__(self, cache_dir: str = "cache", max_size_gb: float = 1.0, ttl: int = 86400):
        """Initialize disk cache
        
        Args:
            cache_dir: Directory to store cached files
            max_size_gb: Maximum cache size in gigabytes
            ttl: Time-to-live in seconds (default 24 hours)
        """
        self.cache_dir = Path(cache_dir)
        self.metadata_file = self.cache_dir / "metadata.json"
        self.max_size_bytes = int(max_size_gb * 1024 * 1024 * 1024)  # Convert GB to bytes
        self.ttl = ttl
        self.metadata: Dict[str, Dict[str, Any]] = {}
        
        # Create cache directory if it doesn't exist
        if not self.cache_dir.exists():
            self.cache_dir.mkdir(parents=True)
            
        # Load metadata if it exists
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
            except json.JSONDecodeError:
                # If metadata file is corrupted, start fresh
                self.metadata = {}
                
        print(f"Initialized disk cache at {self.cache_dir}, max_size={max_size_gb}GB, ttl={ttl}s")
    
    def _save_metadata(self) -> None:
        """Save metadata to disk"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f)
    
    def _clean_expired_entries(self) -> None:
        """Remove expired entries from cache"""
        current_time = time.time()
        expired_keys = []
        
        for key, info in self.metadata.items():
            if current_time - info['timestamp'] > self.ttl:
                expired_keys.append(key)
                # Delete the associated file
                try:
                    os.remove(self.cache_dir / info['filename'])
                except OSError:
                    pass  # File might already be gone
        
        # Remove expired entries from metadata
        for key in expired_keys:
            del self.metadata[key]
            
        if expired_keys:
            self._save_metadata()
            print(f"Removed {len(expired_keys)} expired entries from disk cache")
    
    def _enforce_size_limit(self) -> None:
        """Enforce cache size limit by removing oldest entries"""
        # Check current cache size
        total_size = sum(info['size'] for info in self.metadata.values())
        
        if total_size <= self.max_size_bytes:
            return
            
        # Sort entries by timestamp (oldest first)
        sorted_entries = sorted(self.metadata.items(), key=lambda x: x[1]['timestamp'])
        
        # Remove oldest entries until we're under the size limit
        removed_size = 0
        removed_keys = []
        
        for key, info in sorted_entries:
            if total_size - removed_size <= self.max_size_bytes:
                break
                
            try:
                os.remove(self.cache_dir / info['filename'])
                removed_size += info['size']
                removed_keys.append(key)
            except OSError:
                # File might already be gone
                removed_keys.append(key)
        
        # Update metadata
        for key in removed_keys:
            del self.metadata[key]
            
        if removed_keys:
            self._save_metadata()
            print(f"Removed {len(removed_keys)} entries to enforce size limit")
    
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
        
        if key not in self.metadata:
            print(f"Disk cache miss for {key}")
            return None
            
        file_path = self.cache_dir / self.metadata[key]['filename']
        if not file_path.exists():
            # File is missing but in metadata, remove entry
            del self.metadata[key]
            self._save_metadata()
            print(f"Disk cache miss (file missing): {key}")
            return None
            
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                print(f"Disk cache hit for {key}")
                
                # Update access timestamp
                self.metadata[key]['timestamp'] = time.time()
                self._save_metadata()
                
                return data
        except Exception as e:
            print(f"Error reading from disk cache: {e}")
            return None
    
    def set(self, key: str, data: bytes) -> bool:
        """Store sticker image in cache
        
        Args:
            key: Cache key
            data: Image data to store
            
        Returns:
            True if stored successfully, False otherwise
        """
        try:
            # Generate a filename from the key
            filename = f"{key.split(':')[1]}.png"
            file_path = self.cache_dir / filename
            
            # Write the data to disk
            with open(file_path, 'wb') as f:
                f.write(data)
                
            # Update metadata
            self.metadata[key] = {
                'filename': filename,
                'size': len(data),
                'timestamp': time.time()
            }
            
            self._save_metadata()
            print(f"Stored in disk cache: {key}")
            
            # Enforce size limits
            self._enforce_size_limit()
            
            return True
        except Exception as e:
            print(f"Error writing to disk cache: {e}")
            return False
    
    def ping(self) -> bool:
        """Check if disk cache is available"""
        return self.cache_dir.exists() and os.access(self.cache_dir, os.W_OK)