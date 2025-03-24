# Caching Implementation Documentation

This document describes the caching implementations for both the Text Prediction Service and Sticker Generation Service, including configuration, usage, testing procedures, and fallback mechanisms.

## Text Prediction Service Caching

### Architecture
The text prediction service uses a two-tier caching strategy:

1. **Primary Redis Cache**
   - Persistent storage across service restarts
   - Shared cache across multiple service instances
   - Configurable TTL (Time-To-Live)
   - Stores prediction results as JSON data

2. **In-Memory Fallback Cache**
   - Automatically used when Redis is unavailable
   - Maintains cached predictions in local memory
   - LRU (Least Recently Used) eviction policy
   - Provides resilience when Redis is down

### Key Components

- **RedisCache**: Handles interactions with Redis server
- **MemoryCache**: Provides fallback when Redis is unavailable
- **CachedPredictor**: Wrapper that implements caching behavior around the base predictor

### Configuration

Redis cache configuration is managed through environment variables:
```
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_TTL=3600  # Cache TTL in seconds (1 hour)
```

Memory cache configuration:
```python
# Default settings in code
max_size = 1000  # Maximum number of entries
ttl = 3600       # Time-to-live in seconds
```

### Fallback Mechanism

The caching system implements an automatic fallback strategy:

1. First tries to use Redis for all cache operations
2. If Redis is unavailable (server down, connection issues, etc.), automatically falls back to in-memory cache
3. If prediction isn't found in either cache, generates a new prediction and caches it in all available caches

This ensures high availability even during Redis outages.

### Testing

To test the text prediction caching implementation:

1. Make sure Redis is running (if testing Redis functionality)
   ```bash
   # Check Redis status
   redis-cli ping
   
   # Start Redis if needed
   brew services start redis  # on macOS
   sudo service redis-server start  # on Ubuntu/Debian
   ```

2. Run the test script
   ```bash
   # From the text-prediction-service directory
   python3 test_fallback_cache.py
   ```

3. The test will verify:
   - Redis connectivity
   - Cache hit/miss functionality
   - Fallback behavior
   - Performance improvements

### Performance Impact

Tests show significant performance improvements:
- First request: ~0.7-0.9 seconds
- Cached requests: ~0.001 seconds (99.9% faster)

## Sticker Generation Service Caching

### Architecture
The sticker generation service implements a two-level caching strategy:

1. **Memory LRU Cache (Level 1)**
   - Stores most frequently accessed stickers in RAM
   - Fastest possible retrieval
   - Limited by configurable memory limits
   - LRU (Least Recently Used) eviction policy

2. **Disk Cache (Level 2)**
   - Stores larger volumes of stickers on disk
   - Persists between service restarts
   - Size and time-based eviction policies
   - Serves as fallback when stickers aren't in memory cache

### Key Components

- **MemoryLRUCache**: Fast in-memory cache with LRU eviction
- **DiskCache**: File-based persistence with metadata tracking
- **CachedStickerGenerator**: Coordinates between caching layers and the generator
- **StickerGenerator**: Mock implementation for testing (would be replaced with actual diffusion model in production)

### Mock Implementation Note

For testing purposes, the sticker generation service uses a mock implementation that:
- Simulates the behavior of a diffusion model
- Creates simple colored images with text and shapes
- Adds randomized processing delays to mimic actual generation time
- Produces unique image content for each prompt

In a production environment, this would be replaced with an actual diffusion model like Stable Diffusion, but the caching mechanism remains the same.

### Configuration

Memory cache configuration:
```python
memory_cache = MemoryLRUCache(
    max_items=100,      # Maximum number of stickers
    max_size_mb=100,    # Maximum size in megabytes
    ttl=3600            # Time-to-live in seconds
)
```

Disk cache configuration:
```python
disk_cache = DiskCache(
    cache_dir="sticker_cache",  # Directory for cached files
    max_size_gb=1.0,            # Maximum size in gigabytes
    ttl=86400                   # Time-to-live in seconds (1 day)
)
```

### Fallback Mechanism

The sticker caching system implements a multi-level fallback strategy:

1. First check memory cache (fastest)
2. If not found in memory, check disk cache
3. If not found in disk cache, generate a new sticker
4. Store newly generated sticker in both memory and disk caches when available
5. If memory cache is disabled or full, rely solely on disk cache
6. If both caches are unavailable, fall back to direct generation with no caching

This ensures optimal performance and resilience under various conditions.

### Testing

To test the sticker generation caching implementation:

1. Install required dependencies:
   ```bash
   pip install Pillow
   ```

2. Run the test script:
   ```bash
   # From the sticker-generation-service directory
   python3 src/test_cache/test_sticker_cache.py
   ```

3. The test will:
   - Generate mock stickers for several test prompts
   - Save the generated stickers as PNG files for inspection
   - Test both memory and disk cache functionality
   - Verify fallback behavior
   - Display performance statistics

### Performance Impact

Tests demonstrate dramatic performance improvements:
- First-time generation: ~1-3 seconds (using mock generator)
- Memory cache hit: ~0.05ms (>99.99% faster)
- Disk cache hit: ~1-4ms (>99.9% faster)

With an actual diffusion model, the performance gains would be even more significant, as real image generation can take 5-10+ seconds.

## Monitoring & Management

Both caching systems include:
- Cache statistics endpoints for monitoring
- Automatic cache cleanup based on TTL and size limits
- Configurable limits for resource management

For the sticker service, a `/cache-status` endpoint is available to monitor cache performance and utilization.

## Best Practices

1. **Configure appropriate TTL values** based on how frequently data changes
2. **Monitor cache hit/miss ratios** to optimize performance
3. **Set reasonable size limits** to prevent excessive resource consumption
4. **Consider sharding** for very large deployments (Redis only)
5. **Adjust cache sizes** based on usage patterns and available resources
6. **Implement automated testing** to verify cache behavior during deployments