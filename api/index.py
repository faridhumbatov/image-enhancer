from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import random
import urllib.parse
import time

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
    return {"status": "Stable Generator Active"}

@app.post("/api/generate")
def generate_image(request: GenerateRequest):
    try:
        # 1. Hər dəfə fərqli bir "Seed" yaradırıq (1 milyard ehtimal)
        # Bu, serveri aldadır ki, "bu köhnə şəkil deyil, təzəsini çək"
        seed = random.randint(1, 999999999)
        
        # 2. Prompt-u təmizləyirik
        clean_prompt = urllib.parse.quote(request.prompt)

        # 3. URL-ə 'cache-buster' parametrləri əlavə edirik
        # API Key-i yığışdırdıq, çünki o limitə salır. Anonim daha yaxşıdır.
        api_url = (
            f"https://image.pollinations.ai/prompt/{clean_prompt}"
            f"?model=flux"
            f"&width=1280"
            f"&height=720"
            f"&seed={seed}"
            f"&nologo=true"
            f"&enhance=false" # Sürət üçün əlavə effektləri söndürürük
        )
        
        print(f"URL: {api_url}")

        # 4. Brauzer başlıqlarını (Header) hər dəfə biraz dəyişirik
        # Bu, bizi bloklanmaqdan qoruyur
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) Firefox/100.0"
        ]
        headers = {
            "User-Agent": random.choice(user_agents),
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        }

        # 5. Sorğunu göndəririk (Timeout 30 saniyə qoyuruq ki, ilişib qalmasın)
        response = requests.get(api_url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            # Əgər Flux alınmasa, avtomatik Turbo modelinə keçir (Backup)
            backup_url = api_url.replace("model=flux", "model=turbo")
            print("Flux alınmadı, Turbo modelinə keçilir...")
            response = requests.get(backup_url, headers=headers, timeout=30)

        # Əgər yenə alınmasa
        if response.status_code != 200:
             raise HTTPException(status_code=500, detail="Server çox məşğuldur, 5 saniyə sonra yoxlayın.")

        return Response(content=response.content, media_type="image/jpeg")

    except Exception as e:
        print(f"Xəta: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
