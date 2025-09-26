from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from api_client import APIClientAsync
import aiohttp
import logging

class AuthMiddleware(BaseMiddleware):
    def __init__(self, api_client: APIClientAsync):
        super().__init__()
        self.api = api_client

    async def __call__(self, handler, event: types.Message, data: dict):
        if isinstance(event, types.Message):
            user_id = event.from_user.id
            if "token" not in data:
                try:
                    auth_data = await self.api.register_or_login(user_id)
                    data["token"] = auth_data.get("token")
                    data["user_id"] = auth_data.get("user_id")
                except ValueError:
                    await event.answer("Ошибка аутентификации с бэкендом.")
                    return
            data["api"] = self.api
        return await handler(event, data)