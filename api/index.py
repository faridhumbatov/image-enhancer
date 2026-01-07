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

# Sizin API Key
API_KEY = "sk_4kGgyGCPXHOQs8MK8jPaZCAwG2zFrc7A"

@app.get("/")
def home():
    return {"status": "Premium Generator (URL Auth) Active"}

@app.post("/api/generate")
def generate_image(request: GenerateRequest):
    try:
        seed = random.randint(1, 1000000)
        
        # 1. Prompt-u kodlaşdırırıq (boşluqlar və simvollar üçün)
        clean_prompt = urllib.parse.quote(request.prompt)

        # 2. DÜZƏLİŞ: API Key-i birbaşa URL-ə 'token' parametri kimi əlavə edirik
        # Bu üsul Pollinations-da daha etibarlıdır
        api_url = (
            f"https://image.pollinations.ai/prompt/{clean_prompt}"
            f"?model=flux"
            f"&width=1024"
            f"&height=1024"
            f"&seed={seed}"
            f"&nologo=true"
            f"&token={API_KEY}"  # <--- ƏSAS DƏYİŞİKLİK BURADADIR
        )
        
        print(f"Sorğu URL: {api_url}") # Logda yoxlamaq üçün (Real layihədə gizlətmək lazımdır)

        # 3. Brauzer kimi görünmək üçün sadə başlıq
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # 4. Sorğunu göndəririk
        response = requests.get(api_url, headers=headers, timeout=60)
        
        if response.status_code != 200:
            print(f"Server Xətası: {response.status_code}")
            # Əgər şəkil gəlmirsə, xəta mətnini oxuyaq
            raise HTTPException(status_code=500, detail=f"Xəta: {response.text[:100]}")

        return Response(content=response.content, media_type="image/jpeg")

    except Exception as e:
        print(f"Kritik Xəta: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
