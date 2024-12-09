from aiogram.fsm.state import State, StatesGroup

class SearchPaginator(StatesGroup):
    START = State()
    PRODUCT = State()

class SearchProduct(StatesGroup):
    START = State()

class Product(StatesGroup):
    START = State()

class FavouriteProducts(StatesGroup):
    START = State()

class Search(StatesGroup):
    START = State()

class Registration(StatesGroup):
    logged = State()
    not_logged = State()

class AdminTab(StatesGroup):
    admin = State()
    ban = State()
    unban = State()