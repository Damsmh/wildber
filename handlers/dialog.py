from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row, Url, Back, Cancel, ListGroup
from aiogram_dialog.widgets.common import Whenable
from typing import *

from parser.parser import Parser

from states.states import SearchPaginator, Search, Registration, Product, SearchProduct

from db.functions import ProductInFavourite, ProductInBase, AddProduct, AddFavourite, DeleteFavourite

parser = Parser()
NEXT_page_BTN_ID = "next"
PREVIOUS_page_BTN_ID = "previous"
USER_DATA = {}

router = Router()

@router.message(StateFilter(Registration.logged), F.text == 'Искать товары')
async def start_search_query(message: Message, state: FSMContext):
    await state.set_state(Search.START)
    USER_DATA[message.from_user.id] = {}
    USER_DATA[message.from_user.id]['page'] = 1
    await message.answer('Напишите название товара')

@router.message(StateFilter(Product.START, Search.START, SearchProduct.START, SearchPaginator.START), F.text == 'Искать товары')
async def continue_search_query(message: Message, state: FSMContext):
    await state.set_state(Search.START)
    USER_DATA[message.from_user.id] = {}
    USER_DATA[message.from_user.id]['page'] = 1
    await message.answer('Напишите название товара')

@router.message(StateFilter(Product.START, Search.START, SearchProduct.START, SearchPaginator.START), F.text == 'Поиск по артикулу')
async def continue_search_article(message: Message, state: FSMContext):
    await state.set_state(Product.START)
    await message.answer('Напишите Артикул')
    if message.from_user.id in USER_DATA:
        USER_DATA[message.from_user.id]['product'] = {}
    else:
        USER_DATA[message.from_user.id] = {}
        USER_DATA[message.from_user.id]['product'] = {}

@router.message(StateFilter(Registration.logged), F.text == 'Поиск по артикулу')
async def start_search_article(message: Message, state: FSMContext):
    await message.answer('Напишите Артикул')
    await state.set_state(Product.START)
    if message.from_user.id in USER_DATA:
        USER_DATA[message.from_user.id]['product'] = {}
    else:
        USER_DATA[message.from_user.id] = {}
        USER_DATA[message.from_user.id]['product'] = {}

@router.message(Search.START)
async def start_s(message: Message, dialog_manager: DialogManager):
    USER_DATA[message.from_user.id]['products'] = parser.search_query(message.text)
    await dialog_manager.start(SearchPaginator.START)

@router.message(Product.START)
async def start_a(message: Message, dialog_manager: DialogManager, state: FSMContext):
    if message.text.isdigit():
        response = parser.search_article(int(message.text))
        if len(response) > 0:
            search = response[0]
            USER_DATA[message.from_user.id]['product'] = search
            await dialog_manager.start(SearchProduct.START)
        else:
            await message.answer('Товара с таким артикулом не найдено!')
    else:
        await message.answer('Товара с таким артикулом не найдено!')

async def product_window(callback: CallbackQuery, button: Button, manager: DialogManager):
    user_id = callback.from_user.id
    page = USER_DATA[user_id]['page']
    find_by_id = lambda items, target_id: next((item for item in items if item['id'] == int(target_id)), None)
    products = USER_DATA[user_id]['products'][page]['types']
    result = find_by_id(products, manager.item_id)
    USER_DATA[user_id]['product'] = result
    await manager.start(SearchPaginator.PRODUCT)

async def add_fav(callback: CallbackQuery, button: Button, manager: DialogManager):
    uid = callback.from_user.id
    product = USER_DATA[uid]['product']
    if ProductInBase(product_id=product['id']):
        try:
            AddFavourite(user_id=uid, product_id=product['id'])
        except:
            print('fail to add fav!')
    else:
        AddProduct(product=product)
        AddFavourite(user_id=uid, product_id=product['id'])

async def del_fav(callback: CallbackQuery, button: Button, manager: DialogManager):
    uid = callback.from_user.id
    product = USER_DATA[uid]['product']
    try:
        DeleteFavourite(user_id=uid, product_id=product['id'])
    except:
        print('fail to add fav!')

async def get_vars(callback: CallbackQuery, button: Button, manager: DialogManager):
    uid = callback.from_user.id
    page = USER_DATA[uid]['page']
    product_id = USER_DATA[uid]['products'][page]['id']
    types = parser.search_product_types(product_id)
    USER_DATA[uid]['products'][page]['types'] = types

def have_types(data: Dict, widget: Whenable, manager: DialogManager):
    product_id = data.get('id')
    user_id = data.get('user_id')
    page = data.get('page')
    return 'types' in USER_DATA[user_id]['products'][page]


