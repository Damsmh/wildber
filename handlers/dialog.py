import asyncio
from typing import Dict, Any
from environs import Env

from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup

from aiogram import Router, F, Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, ContentType

from aiogram_dialog import Dialog, Window, setup_dialogs, DialogManager
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Checkbox, Button, Row, Cancel, Start, Back, Next

from parser.parser import parser

env = Env()
env.read_env()

class Paginator(StatesGroup):
    START = State()


NEXT_PAGE_BTN_ID = "next"
PREVIOUS_PAGE_BTN_ID = "previous"
PAGE=1
PRODUCT = []


router = Router()


@router.message(F.content_type == ContentType.TEXT)
async def start(message: Message, dialog_manager: DialogManager):
    global PRODUCT
    PRODUCT = parser.run(message.text)
    await dialog_manager.start(Paginator.START)





async def page_select(callback: CallbackQuery, button: Button,
                     manager: DialogManager):
    global PAGE
    if button.callback_prefix()[:-1] == NEXT_PAGE_BTN_ID and PAGE < 101:
        PAGE += 1
    elif button.callback_prefix()[:-1] == PREVIOUS_PAGE_BTN_ID and PAGE > 1:
        PAGE -= 1
    


    

async def getter(**kwargs):
    global PAGE
    return {'page_str': f'{PAGE}/100',
            'name': PRODUCT[PAGE-1]['name'],
            'link': PRODUCT[PAGE-1]['link'],
            'brand': PRODUCT[PAGE-1]['brand'],
            'feedbacks': PRODUCT[PAGE-1]['feedbacks'],
            'price': PRODUCT[PAGE-1]['price'],
            'rating': PRODUCT[PAGE-1]['reviewRating'],}
    
    

paginator = Dialog(
    Window(
        Const("Найденные товары"),
        
        Button(
            Const("<"),
            id=PREVIOUS_PAGE_BTN_ID,
            on_click=page_select,
            
        ),
        Format(
            text='''Товар {page_str}
Название: {name}\n 
Бренд: {brand}      Рейтинг: {rating}   
Отзывов: {feedbacks}    Цена: {price} Р
{link}'''
        ),
        Button(
            Const(">"),
            id=NEXT_PAGE_BTN_ID,
            on_click=page_select,
            
        ),
        state=Paginator.START,
        getter=getter
    )
)



