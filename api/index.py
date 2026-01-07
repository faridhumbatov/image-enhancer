from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import random
import urllib.parse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str

# Sizin təqdim etdiyiniz Pollinations API Key
API_KEY = "sk_4kGgyGCPXHOQs8MK8jPaZCAwG2zFrc7A"

@app.get("/")
def home():
    return {"status": "Premium Generator Active"}

@app.post("/api/generate")
def generate_image(request: GenerateRequest):
    try:
        # 1. URL Hazırlığı
        seed = random.randint(1, 1000000)
        # width=1024, height=1024 (Premium-da kvadrat şəkil daha keyfiyyətli olur)
        api_url = f"https://image.pollinations.ai/prompt/{request.prompt}?model=flux&width=1024&height=1024&seed={seed}&nologo=true"
        
        print(f"Sorğu göndərilir: {api_url}")

        # 2. Header-ə API Key əlavə edirik (Authorization: Bearer ...)
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "User-Agent": "MyPremiumApp/1.0"
        }

        # 3. Sorğunu göndəririk
        response = requests.get(api_url, headers=headers, timeout=60)
        
        # 4. Yoxlayırıq
        if response.status_code != 200:
            print(f"Xəta kodu: {response.status_code} - {response.text}")
            raise HTTPException(status_code=500, detail=f"API Xətası: {response.status_code}")

        # 5. Şəkli (binary data) istifadəçiyə qaytarırıq
        return Response(content=response.content, media_type="image/jpeg")

    except Exception as e:
        print(f"Kritik Xəta: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
