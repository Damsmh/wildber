from aiogram import Router, F
from aiogram.filters import Command, CommandStart, callback_data
from aiogram.filters.callback_data import CallbackData, CallbackQuery
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.keyboard import reg_keyboard, search_keyboard
from db.functions import UserInBase, GetId
from db.models import session, User, Product

router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='Привет! Я помогу тебе с анализом цены товара на Wildberries', reply_markup=reg_keyboard)

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='Помощи не будет, умри')

@router.message(F.text == 'Зарегистрироваться')
async def process_registartion(message: Message):
    if UserInBase(TG=message.from_user.id):
        await message.answer(text='Вы уже зарегистрированы!', reply_markup=search_keyboard)
    else:
        try:
            session.add(User(username=message.from_user.username,
                             user_id=message.from_user.id))
            session.commit()
            await message.answer(text='Вы успешно зарегистрировались!', reply_markup=search_keyboard)
        except:
            await message.answer(text='Внутренняя ошибка сервиса! Попробуйте позже.')
        
@router.message(F.text == 'Отказаться от подписки')
async def process_logout(message: Message):
    print('user_logout')
    if UserInBase(TG=message.from_user.id):
        try:
            user = session.query(User).filter(User.user_id == message.from_user.id).one()
            session.delete(user)
            session.commit()
            await message.answer(text='Вы отписались!', reply_markup=reg_keyboard)
        except:
            await message.answer(text='Ошибка!', reply_markup=reg_keyboard)
    else:
        await message.answer(text='Вы не вошли!')



