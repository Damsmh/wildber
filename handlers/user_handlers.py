from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from keyboards.keyboard import keyboard, keyboard_logged, adm_keyboard
from db.functions import UserInBase, AddUser, DeleteUser, UserList
from db.models import Product

from states.states import Registration, Product, Search, SearchPaginator, SearchProduct, AdminTab
from middlware.middlware import AdminCheckMiddleware, BanCheckMiddleware
from .admin_handlers import admin_router, USERS


router = Router()
router.message.middleware(BanCheckMiddleware())
admin_router.message.middleware(AdminCheckMiddleware())
USER_DATA = {}

@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    if await UserInBase(TG=message.from_user.id):
        await state.set_state(Registration.logged)
        USER_DATA[message.from_user.id] = {}
        await message.answer(text='Выберите опцию', reply_markup=keyboard_logged)
    else:
        await state.set_state(Registration.not_logged)
        await message.answer(text='Привет! Я помогу тебе с анализом цены товара на Wildberries', reply_markup=keyboard)

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text='@Dantes8068')

@admin_router.message(Command(commands='admin'))
async def process_help_command(message: Message, state: FSMContext):
    await state.set_state(AdminTab.admin)
    await message.answer(text='Выберите опцию', reply_markup=adm_keyboard)


@router.message(F.text == 'Зарегистрироваться', StateFilter(Registration.not_logged))
async def process_registartion(message: Message, state: FSMContext):
    if await UserInBase(TG=message.from_user.id):
        await state.set_state(Registration.logged)
        await message.answer(text='Вы уже зарегистрированы!', reply_markup=keyboard_logged)
    else:
        try:
            await AddUser(username=message.from_user.username, user_id=message.from_user.id)
            await message.answer(text='Вы успешно зарегистрировались!', reply_markup=keyboard_logged)
            await state.set_state(Registration.logged)
        except:
            await message.answer(text='Внутренняя ошибка сервиса! Попробуйте позже.')
            await state.set_state(Registration.not_logged)

@router.message(F.text == 'Отказаться от подписки', StateFilter(Registration.logged, Product.START, Search.START, SearchProduct.START, SearchPaginator.START))
async def process_logout(message: Message, state: FSMContext):
    if await UserInBase(TG=message.from_user.id):
        try:
            await DeleteUser(message.from_user.id)
            await message.answer(text='Вы отписались!', reply_markup=keyboard)
            await state.set_state(Registration.not_logged)
        except:
            await message.answer(text='Ошибка!', reply_markup=keyboard)
            await state.set_state(Registration.not_logged)
    else:
        await message.answer(text='Вы не вошли!')
        await state.set_state(Registration.not_logged)



