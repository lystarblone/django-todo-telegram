import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs, StartMode
from aiogram.filters import Command
from config import BOT_TOKEN, API_BASE_URL
from api_client import APIClientAsync
from middlewares import AuthMiddleware
from handlers.start import start
from handlers.tasks import show_tasks
from dialogs.add_task_dialog import add_task_dialog
from states import AddTaskDialog

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    api_client = APIClientAsync(API_BASE_URL)
    dp.message.middleware(AuthMiddleware(api_client))

    dp.message.register(start, Command("start"))
    dp.message.register(show_tasks, Command("tasks"))

    dp.include_router(add_task_dialog)

    @dp.message(Command("add"))
    async def start_add_dialog(message: types.Message, dialog_manager):
        await dialog_manager.start(AddTaskDialog.title, mode=StartMode.RESET_STACK)

    setup_dialogs(dp)

    logging.info("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())