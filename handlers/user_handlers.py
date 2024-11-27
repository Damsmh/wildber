from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from keyboards.keyboard import keyboard

# Инициализируем роутер уровня модуля
router = Router()

bot_mode = 'echo'

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())

async def process_start_command(message: Message):
    global bot_mode
    bot_mode = 'echo'
    await message.answer(text='Напиши названире товара, который хочешь найти')


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='Помощи не будет, умри')


