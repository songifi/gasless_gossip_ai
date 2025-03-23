"""Main Module"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .api import get_service_status, get_next_words, NextWordInput

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

# Run the app using uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=host, port=port)