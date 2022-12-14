import uvicorn
from fastapi import File, UploadFile, Request, FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from core.account.controller import account_router
from core.chat.controller import websocket_router
from core.constant import members, mentor

PORT = os.environ.get('APP_PORT') or 8080

app = FastAPI(
    title='Mask Detection Cloud', 
    version='1.1.2'
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(account_router)
app.include_router(websocket_router)

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
        {
            "request": request, 
            "members": members,
            "mentor": mentor
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host='127.0.0.1',
        port=int(PORT),
        log_level="info",
        reload=True)