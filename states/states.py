from aiogram.fsm.state import State, StatesGroup

class SearchPaginator(StatesGroup):
    START = State()

class Product(StatesGroup):
    START = State()

class Search(StatesGroup):
    START = State()

class Registration(StatesGroup):
    logged = State()
    not_logged = State()