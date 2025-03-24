"""Module for API functions and Input Model"""

from fastapi import HTTPException
from pydantic import BaseModel
from src.predictor import Predictor
from src.cache import RedisCache
from src.cached_predictor import CachedPredictor

# Created base predictor - Instance of Bert Model.
base_predictor = Predictor()
# Created cache
redis_cache = RedisCache()

# Create cached predictor with Redis and in-memory fallback
nextWord = CachedPredictor(base_predictor, redis_cache)

# Pydantic Model FOr Data Validation.
class NextWordInput(BaseModel):
    '''Pydantic Class'''
    text: str
    predictions: int
    tokens: int

def get_service_status():
    '''Service Status'''
    return {"status": "success", "message": "Service is running"}

def get_next_words(data: NextWordInput):
    '''Next Word Prediction Func'''
    try:
        result = nextWord.gen_m_words_n_predictions(data.tokens, data.predictions, data.text)
        return {"status": "success", "words": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {type(e).__name__} {e}") from e
