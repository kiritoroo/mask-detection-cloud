from fastapi import APIRouter, Request, Response
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

ai_router = APIRouter()

@ai_router.get("/ai")
def ai(request: Request):
    return templates.TemplateResponse(
        "pages/ai.html",
        {
            "request": request
        }
    )