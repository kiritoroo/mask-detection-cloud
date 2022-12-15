from fastapi import APIRouter, Request, Response, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from .service import image_process

templates = Jinja2Templates(directory="templates")
ai_router = APIRouter(tags=["AI Service"])

@ai_router.get("/ai")
def ai(request: Request):
    return templates.TemplateResponse(
        "pages/ai.html",
        {
            "request": request
        }
    )
    
@ai_router.post('/api/image')
def image(image_data: str = Form()) -> any:
    result = image_process(image_base64_encode=image_data)
    response = { 
        "message": "None Image"
    }
    if result != None:
        response = { 
            "message": result.decode("utf-8") 
        }
    return JSONResponse(content=response)