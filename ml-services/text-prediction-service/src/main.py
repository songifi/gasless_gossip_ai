"""Main Module with Redis caching support"""

import os
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .api import get_service_status, get_next_words, NextWordInput
from .cache import RedisCache

# Load environment variables
load_dotenv()

# Create the FastAPI app
app = FastAPI()

# Configure CORS (allow all origins; adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read endpoint, host, and port from environment variables
endpoint = os.getenv("ENDPOINT", "/")
host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", "8000"))

# Add middleware to check Redis connectivity on startup
@app.on_event("startup")
async def startup_event():
    """Verify Redis connectivity on startup"""
    cache = RedisCache()
    if cache.ping():
        print("✅ Successfully connected to Redis server")
    else:
        print("⚠️ Could not connect to Redis server. Running without caching.")

# Define GET endpoint for service status
@app.get("/")
def read_root():
    '''Service Status'''
    return get_service_status()

# Define POST endpoint for next word prediction
@app.post("/predict")
async def post_next_word(data: NextWordInput):
    '''Next Word Route'''
    return get_next_words(data)

# Add a cache status endpoint for monitoring
@app.get("/cache-status")
async def cache_status():
    '''Cache Status Endpoint'''
    cache = RedisCache()
    status = "available" if cache.ping() else "unavailable"
    return {"cache_status": status}

# Run the app using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=host, port=port)