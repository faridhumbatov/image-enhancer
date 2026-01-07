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
    return {"status": "Server running with Dynamic Versioning"}

@app.post("/api/enhance")
def enhance_image(request: EnhanceRequest):
    api_token = os.environ.get("REPLICATE_API_TOKEN")
    if not api_token:
        raise HTTPException(status_code=500, detail="API Token missing")

    try:
        # 1. Müştərini yaradırıq
        client = replicate.Client(api_token=api_token)

        # 2. Əllə kod yazmaq əvəzinə, modelin ən son versiyasını serverdən soruşuruq
        # "nightmareai/real-esrgan" bu iş üçün ən stabil modeldir
        model = client.models.get("nightmareai/real-esrgan")
        latest_version = model.versions.list()[0] # Ən son versiyanı götürür

        print(f"Using version: {latest_version.id}") # Logda hansı versiyanı tapdığını görəcəyik

        # 3. Həmin tapılan versiya ilə işə salırıq
        output = client.run(
            f"nightmareai/real-esrgan:{latest_version.id}",
            input={
                "image": request.image_url,
                "scale": 2,
                "face_enhance": True
            }
        )
        
        return {"enhanced_image_url": output}

    except replicate.exceptions.ReplicateError as e:
        print(f"Replicate Error: {e}")
        # Xəta mesajını olduğu kimi qaytarırıq ki, dəqiq bilək
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")
        
    except Exception as e:
        print(f"General Error: {e}")
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
