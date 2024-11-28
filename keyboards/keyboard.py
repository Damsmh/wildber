from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard  import ReplyKeyboardBuilder
from aiogram.filters import callback_data

main_builder = ReplyKeyboardBuilder()

start_builder = ReplyKeyboardBuilder()

reg_btn = KeyboardButton(text='Зарегистрироваться',
                         callback_data='registration')
logout_btn = KeyboardButton(text='Отказаться от подписки',
                            callback_data='logout')
start_search_btn = KeyboardButton(text='Искать товары',
                            callback_data='get_search')

main_builder.row(reg_btn, logout_btn, width=2)
start_builder.row(start_search_btn, width=2)

reg_keyboard: ReplyKeyboardMarkup = main_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)

search_keyboard: ReplyKeyboardMarkup = start_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=False
)