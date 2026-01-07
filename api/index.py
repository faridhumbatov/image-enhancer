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
    return {"status": "Server is running"}

@app.post("/api/enhance")
def enhance_image(request: EnhanceRequest):
    # Tokeni birbaşa yoxlayırıq
    api_token = os.environ.get("REPLICATE_API_TOKEN")
    
    if not api_token:
        raise HTTPException(status_code=500, detail="REPLICATE_API_TOKEN is missing in Vercel settings")

    try:
        # Replicate müştərisini tokenlə başladırıq
        client = replicate.Client(api_token=api_token)
        
        output = client.run(
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
