from aiogram import types
from datetime import datetime
import pytz
from config import TIMEZONE
import logging

logger = logging.getLogger(__name__)

async def show_tasks(message: types.Message, api, token):
    try:
        tasks = await api.get_tasks(token)
        logger.info(f"Tasks fetched: {tasks}")
        if not tasks:
            await message.answer("Нет задач.")
            return

        tz = pytz.timezone(TIMEZONE)
        response = "Ваши задачи:\n"
        for task in tasks:
            created_at_utc = datetime.fromisoformat(task["created_at"].rstrip("Z"))
            created_at_local = created_at_utc.astimezone(tz).strftime("%Y-%m-%d %H:%M")
            categories = task.get("categories", [])
            category_names = ", ".join(cat["name"] for cat in categories) if categories else "Без категории"
            response += f"- {task['title']} (Категории: {category_names}, Создано: {created_at_local})\n"
        await message.answer(response)
    except ValueError as e:
        logger.error(f"Error fetching tasks: {e}")
        await message.answer(f"Ошибка при получении задач: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in show_tasks: {e}")
        await message.answer(f"Неизвестная ошибка: {e}")