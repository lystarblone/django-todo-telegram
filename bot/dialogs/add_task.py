from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row, Select, Cancel
from aiogram_dialog.widgets.input import MessageInput
from datetime import datetime
import pytz
from ..config import TIMEZONE
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class AddTaskSG(StatesGroup):
    title = State()
    description = State()
    due_date = State()
    category = State()

async def get_categories(dialog_manager: DialogManager, **kwargs) -> Dict:
    api = dialog_manager.middleware_data['api']
    token = dialog_manager.middleware_data['token']
    try:
        categories = api.get_categories(token)
        return {'categories': [(cat['name'], cat['id']) for cat in categories]}
    except ValueError:
        return {'categories': []}

async def on_title(message: Message, dialog_manager: DialogManager):
    await dialog_manager.update({'title': message.text})
    await dialog_manager.switch_to(AddTaskSG.description)

async def on_description(message: Message, dialog_manager: DialogManager):
    await dialog_manager.update({'description': message.text})
    await dialog_manager.switch_to(AddTaskSG.due_date)

async def on_due_date(message: Message, dialog_manager: DialogManager):
    try:
        due_date = datetime.strptime(message.text, '%Y-%m-%d %H:%M')
        tz = pytz.timezone(TIMEZONE)
        due_date = tz.localize(due_date).astimezone(pytz.utc).isoformat()
        await dialog_manager.update({'due_date': due_date})
        await dialog_manager.switch_to(AddTaskSG.category)
    except ValueError:
        await message.answer("Invalid date format. Use YYYY-MM-DD HH:MM")

async def on_category_selected(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, item_id: str):
    await dialog_manager.update({'category_id': item_id})
    await create_task(dialog_manager)

async def on_new_category(message: Message, dialog_manager: DialogManager):
    api = dialog_manager.middleware_data['api']
    token = dialog_manager.middleware_data['token']
    try:
        cat = api.create_category(token, message.text)
        await dialog_manager.update({'category_id': cat['id']})
        await create_task(dialog_manager)
    except ValueError:
        await message.answer("Error creating category.")

async def create_task(dialog_manager: DialogManager):
    data = dialog_manager.dialog_data
    api = dialog_manager.middleware_data['api']
    token = dialog_manager.middleware_data['token']
    task_data = {
        'title': data['title'],
        'description': data.get('description', ''),
        'due_date': data['due_date'],
        'category': data['category_id']
    }
    try:
        api.create_task(token, task_data)
        await dialog_manager.done()
        await dialog_manager.event.answer("Task created successfully!")
    except ValueError:
        await dialog_manager.event.answer("Error creating task.")

title_window = Window(
    Const("Enter task title:"),
    MessageInput(on_title),
    state=AddTaskSG.title
)

description_window = Window(
    Const("Enter description (optional):"),
    MessageInput(on_description),
    Cancel(Const("Skip")),
    state=AddTaskSG.description
)

due_date_window = Window(
    Const(f"Enter due date (YYYY-MM-DD HH:MM in {TIMEZONE}):"),
    MessageInput(on_due_date),
    state=AddTaskSG.due_date
)

category_window = Window(
    Const("Select category or enter new:"),
    Select(
        Format("{item[0]}"),
        id="cat_sel",
        item_id_getter=lambda x: x[1],
        items="categories",
        on_click=on_category_selected
    ),
    MessageInput(on_new_category),
    state=AddTaskSG.category,
    getter=get_categories
)

add_task_dialog = Dialog(
    title_window,
    description_window,
    due_date_window,
    category_window
)