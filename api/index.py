from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import replicate
import os

app = FastAPI()

# 1. CORS problemini həll etmək üçün ən geniş icazələr
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Bütün saytlara icazə ver
    allow_credentials=True,
    allow_methods=["*"],  # Bütün metodlara (POST, GET, OPTIONS) icazə ver
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"status": "Flux Generator Ready"}

# OPTIONS sorğusunu əllə idarə edirik (CORS xətasını qabaqlamaq üçün)
@app.options("/api/generate")
async def options_generate():
    return JSONResponse(content="OK", headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "*"
    })

@app.post("/api/generate")
def generate_image(request: GenerateRequest):
    api_token = os.environ.get("REPLICATE_API_TOKEN")
    if not api_token:
        print("Xəta: Token yoxdur")
        raise HTTPException(status_code=500, detail="API Token missing")

    print(f"Sorğu gəldi: {request.prompt}") # Loglara yazırıq

    try:
        # FLUX.1 Schnell modeli (Rəsmi)
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": request.prompt,
                "go_fast": True,
                "megapixels": "1",
                "num_outputs": 1,
                "aspect_ratio": "16:9",
                "output_format": "jpg"
            }
        )
        
        print(f"Raw Output: {output}") # Nəticəni logda görək

        # FLUX nəticəni list kimi qaytarır: ['https://...']
        # Biz onu sadə mətnə (str) çeviririk
        image_url = str(output[0])
        
        return {"generated_image_url": image_url}

    except replicate.exceptions.ReplicateError as e:
        print(f"Replicate Xətası: {e}")
        # Xətanı JSON kimi qaytarırıq ki, brauzer oxuya bilsin
        return JSONResponse(status_code=500, content={"detail": f"AI Error: {str(e)}"})
        
    except Exception as e:
        print(f"Ümumi Xəta: {e}")
        return JSONResponse(status_code=500, content={"detail": f"Server Error: {str(e)}"})
