from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import replicate
import os

app = FastAPI()

# Frontend-dən gələn sorğulara icazə veririk
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend-dən bu formatda məlumat gözləyirik: {"image_url": "https://..."}
class EnhanceRequest(BaseModel):
    image_url: str

@app.get("/")
def home():
    return {"status": "Backend is Ready"}

@app.post("/api/enhance")
def enhance_image(request: EnhanceRequest):
    api_token = os.environ.get("REPLICATE_API_TOKEN")
    if not api_token:
        raise HTTPException(status_code=500, detail="API Token is missing in Vercel")

    try:
        # CodeFormer Modeli (Stabil Versiya)
        output = replicate.run(
            "sczhou/codeformer:7de2ea26c616d5bf2245ad0d5e24f0ff9a6204578a5c876cf5ef964a3b76756c",
            input={
                "image": request.image_url,
                "upscale": 2,
                "face_upsample": True,
                "background_enhance": True
            }
        )
        return {"enhanced_image_url": output}

    except Exception as e:
        print(f"Server Xətası: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
