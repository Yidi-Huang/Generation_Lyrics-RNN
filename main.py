import os
from fastapi import FastAPI, Request, Form
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from tensorflow.keras.models import load_model 
import sys
sys.path.append("script")
from script.generate import calculate_mapping_length,lyrics_generator
import re
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Obtenir le chemin absolu du dossier de modèles
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

templates = Jinja2Templates(directory=templates_dir)

# Configuration du service de fichiers statiques
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/images", StaticFiles(directory="images"), name="images")

@app.get("/", response_class=JSONResponse)
async def read_index(request: Request):
    # Rendre le modèle index.html et renvoyer la page HTML
    return templates.TemplateResponse("index.html", {"request": request})
    
@app.get("/projet_detail.html/")
async def get_projet_detail(request: Request):
    return templates.TemplateResponse("projet_detail.html", {"request": request})



@app.post("/generate_lyrics/", response_class=JSONResponse)
async def generate_lyrics(request: Request, artist: str = Form(...), title: str = Form(...), starter: str = Form(...), ch: int = Form(...)):
    try:
        model_path = os.path.join("model", f"{artist}.h5")
        if os.path.exists(model_path):
            model = load_model(f'model/{artist}.h5')
            print('Success: Model found.')
        else:
            raise FileNotFoundError(f"Model for artist {artist} not found")
        
        max_title_length = 20
        mapping, reverse_mapping = calculate_mapping_length(artist)
        l_symb = len(mapping)
        
        generated_text = lyrics_generator(model, mapping, reverse_mapping, starter+'<c>', title, ch, max_title_length, l_symb)
        generated_text = re.sub(r'<c>', '\n', generated_text)

        return templates.TemplateResponse("index.html", {"request": request, "generated_text": generated_text})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "generated_text": f"Error: {str(e)}"})


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
