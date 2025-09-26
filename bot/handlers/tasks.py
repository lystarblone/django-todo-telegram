from aiogram import types
from datetime import datetime
import pytz
from bot.config import TIMEZONE

async def show_tasks(message: types.Message, api, token):
    try:
        tasks = await api.get_tasks(token)
        if not tasks:
            await message.answer("Нет задач.")
            return

        tz = pytz.timezone(TIMEZONE)
        response = "Ваши задачи:\n"
        for task in tasks:
            created_at_utc = datetime.fromisoformat(task["created_at"].rstrip("Z"))
            created_at_local = created_at_utc.astimezone(tz).strftime("%Y-%m-%d %H:%M")
            category = task.get("category", {}).get("name", "Без категории")
            response += f"- {task['title']} (Категория: {category}, Создано: {created_at_local})\n"
        await message.answer(response)
    except ValueError as e:
        await message.answer(f"Ошибка при получении задач: {e}")