from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from .api_client import APIClient
from .config import API_BASE_URL

class AuthMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.api = APIClient(API_BASE_URL)

    async def __call__(self, handler, event: types.Message, data: dict):
        if isinstance(event, types.Message):
            user_id = event.from_user.id
            try:
                auth_data = self.api.register_or_login(user_id)
                data["token"] = auth_data["token"]
                data["user_id"] = auth_data["user_id"]
            except ValueError:
                await event.answer("Ошибка аутентификации с бэкендом.")
                return
            data["api"] = self.api

        return await handler(event, data)
