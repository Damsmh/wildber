from environs import Env

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F 
from aiogram.types import Message, CallbackQuery, ContentType

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row, Url

from db.functions import UserInBase

from parser.parser import parser

env = Env()
env.read_env()

class Paginator(StatesGroup):
    START = State()

class Search(StatesGroup):
    START = State()

NEXT_PAGE_BTN_ID = "next"
PREVIOUS_PAGE_BTN_ID = "previous"
PAGE=1
PRODUCT = []

router = Router()

@router.message(F.text == 'Искать товары')
async def start_search(message: Message, state: FSMContext):
    await state.set_state(Search.START)
    print('dialog_pre_start')
    await message.answer('Напишите название товара')

@router.message(Search.START)
async def start(message: Message, state: FSMContext, dialog_manager: DialogManager):
    global PRODUCT
    PRODUCT = parser.run(message.text)
    print('dialog_start')
    await dialog_manager.start(Paginator.START)

async def page_select(callback: CallbackQuery, button: Button,
                     manager: DialogManager, state: FSMContext):
    print('dialog_page')
    if state.get_state() == Paginator.START:
        global PAGE
        if button.callback_prefix()[:-1] == NEXT_PAGE_BTN_ID and PAGE < 101:
            PAGE += 1
        elif button.callback_prefix()[:-1] == PREVIOUS_PAGE_BTN_ID and PAGE > 1:
            PAGE -= 1

async def getter(**kwargs):
    global PAGE
    return {'page_str': f'{PAGE}/100',
            'preview': PRODUCT[PAGE-1]['preview'],
            'name': PRODUCT[PAGE-1]['name'],
            'link': PRODUCT[PAGE-1]['link'],
            'brand': PRODUCT[PAGE-1]['brand'],
            'feedbacks': PRODUCT[PAGE-1]['feedbacks'],
            'price': PRODUCT[PAGE-1]['price'],
            'rating': PRODUCT[PAGE-1]['reviewRating'],}
    
paginator = Dialog(
    Window(
        StaticMedia(
            url='{preview}',
            type=ContentType.PHOTO
        ),
        Format('''Название: {name} 
Бренд: {brand}      Рейтинг: {rating}   
Отзывов: {feedbacks}    Цена: {price} Р'''
        ),
        Row(
            Button(
            Const("<"),
            id=PREVIOUS_PAGE_BTN_ID,
            on_click=page_select,
            ),
            Button(
                Format('Товар {page_str}'),
                id='',
            ),
            Button(
            Const(">"),
            id=NEXT_PAGE_BTN_ID,
            on_click=page_select,
            ),
        ),
        Row(
            Button(
            Const("Добавить в отслеживаемые"),
            id=PREVIOUS_PAGE_BTN_ID,
            on_click=page_select,
            ),
            Button(
            Const("Убрать из отслеживаемого"),
            id=PREVIOUS_PAGE_BTN_ID,
            on_click=page_select,
            ),
        ),
        # Url(
        #     Const("Открыть в Wildberries"),
        #     url='{link}'
        # ),
        state=Paginator.START,
        getter=getter
    )
)