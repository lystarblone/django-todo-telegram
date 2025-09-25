import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

from .config import BOT_TOKEN
from .middlewares import AuthMiddleware
from .handlers.start import start
from .handlers.tasks import show_tasks

logging.basicConfig(level=logging.INFO)


class AddTaskStates(StatesGroup):
    title = State()
    description = State()
    due_date = State()
    category = State()


async def process_add_command(message: types.Message, state: FSMContext):
    await state.set_state(AddTaskStates.title)
    await message.answer("Enter task title:")


async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddTaskStates.description)
    await message.answer("Enter description (or type /skip):")


async def process_description(message: types.Message, state: FSMContext):
    if message.text == "/skip":
        await state.update_data(description="")
    else:
        await state.update_data(description=message.text)
    await state.set_state(AddTaskStates.due_date)
    await message.answer("Enter due date (YYYY-MM-DD HH:MM):")


async def process_due_date(message: types.Message, state: FSMContext):
    from datetime import datetime
    import pytz

    try:
        due_date = datetime.strptime(message.text, "%Y-%m-%d %H:%M")
        tz = pytz.timezone("America/Adak")
        due_date = tz.localize(due_date).astimezone(pytz.utc).isoformat()
        await state.update_data(due_date=due_date)
        await state.set_state(AddTaskStates.category)
        await message.answer("Enter category name:")
    except ValueError:
        await message.answer("Invalid date format. Use YYYY-MM-DD HH:MM")


async def process_category(message: types.Message, state: FSMContext, api, token):
    await state.update_data(category=message.text)
    data = await state.get_data()
    task_data = {
        "title": data["title"],
        "description": data.get("description", ""),
        "due_date": data["due_date"],
        "category": data["category"],
    }
    try:
        api.create_task(token, task_data)
        await message.answer("Task created successfully!")
    except ValueError as e:
        await message.answer(f"Error creating task: {str(e)}")
    await state.clear()


async def main():
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.message.middleware(AuthMiddleware())

    dp.message.register(start, Command("start"))
    dp.message.register(show_tasks, Command("tasks"))
    dp.message.register(process_add_command, Command("add"))
    dp.message.register(process_title, AddTaskStates.title)
    dp.message.register(process_description, AddTaskStates.description)
    dp.message.register(process_due_date, AddTaskStates.due_date)
    dp.message.register(process_category, AddTaskStates.category)

    logging.info("Бот запущен")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
