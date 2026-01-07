from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "Free Unlimited Generator Active"}

@app.post("/api/generate")
def generate_image(request: GenerateRequest):
    try:
        # Pollinations AI heç bir token tələb etmir.
        # Sadəcə URL-ə prompt-u göndəririk.
        seed = random.randint(1, 999999) # Hər dəfə fərqli nəticə üçün
        prompt_encoded = request.prompt.replace(" ", "%20")
        
        # Flux modelini seçirik
        image_url = f"https://pollinations.ai/p/{prompt_encoded}?width=1024&height=768&seed={seed}&model=flux"
        
        return {"generated_image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
