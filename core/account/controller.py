from fastapi import APIRouter, Depends, Request, Response, status, Form
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer
from fastapi.templating import Jinja2Templates

from .constants import account_response_data
from .deps import get_account_service
from .service import AccountService
from .schema import AccountSchemaCreate

templates = Jinja2Templates(directory="templates")
token_auth_scheme = HTTPBearer()

"""Endpoints for Account"""
account_router = APIRouter(tags=['Account'])

@account_router.get("/register")
def login(request: Request):
    return templates.TemplateResponse(
        "pages/register.html",
        {"request": request, "message": "Register new account"}
    )

@account_router.post('/register', **account_response_data.get('register'))
async def register(
    request: Request,
    response: Response,
    email: str = Form(),
    username: str = Form(),
    password: str = Form(),
    phone: str = Form(),
    service_data=Depends(get_account_service)
):
    result = await AccountService(**service_data) \
        .register(user_data=AccountSchemaCreate(
            username=username,
            email=email,
            password=password,
            phone=phone))
        
    if "message" in result:
        return templates.TemplateResponse(
            "pages/register.html",
            {"request": request, "message": result['message']}
        )
        
    return templates.TemplateResponse(
        "pages/login.html",
        {
            "request": request, 
            "user": {"username": result['username']},
            "message": "Login now"
        }
    )

@account_router.get("/login")
def login(request: Request):
    return templates.TemplateResponse(
        "pages/login.html",
        {
            "request": request,
            "user": {"username": ""},
            "message": "Enter username and password"
        }
    )

@account_router.post('/login', **account_response_data.get('login'))
async def login(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    service_data=Depends(get_account_service),
):
    result = await AccountService(**service_data) \
        .login(username=form_data.username, password=form_data.password)
        
    if "access_token" in result:
        response = RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
        response.set_cookie(key='jwt', value=result['access_token'])
        return response
    
    return templates.TemplateResponse(
        "pages/login.html",
        {
            "request": request, 
            "user": {"username": ""},
            "message": result['message']
        }
    )

@account_router.get('/user/{user_id}', **account_response_data.get('detail'))
async def detail_user(
    user_id: str,
    token: str = Depends(token_auth_scheme),
    service_data=Depends(get_account_service)
):
    return await AccountService(**service_data) \
        .detail_user(user_id=user_id)

@account_router.get('/me/{username}', **account_response_data.get('detail'))
async def get_user(
    username: str,
    token: str = Depends(token_auth_scheme),
    service_data=Depends(get_account_service)
):
    return await AccountService(**service_data) \
        .get_user(username=username)