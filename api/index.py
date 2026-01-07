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

class EnhanceRequest(BaseModel):
    image_url: str

@app.get("/")
def home():
    return {"status": "CodeFormer Model Ready"}

@app.post("/api/enhance")
def enhance_image(request: EnhanceRequest):
    # 1. API Token yoxlanışı
    api_token = os.environ.get("REPLICATE_API_TOKEN")
    if not api_token:
        print("Error: Token not found")
        raise HTTPException(status_code=500, detail="API Token missing")

    try:
        # 2. CodeFormer Modelini işə salırıq
        # Bu model üzləri düzəltmək və keyfiyyəti artırmaqda ən yaxşısıdır.
        # Stabil Versiya Hash: 7de2ea26...
        output = replicate.run(
            "sczhou/codeformer:7de2ea26c616d5bf2245ad0d5e24f0ff9a6204578a5c876cf5ef964a3b76756c",
            input={
                "image": request.image_url,
                "upscale": 2,             # Şəkli 2 dəfə böyüt
                "face_upsample": True,    # Üzləri xüsusi bərpa et
                "background_enhance": True, # Arxa fonu da təmizlə
                "codeformer_fidelity": 0.7 # 0 = maksimum bərpa, 1 = orijinala sadiq qalmaq
            }
        )
        
        print(f"Success: {output}")
        return {"enhanced_image_url": output}

    except replicate.exceptions.ReplicateError as e:
        print(f"Replicate Error: {e}")
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")
        
    except Exception as e:
        print(f"General Error: {e}")
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
