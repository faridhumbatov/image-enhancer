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
    return {"status": "Stealth Proxy Active"}

@app.post("/api/generate")
def generate_image(request: GenerateRequest):
    try:
        clean_prompt = urllib.parse.quote(request.prompt)
        seed = random.randint(1, 1000000)
        
        # URL
        image_url = f"https://pollinations.ai/p/{clean_prompt}?width=1280&height=720&seed={seed}&model=flux&nologo=true"
        
        # BU HİSSƏ VACİBDİR: Özümüzü real brauzer kimi göstəririk
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8"
        }

        # Şəkli yükləyirik (Timeout artırırıq ki, gözləsin)
        response = requests.get(image_url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"Xəta kodu: {response.status_code}")
            raise HTTPException(status_code=500, detail="Pollinations blokladı")

        # Gələn datanın həqiqətən şəkil olub-olmadığını yoxlayırıq
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type:
            print(f"Gələn data şəkil deyil: {response.text[:100]}")
            raise HTTPException(status_code=500, detail="Server şəkil göndərmədi")

        return Response(content=response.content, media_type="image/jpeg")

    except Exception as e:
        print(f"Kritik Xəta: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
