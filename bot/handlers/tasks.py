from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime
import pytz
from ..config import TIMEZONE

router = Router()

@router.message(Command("tasks"))
async def show_tasks(message: Message, api, token):
    try:
        tasks = api.get_tasks(token)
        if not tasks:
            await message.answer("No tasks found.")
            return

        tz = pytz.timezone(TIMEZONE)
        response = "Your tasks:\n"
        for task in tasks:
            created_at_utc = datetime.fromisoformat(task['created_at'].rstrip('Z'))
            created_at_local = created_at_utc.astimezone(tz).strftime('%Y-%m-%d %H:%M')
            category = task.get('category', {}).get('name', 'No category')
            response += f"- {task['title']} (Category: {category}, Created: {created_at_local})\n"
        await message.answer(response)
    except ValueError:
        await message.answer("Error fetching tasks.")