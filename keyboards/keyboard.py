from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard  import ReplyKeyboardBuilder




kb_builder = ReplyKeyboardBuilder()

quiz_easy_1_builder = ReplyKeyboardBuilder()
quiz_easy_2_builder = ReplyKeyboardBuilder()
quiz_easy_3_builder = ReplyKeyboardBuilder()

quiz_hard_1_builder = ReplyKeyboardBuilder()
quiz_hard_2_builder = ReplyKeyboardBuilder()
quiz_hard_3_builder = ReplyKeyboardBuilder()

# Создаем кнопки
survey_btn = KeyboardButton(text='Пройти опрос')
viktor_btn_easy = KeyboardButton(text='Пройти викторину (легко)')
viktor_btn_hard = KeyboardButton(text='Пройти викторину (сложно)')

x = 3

# Добавляем кнопки в билдер
kb_builder.row(survey_btn, viktor_btn_easy, viktor_btn_hard, width=2)


# Создаем объект клавиатуры
keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)
easy_quiz_keyboards = [quiz_easy_1_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
),
quiz_easy_2_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
),
quiz_easy_3_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)]

hard_quiz_keyboards = [quiz_hard_1_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
),
quiz_hard_2_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
),
quiz_hard_3_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
)]