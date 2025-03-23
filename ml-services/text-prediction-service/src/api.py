"""Module for API functions and Input Model"""

from fastapi import HTTPException
from pydantic import BaseModel
from src.predictor import Predictor

# Instance of Bert Model.
nextWord = Predictor()

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
