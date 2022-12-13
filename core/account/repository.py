from fastapi import HTTPException
from bson import ObjectId
import datetime

from .interface.repository_interface import AccountRepositoryInterface
from .constants import account_response_exept
from .schema import AccountSchemaCreate

class AccountRepository(AccountRepositoryInterface):
    def __init__(self, user_collection) -> None:
        self._user_collection = user_collection
        
    async def detail_user(self, user_id: str):
        if not ObjectId.is_valid(user_id):
            raise HTTPException(**account_response_exept.get('not_found'))
        data = {
            'filter': {
                '_id': ObjectId(user_id)
            }
        }
        if not (user := await self._user_collection.find_one(**data)):
            raise HTTPException(**account_response_exept.get('not_found'))
        return user
    
    async def save_user(self, user: AccountSchemaCreate):
        data = dict(
            **user.dict(exclude_none=True),
            created_at=datetime.datetime.utcnow(),
            is_admin=False
        )
        result = await self._user_collection.insert_one(document=data)
        return await self.detail_user(user_id=result.inserted_id)
    
    async def get_user(self, username: str):
        data = {
            'filter': {
                'username': username
            }
        }
        return await self._user_collection.find_one(**data)