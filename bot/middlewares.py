from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
from .api_client import APIClient
from .config import API_BASE_URL

class AuthMiddleware(BaseMiddleware):
    def __init__(self):
        self.api = APIClient(API_BASE_URL)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        if 'token' not in data:
            try:
                auth_data = self.api.register_or_login(user_id)
                data['token'] = auth_data['token']
                data['user_id'] = auth_data['user_id']
            except ValueError:
                await event.answer("Error authenticating with the backend. Please try again later.")
                return
        data['api'] = self.api
        return await handler(event, data)