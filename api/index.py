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
    return {"status": "Active"}

@app.post("/api/enhance")
def enhance_image(request: EnhanceRequest):
    api_token = os.environ.get("REPLICATE_API_TOKEN")
    if not api_token:
        raise HTTPException(status_code=500, detail="API Token missing")

    try:
        # GFPGAN modeli (Daha stabil və etibarlıdır)
        # Versiya: v1.4
        output = replicate.run(
            "tencentarc/gfpgan:92836085e347504f588f0bc2062f613d02086302568f70e1a9134070a2936338",
            input={
                "img": request.image_url, # Diqqət: Bu model 'image' yox, 'img' qəbul edir
                "scale": 2,
                "version": "v1.4"
            }
        )
        
        return {"enhanced_image_url": output}

    except replicate.exceptions.ReplicateError as e:
        # Əgər həqiqətən ödəniş/limit problemi varsa, burada bilinəcək
        print(f"Replicate Error: {e}")
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")
        
    except Exception as e:
        print(f"General Error: {e}")
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