def in_fav(data: Dict, widget: Whenable, manager: DialogManager):
    product_id = data.get('id')
    user_id = data.get('user_id')
    return ProductInFavourite(product_id=product_id, user_id=user_id) != []

def not_in_fav(data: Dict, widget: Whenable, manager: DialogManager):
    product_id = data.get('id')
    user_id = data.get('user_id')
    return ProductInFavourite(product_id=product_id, user_id=user_id) == []

async def page_select(callback: CallbackQuery, button: Button, manager: DialogManager):
    user_products = USER_DATA[callback.from_user.id]['products']
    user_page = USER_DATA[callback.from_user.id]['page']
    if button.widget_id == NEXT_page_BTN_ID and user_page < user_products[0]['count']:
        USER_DATA[callback.from_user.id]['page'] += 1
    elif button.widget_id == PREVIOUS_page_BTN_ID and user_page > 1:
        USER_DATA[callback.from_user.id]['page'] -= 1

async def search_getter(**kwargs):
    user_id = kwargs['event_from_user'].id
    page = USER_DATA[user_id]['page']
    product = USER_DATA[user_id]['products']
    res_dict = {'count': product[0]['count'],
                'id':  product[page]['id'],
                'page_str': f'{page}/{product[0]["count"]}',
                'page': page,
                'preview': product[page]['preview'],
                'name': product[page]['name'],
                'link': product[page]['link'],
                'brand': product[page]['brand'],
                'feedbacks': product[page]['feedbacks'],
                'price': product[page]['price'],
                'rating': product[page]['reviewRating'],
                'product': product[page],
                'user_id': user_id,
                }
    if 'types' in product[page]: res_dict['types'] = product[page]['types']
    return res_dict

async def product_getter(**kwargs):
    user_id = kwargs['event_from_user'].id
    product = USER_DATA[user_id]['product']
    return {'id': product['id'],
            'preview': product['preview'],
            'name': product['name'],
            'link': product['link'],
            'brand': product['brand'],
            'feedbacks': product['feedbacks'],
            'price': product['price'],
            'rating': product['reviewRating'],
            'user_id': user_id,
            'product': product,
            }

paginator = Dialog(
    Window(
        StaticMedia(
            url=Format('{preview}'),
            type=ContentType.PHOTO,
        ),
        Format('''Название: {name}
Артикул: {id}
Бренд: {brand}      Рейтинг: {rating}
Отзывов: {feedbacks}      Цена: {price} Р'''
        ),
        Row(
            Button(
                Const("<"),
                id=PREVIOUS_page_BTN_ID,
                on_click=page_select,
            ),
            Button(
                Format('Товар {page_str}'),
                id='',
            ),
            Button(
                Const(">"),
                id=NEXT_page_BTN_ID,
                on_click=page_select,
            ),
        ),
        Button(
                Const("Посмотреть все виды"),
                id='get_vars',
                on_click=get_vars,
            ),
        ListGroup(
            Button(
                Format("{item[name]}"),
                id="button",
                on_click=product_window,
            ),
            id="s_item",
            item_id_getter=lambda item: item["id"],
            items="types",
            when=have_types
        ),
        Url(
            text=Const("Открыть в Wildberries"),
            url=Format('{link}'),
            id='link'
        ),
        Cancel(Const("Закрыть")),
        state=SearchPaginator.START,
        getter=search_getter
    ),
    Window(
        StaticMedia(
            url=Format('{preview}'),
            type=ContentType.PHOTO,
        ),
        Format('''Название: {name} 
Артикул: {id}
Бренд: {brand}      Рейтинг: {rating}   
Отзывов: {feedbacks}      Цена: {price} Р'''
        ),
        Row(
            Back(
                Const('Назад'),
            ),
            Button(
                Const('Отслеживать'),
                id='add_fav',
                when=not_in_fav,
                on_click=add_fav,
            ),
            Button(
                Const('Перестать отслеживать'),
                id='del_fav',
                when=in_fav,
                on_click=del_fav,
            ),
        ),
        state=SearchPaginator.PRODUCT,
        getter=product_getter
    )
)

product = Dialog (
    Window(
        StaticMedia(
            url=Format('{preview}'),
            type=ContentType.PHOTO,
        ),
        Format('''Название: {name} 
Артикул: {id}
Бренд: {brand}      Рейтинг: {rating}   
Отзывов: {feedbacks}      Цена: {price} Р'''
        ),
        Button(
            Const('Отслеживать'),
            id='add_fav',
            when=not_in_fav,
            on_click=add_fav,
        ),
        Button(
            Const('Перестать отслеживать'),
            id='del_fav',
            when=in_fav,
            on_click=del_fav,
        ),
        Cancel(Const("Закрыть")),
        state=SearchProduct.START,
        getter=product_getter
    )
)