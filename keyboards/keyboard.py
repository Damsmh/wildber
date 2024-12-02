from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard  import ReplyKeyboardBuilder
from aiogram.filters import callback_data, StateFilter
from aiogram.fsm.context import FSMContext

from states.states import Registration

logged_builder = ReplyKeyboardBuilder()
Unlogged_builder = ReplyKeyboardBuilder()

reg_btn = KeyboardButton(text='Зарегистрироваться',
                         callback_data='registration')
logout_btn = KeyboardButton(text='Отказаться от подписки',
                            callback_data='logout')
start_search_btn = KeyboardButton(text='Искать товары',
                            callback_data='get_search')

logged_builder.row(logout_btn, start_search_btn, width=2)
Unlogged_builder.row(reg_btn, width=2)

keyboard: ReplyKeyboardMarkup = Unlogged_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)

keyboard_logged: ReplyKeyboardMarkup = logged_builder.as_markup(
    resize_keyboard=True,
)

