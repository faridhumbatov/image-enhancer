from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import replicate
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Artıq şəkil URL-i yox, "prompt" (təsvir) qəbul edirik
class GenerateRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "Image Generator Ready"}

@app.post("/api/generate")
def generate_image(request: GenerateRequest):
    api_token = os.environ.get("REPLICATE_API_TOKEN")
    if not api_token:
        raise HTTPException(status_code=500, detail="API Token missing")

    try:
        # FLUX.1 [schnell] Modeli - Çox sürətli və keyfiyyətlidir
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": request.prompt,
                "go_fast": True,   # Sürətli rejim
                "megapixels": "1", # Şəkil ölçüsü
                "num_outputs": 1,
                "aspect_ratio": "16:9", # Ekran formatı (1:1, 16:9, 9:16 ola bilər)
                "output_format": "jpg"
            }
        )
        
        # Flux modeli nəticəni siyahı (list) kimi qaytarır, biz birincini götürürük
        image_url = output[0]
        
        return {"generated_image_url": image_url}

    except Exception as e:
        print(f"Xəta: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
