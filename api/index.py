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
    return {"message": "Server is active"}

@app.post("/api/enhance")
def enhance_image(request: EnhanceRequest):
    api_token = os.environ.get("REPLICATE_API_TOKEN")
    if not api_token:
        raise HTTPException(status_code=500, detail="API Token tapılmadı!")

    try:
        # Yeni versiyalarda 'image' parametri daha çox istifadə olunur
        # Və modeli birbaşa ID ilə çağırmaq daha təhlükəsizdir
        output = replicate.run(
            "xinntao/realsrgan:1b97abc4b3a1a37c37c2a71d798e1e7047f6368d9c669176378e9f2b801a6b0c",
            input={
                "image": request.image_url,  # 'img' yerinə 'image' yoxlayın
                "upscale": 2,               # 'scale' yerinə 'upscale' yoxlayın
                "face_enhance": True
            }
        )
        return {"enhanced_image_url": output}
    except Exception as e:
        # Replicate-dən gələn mesajı logda görmək üçün
        print(f"Replicate Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
