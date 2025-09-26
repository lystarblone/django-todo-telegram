from aiogram.fsm.state import State, StatesGroup

class AddTaskDialog(StatesGroup):
    title = State()
    description = State()
    due_date = State()
    category = State()