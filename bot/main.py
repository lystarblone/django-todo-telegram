import asyncio
import logging
from mailbox import Message
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import DialogManager, setup_dialogs
from click import Command
from .dialogs.add_task import AddTaskSG
from .config import BOT_TOKEN
from .middlewares import AuthMiddleware
from .handlers.start import router as start_router
from .handlers.tasks import router as tasks_router
from .dialogs.add_task import add_task_dialog

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.message.middleware(AuthMiddleware())

    dp.include_router(start_router)
    dp.include_router(tasks_router)

    registry = setup_dialogs(dp)
    registry.register(add_task_dialog)

    @dp.message(Command("add"))
    async def start_add(message: Message, dialog_manager: DialogManager):
        await dialog_manager.start(AddTaskSG.title)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())