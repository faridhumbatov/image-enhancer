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

@app.get("/")
def home():
    return {"status": "Proxy Generator Ready"}

@app.post("/api/generate")
def generate_image(request: GenerateRequest):
    try:
        # 1. URL-i hazırlayırıq
        clean_prompt = urllib.parse.quote(request.prompt)
        seed = random.randint(1, 1000000)
        
        image_url = f"https://pollinations.ai/p/{clean_prompt}?width=1280&height=720&seed={seed}&model=flux&nologo=true"
        
        # 2. Şəkli Server tərəfində yükləyirik (Brauzer qarışmır)
        # Bu hissə 'requests' kitabxanası ilə işləyir
        response = requests.get(image_url)
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Pollinations cavab vermədi")

        # 3. Şəkli birbaşa fayl kimi (bytes) istifadəçiyə göndəririk
        return Response(content=response.content, media_type="image/jpeg")

    except Exception as e:
        print(f"Xəta: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
