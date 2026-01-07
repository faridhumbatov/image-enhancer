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
        client = replicate.Client(api_token=api_token)
        
        # Versiya ID-si yerinə birbaşa model adından istifadə edirik
        # Bu üsul həmişə ən son işlək versiyanı seçir
        output = client.run(
            "xinntao/real-esrgan",
            input={
                "image": request.image_url,
                "upscale": 2,
                "face_enhance": True
            }
        )
        return {"enhanced_image_url": output}
    except Exception as e:
        print(f"Replicate Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
