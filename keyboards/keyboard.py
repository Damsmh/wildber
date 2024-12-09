from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard  import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import callback_data, StateFilter
from aiogram.fsm.context import FSMContext


from states.states import Registration

class AdmCallbackFactory(CallbackData, prefix='adm'):
    action: str | None
    id: int | None

logged_builder = ReplyKeyboardBuilder()
Unlogged_builder = ReplyKeyboardBuilder()
admin_builder = InlineKeyboardBuilder()

user_count = InlineKeyboardButton(text="Кол-во пользователей", callback_data=AdmCallbackFactory(action="count", id=1).pack())
user_ban = InlineKeyboardButton(text="Забанить", callback_data=AdmCallbackFactory(action="ban", id=2).pack())
user_unban = InlineKeyboardButton(text="Разбанить", callback_data=AdmCallbackFactory(action="unban", id=3).pack())
admin_exit = InlineKeyboardButton(text="Закрыть", callback_data=AdmCallbackFactory(action="exit", id=4).pack())
users = InlineKeyboardButton(text="Список пользователей", callback_data=AdmCallbackFactory(action="users", id=5).pack())


reg_btn = KeyboardButton(text='Зарегистрироваться')
logout_btn = KeyboardButton(text='Отказаться от подписки')
query_search_btn = KeyboardButton(text='Искать товары')
article_search_btn = KeyboardButton(text='Поиск по артикулу')
liked_btn = KeyboardButton(text='Мои товары')

logged_builder.row(logout_btn, query_search_btn, article_search_btn, liked_btn, width=4)
Unlogged_builder.row(reg_btn, width=2)
admin_builder.add(user_count)
admin_builder.row(user_ban, user_unban, width=2)
admin_builder.add(admin_exit)
admin_builder.row(users)

adm_keyboard: InlineKeyboardMarkup = admin_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=False
)

keyboard: ReplyKeyboardMarkup = Unlogged_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)

keyboard_logged: ReplyKeyboardMarkup = logged_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=False
)

