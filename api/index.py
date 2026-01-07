from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import urllib.parse

app = FastAPI()

# Bütün saytlardan gələn sorğulara icazə veririk (CORS)
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
    return {"status": "Unlimited Free Generator Running"}

@app.post("/api/generate")
def generate_image(request: GenerateRequest):
    try:
        # 1. Prompt-u URL üçün təmizləyirik (boşluqları %20 edirik)
        clean_prompt = urllib.parse.quote(request.prompt)
        
        # 2. Təsadüfi bir "seed" yaradırıq ki, eyni söz yazanda hər dəfə fərqli şəkil çıxsın
        seed = random.randint(1, 1000000)
        
        # 3. Pollinations API linkini formalaşdırırıq (Flux modeli ilə)
        # Bu linkə daxil olan kimi şəkil yaranır
        image_url = f"https://pollinations.ai/p/{clean_prompt}?width=1280&height=720&seed={seed}&model=flux&nologo=true"
        
        return {"generated_image_url": image_url}

    except Exception as e:
        print(f"Xəta: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
