from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import replicate
import os

app = FastAPI()

# Frontend-in API-a qoşula bilməsi üçün icazələr
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
    return {"status": "Server is running perfectly!"}

@app.post("/api/enhance")
def enhance_image(request: EnhanceRequest):
    # 1. Tokeni yoxlayırıq
    api_token = os.environ.get("REPLICATE_API_TOKEN")
    if not api_token:
        print("Xəta: Token tapılmadı")
        raise HTTPException(status_code=500, detail="REPLICATE_API_TOKEN is missing")

    try:
        # 2. Modeli işə salırıq
        # "nightmareai/real-esrgan" modeli daha stabildir.
        # Versiya ID-si: 42fed1c4... (Ən son stabil versiya)
        output = replicate.run(
            "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73ab415c722d3790c507",
            input={
                "image": request.image_url,
                "scale": 2,            # Neçə dəfə böyütmək (maksimum 10 ola bilər)
                "face_enhance": True   # Üzləri düzəltmək
            }
        )
        
        # Logda nəticəni görmək üçün
        print(f"Success! Output: {output}")
        return {"enhanced_image_url": output}

    except replicate.exceptions.ReplicateError as e:
        # Replicate-dən gələn xüsusi xətalar (məsələn: Balans bitibsə)
        print(f"Replicate Xətası: {str(e)}")
        raise HTTPException(status_code=402, detail=f"AI Xətası: {str(e)}")
        
    except Exception as e:
        # Digər ümumi xətalar
        print(f"Ümumi Xəta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server Xətası: {str(e)}")
