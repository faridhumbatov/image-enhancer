from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import replicate
import os

app = FastAPI()

# CORS icazələri (Front-end-in API-ya daxil olması üçün mütləqdir)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EnhanceRequest(BaseModel):
    image_url: str

@app.post("/api/enhance")
def enhance_image(request: EnhanceRequest):
    # 1. API Token yoxlanışı
    api_token = os.environ.get("REPLICATE_API_TOKEN")
    if not api_token:
        return {"error": "REPLICATE_API_TOKEN tapılmadı. Vercel Settings-də quraşdırın."}

    try:
        # 2. Replicate modelini çağırırıq
        # Diqqət: Realsrgan bəzən gecikə bilər, model versiyasının doğruluğuna baxın
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
        # Xətanı terminalda görmək üçün
        print(f"Xəta baş verdi: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
