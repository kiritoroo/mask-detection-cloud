import uvicorn
from fastapi import File, UploadFile, Request, FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from core.account.controller import account_router
from core.constant import members

PORT = os.environ.get('APP_PORT') or 8080

app = FastAPI(
    title='Mask Detection Cloud', 
    version='1.1.2'
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(account_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.route(path='/', methods=['GET', 'POST'])
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