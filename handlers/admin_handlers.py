from aiogram import Router, F
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from keyboards.keyboard import keyboard_logged, adm_keyboard, AdmCallbackFactory
from db.functions import UserCount, UserBan, UserUnban, UserList

from states.states import Registration, AdminTab

admin_router = Router()

USERS = ''

@admin_router.callback_query(AdmCallbackFactory.filter(F.action == 'count'), StateFilter(AdminTab.admin))
async def user_count(query: CallbackQuery):
    count = str(await UserCount())
    await query.message.edit_text(text=f'Общее кол-во пользователей: {count}', reply_markup=adm_keyboard)
    await query.answer()

@admin_router.callback_query(AdmCallbackFactory.filter(F.action == 'ban'), StateFilter(AdminTab.admin))
async def user_ban(query: CallbackQuery, state: FSMContext):
    await state.set_state(AdminTab.ban)
    result = await UserList()
    string = ''
    for user in result:
        string += f'username: {user[0]}, uid: {user[1]}\n'
    await query.message.edit_text(text='Введите имя пользователя:\n' + string, reply_markup=adm_keyboard)
    await query.answer()

@admin_router.callback_query(AdmCallbackFactory.filter(F.action == 'unban'), StateFilter(AdminTab.admin))
async def user_unban(query: CallbackQuery, state: FSMContext):
    await state.set_state(AdminTab.unban)
    result = await UserList()
    string = ''
    for user in result:
        string += f'username: {user[0]}, uid: {user[1]}\n'
    await query.message.edit_text(text='Введите имя пользователя:\n' + string, reply_markup=adm_keyboard)
    await query.answer()

@admin_router.message(StateFilter(AdminTab.ban))
async def ban(message: Message, state: FSMContext):
    await state.set_state(AdminTab.admin)
    try:
        await UserBan(message.text)
        await message.answer(text=f'Пользователь {message.text} успешно забанен.', reply_markup=adm_keyboard)
    except:
        await message.answer(text='Не удалось забанить пользователя!', reply_markup=adm_keyboard)

@admin_router.message(StateFilter(AdminTab.unban))
async def unban(message: Message, state: FSMContext):
    await state.set_state(AdminTab.admin)
    try:
        await UserUnban(message.text)
        await message.answer(text=f'Пользователь {message.text} успешно разбанен.', reply_markup=adm_keyboard)
    except:
        await message.answer(text='Не удалось разбанить пользователя!', reply_markup=adm_keyboard)

@admin_router.callback_query(AdmCallbackFactory.filter(F.action == 'users'), StateFilter(AdminTab.admin))
async def get_users(query: CallbackQuery, state: FSMContext):
    result = await UserList()
    string = ''
    for user in result:
        string += f'username: {user[0]}, uid: {user[1]}\n'
    await query.message.edit_text(text=string, reply_markup=adm_keyboard)

@admin_router.callback_query(AdmCallbackFactory.filter(F.action == 'exit'), StateFilter(AdminTab.admin))
async def adm_exit(query: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.logged)
    await query.message.edit_reply_markup()
    await query.message.answer(text='', reply_markup=keyboard_logged)