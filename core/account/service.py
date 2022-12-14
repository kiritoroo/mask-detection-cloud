from fastapi import HTTPException, status

from .schema import AccountSchemaCreate
from .constants import TokenType
from .interface.repository_interface import AccountRepositoryInterface
from .interface.password_service_interface import PasswordServiceInterface
from .interface.token_service_interface import TokenServiceInterface
from .interface.service_interface import AccountServiceInterface

class AccountService(AccountServiceInterface):
    def __init__(self, 
        repository: AccountRepositoryInterface,
        password_service: PasswordServiceInterface,
        token_service: TokenServiceInterface
    ) -> None:
        self._repository = repository
        self._password_service = password_service
        self._token_service = token_service
        
    async def login(self, username: str, password: str):
        user = await self._authenticate(username=username, password=password)
        if user is None:
            return {'message': "Username or password not found"}
        
        access_token = await self._create_token_data(
            username=user['username'],
            email=user['email'],
            token_type=TokenType.ACCESS_TOKEN,
            exp_time=int(5))

        refresh_toekn = await self._create_token_data(
            username=user['username'],
            email=user['email'],
            token_type=TokenType.REFRESH_TOKEN,
            exp_time=int(10))
        return {
            'access_token': access_token,
            'refresh_token': refresh_toekn
        }
        
    async def register(self, user_data: AccountSchemaCreate):
        if await self._repository.get_user(username=user_data.username):
            # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with this username exists')
            return {"message": "User with this username exists"}
        
        hashed_password = await self._password_service.hashed_password(plain_password=user_data.password)
        user_data.password = hashed_password
        return await self._repository.save_user(user=user_data)
        
    async def get_user(self, username: str):
        return await self._repository.get_user(username=username)
        
    async def _authenticate(self, username: str, password: str):
        if not (user := await self._repository.get_user(username=username)):
            # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect username or password')
            return None
        
        user = await self._repository.get_user(username=username)
        if await self._password_service.verify_passwords(plain_password=password, hashed_password=user['password']) == (False, None):
            # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect username or password')
            return None
        
        return user
    
    async def detail_user(self, user_id: str):
        return await self._repository.detail_user(user_id=user_id)

    async def _create_token_data(self, username: str, email:str, token_type: TokenType, exp_time: int):
        return await self._token_service.encode_token(
            username=username,
            email=email,
            token_type=token_type,
            secret_key='CLOUD',
            algorithm='HS256',
            exp_time=int(exp_time)
        )