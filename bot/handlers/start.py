from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Welcome to ToDo Bot! Use /tasks to view tasks, /add to add a new one.")