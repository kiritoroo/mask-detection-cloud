import uvicorn
from fastapi import File, UploadFile, Request, FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from service.constant import *
import os

PORT = os.environ.get('APP_POST') or 8080

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def main(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "members": members})

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host='0.0.0.0',
        port=int(PORT),
        log_level="info",
        reload=True)