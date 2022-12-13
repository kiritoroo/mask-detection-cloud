from fastapi import Depends
from passlib.context import CryptContext

from .repository import AccountRepository
from .password_service import PasswordService
from .token_service import TokenService
from ..database import database

user_collection = database.get_collection('users')

async def get_user_collection():
    yield user_collection

async def get_account_service(
    _user_collection=Depends(get_user_collection)
):
    yield {
        'repository': AccountRepository(user_collection=_user_collection),
        'password_service': PasswordService(context=CryptContext(schemes=['bcrypt'], deprecated='auto')),
        'token_service': TokenService()
    }