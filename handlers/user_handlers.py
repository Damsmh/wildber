from aiogram import Router, F
from aiogram.filters import Command, CommandStart, callback_data
from aiogram.filters.callback_data import CallbackData, CallbackQuery
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from keyboards.keyboard import keyboard, keyboard_logged
from db.functions import UserInBase, GetId, AddUser, DeleteUser
from db.models import session, User, Product

from states.states import Registration, Product, Search, SearchPaginator, SearchProduct

router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    if UserInBase(TG=message.from_user.id):
        await state.set_state(Registration.logged)
        await message.answer(text='Выберите опцию', reply_markup=keyboard_logged)
    else:
        await state.set_state(Registration.not_logged)
        await message.answer(text='Привет! Я помогу тебе с анализом цены товара на Wildberries', reply_markup=keyboard)

@router.message(Command(commands='help'))
async def process_help_command(message: Message, state: FSMContext):
    await message.answer(text='Помощи не будет')

@router.message(F.text == 'Зарегистрироваться', StateFilter(Registration.not_logged))
async def process_registartion(message: Message, state: FSMContext):
    if UserInBase(TG=message.from_user.id):
        await state.set_state(Registration.logged)
        await message.answer(text='Вы уже зарегистрированы!', reply_markup=keyboard_logged)
    else:
        try:
            AddUser(username=message.from_user.username, user_id=message.from_user.id)
            await message.answer(text='Вы успешно зарегистрировались!', reply_markup=keyboard_logged)
            await state.set_state(Registration.logged)
        except:
            await message.answer(text='Внутренняя ошибка сервиса! Попробуйте позже.')
            await state.set_state(Registration.not_logged)

@router.message(F.text == 'Отказаться от подписки', StateFilter(Registration.logged, Product.START, Search.START, SearchProduct.START, SearchPaginator.START))
async def process_logout(message: Message, state: FSMContext):
    if UserInBase(TG=message.from_user.id):
        try:
            DeleteUser(message.from_user.id)
            await message.answer(text='Вы отписались!', reply_markup=keyboard)
            await state.set_state(Registration.not_logged)
        except:
            await message.answer(text='Ошибка!', reply_markup=keyboard)
            await state.set_state(Registration.not_logged)
    else:
        await message.answer(text='Вы не вошли!')
        await state.set_state(Registration.not_logged)



