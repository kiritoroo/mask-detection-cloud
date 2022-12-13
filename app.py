import uvicorn
from fastapi import File, UploadFile, Request, FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def main(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request})

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host='127.0.0.1',
        port=8080,
        log_level="info",
        reload=True)