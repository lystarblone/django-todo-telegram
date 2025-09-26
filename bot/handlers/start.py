from aiogram import types

async def start(message: types.Message):
    await message.answer("Welcome to ToDo Bot! Use /tasks to view tasks, /add to add a new one.")