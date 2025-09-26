from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram import types
from datetime import datetime
import pytz
from bot.config import TIMEZONE
from bot.states import AddTaskDialog

async def start_add(call: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(AddTaskDialog.title, data={})

async def on_title(event: types.Message, dialog: DialogManager, message: types.Message, manager: DialogManager):
    await manager.update({"title": message.text})
    await manager.switch_to(AddTaskDialog.description)

async def on_description(event: types.Message, dialog: DialogManager, message: types.Message, manager: DialogManager):
    if message.text == "/skip":
        await manager.update({"description": ""})
        await manager.switch_to(AddTaskDialog.due_date)
    else:
        await manager.update({"description": message.text})
        await manager.switch_to(AddTaskDialog.due_date)

async def on_due_date(event: types.Message, dialog: DialogManager, message: types.Message, manager: DialogManager):
    txt = message.text
    try:
        due_date = datetime.strptime(txt, "%Y-%m-%d %H:%M")
        tz = pytz.timezone(TIMEZONE)
        due_date = tz.localize(due_date).astimezone(pytz.utc).isoformat()
        await manager.update({"due_date": due_date})
        await manager.switch_to(AddTaskDialog.category)
    except ValueError:
        await message.answer("Неверный формат. Используй YYYY-MM-DD HH:MM")

async def get_categories(data: dict, manager: DialogManager) -> dict:
    api = manager.middleware_data.get("api")
    token = manager.middleware_data.get("token")
    try:
        categories = await api.get_categories(token)
        return {"categories": [(cat["name"], cat["id"]) for cat in categories]}
    except ValueError as e:
        await manager.event.answer(f"Ошибка получения категорий: {e}")
        return {"categories": []}

async def on_category_selected(event: types.CallbackQuery, select: Select, manager: DialogManager, item_id: str):
    data = await manager.get_data()
    api = manager.middleware_data.get("api")
    token = manager.middleware_data.get("token")

    task_data = {
        "title": data["title"],
        "description": data.get("description", ""),
        "due_date": data["due_date"],
        "category": int(item_id),
    }

    try:
        await api.create_task(token, task_data)
        await event.message.answer("Задача успешно создана!")
    except ValueError as e:
        await event.message.answer(f"Ошибка при создании задачи: {e}")

    await manager.done()

add_task_dialog = Dialog(
    Window(
        Const("Введите заголовок задачи:"),
        MessageInput(on_title),
        state=AddTaskDialog.title,
    ),
    Window(
        Const("Введите описание (или напишите /skip):"),
        MessageInput(on_description),
        state=AddTaskDialog.description,
    ),
    Window(
        Const("Введите дату дедлайна (YYYY-MM-DD HH:MM):"),
        MessageInput(on_due_date),
        state=AddTaskDialog.due_date,
    ),
    Window(
        Const("Выберите категорию задачи:"),
        Group(
            Select(
                Format("{item[0]}"),
                id="category_select",
                items="categories",
                item_id_getter=lambda x: x[1],
                on_click=on_category_selected,
            ),
            width=2,
        ),
        state=AddTaskDialog.category,
        getter=get_categories,
    ),
)