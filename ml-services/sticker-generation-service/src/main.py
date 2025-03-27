'''
Main Module
API for generating stickers from text prompts
'''
import os
from io import BytesIO
import base64
from PIL import Image
from pydantic import BaseModel
from rembg import remove
from .utils import create_sticker
from .diffusion_model import generate_image_from_prompt
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse

class PromptRequest(BaseModel):
    '''prompt request model '''
    prompt: str

app = FastAPI()

# Initialize cache (must be done before using @cache)
@app.on_event("startup")
async def startup():
    '''Startup event'''
    FastAPICache.init(InMemoryBackend(), prefix="sticker-cache")

@app.get("/")
def get_service_status():
    '''Service Status'''
    return{"status":"success", "message": "service is running."}


@app.post("/generate-sticker")
async def generate_sticker(request: PromptRequest):
    '''Generate Sticker Route'''
    try:
        # Your existing pipeline
        image = generate_image_from_prompt(request.prompt)
        sticker = create_sticker(image)
        sticker = Image.fromarray(sticker)
        sticker = remove(sticker)
        # Convert to bytes
        img_buffer = BytesIO()
        sticker.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        img_b64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
        return JSONResponse({
            "image": img_b64,
            "format": "png"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {type(e).__name__} {e}") from e

@app.get("/generate-sticker-web")
@cache(expire=300)  # Cache for 5 minutes
async def sticker_web(request: PromptRequest):
    """
    Generate a sticker and return an HTML response.
    """
    # Generate image (will be cached based on prompt value)
    image = generate_image_from_prompt(request.prompt)
    sticker = create_sticker(image)
    sticker = Image.fromarray(sticker)
    sticker = remove(sticker)
    
    # Convert to base64
    img_buffer = BytesIO()
    sticker.save(img_buffer, format="PNG")
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    
    return HTMLResponse(
        f"""
        <html>
            <body>
                <img src="data:image/png;base64,{img_base64}">
                <form>
                    <input name="prompt" value="{request.prompt}">
                    <button>Generate</button>
                </form>
            </body>
        </html>
        """
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





