from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import replicate
import os

app = FastAPI()

class EnhanceRequest(BaseModel):
    image_url: str

@app.get("/")
def home():
    return {"message": "Image Enhancer API is running!"}

@app.post("/api/enhance")
def enhance_image(request: EnhanceRequest):
    # API Tokeni yoxlayırıq
    if not os.environ.get("REPLICATE_API_TOKEN"):
        raise HTTPException(status_code=500, detail="API Token təyin edilməyib!")

    try:
        # Replicate-də Real-ESRGAN modelini işə salırıq
        output = replicate.run(
            "xinntao/realsrgan:1b97abc4b3a1a37c37c2a71d798e1e7047f6368d9c669176378e9f2b801a6b0c",
            input={
                "img": request.image_url,
                "scale": 2,
                "face_enhance": True
            }
        )
        return {"enhanced_image_url": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))