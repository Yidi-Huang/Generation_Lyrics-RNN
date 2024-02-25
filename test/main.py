import os
from fastapi import FastAPI, Request, Form
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# 获取模板文件夹的绝对路径
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

templates = Jinja2Templates(directory=templates_dir)


class InputForm(BaseModel):
    user_input: str


hp_dico = dict()


@app.post("/process_input")
async def process_input(request: Request, user_input: str = Form(...)):
    hp_dico["title"] = user_input
    return templates.TemplateResponse(
        "index.html", {"request": request, "pt": f"Title : {user_input}"}
    )


@app.post("/process_input2")
async def process_input(request: Request, user_input2: str = Form(...)):
    hp_dico["prompt_phrase"] = user_input2 + "<c>"
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "pp": f"First phrase of your song : {user_input2}"},
    )


@app.post("/select_model")
async def select_model(request: Request, model: str = Form(...)):
    hp_dico["model"] = model
    filename = model + ".txt"
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    if filename in os.listdir(models_dir):
        return templates.TemplateResponse(
            "index.html", {"request": request, "result": f"Model {model} found."}
        )
    else:
        return templates.TemplateResponse(
            "index.html", {"request": request, "result": f"Model {model} not found."}
        )


@app.post("/set_len")
async def set_length(request: Request, len: str = Form(...)):
    length = int(len)  # 将字符串转换为整数
    if 0 < length < 500:
        hp_dico["length"] = length
        message = f"Length {length} is OK."
    else:
        message = "Length not allowed."
    return templates.TemplateResponse(
        "index.html", {"request": request, "message": message, "len": length}
    )


@app.get("/hp_dico")
async def get_hp_dico():
    return hp_dico


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)
