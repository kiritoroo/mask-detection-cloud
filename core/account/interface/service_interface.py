from abc import ABC, abstractmethod
from ..schema import AccountSchemaCreate

class AccountServiceInterface(ABC):
    @abstractmethod
    async def login(self, username: str, password: str) -> dict:
        pass
    
    @abstractmethod
    async def register(self, user_data: AccountSchemaCreate) -> dict:
        pass
    
    @abstractmethod
    async def detail_user(self, user_id: str) -> dict:
        pass
    
    @abstractmethod
    async def get_user(self, username: str) -> dict:
        pass