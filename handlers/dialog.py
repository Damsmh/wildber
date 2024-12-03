import operator
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row, Url, Back, Cancel, Column, Select
from aiogram_dialog.widgets.common import WhenCondition

from parser.parser import parser

from states.states import SearchPaginator, Search, Registration, Product, SearchProduct

NEXT_page_BTN_ID = "next"
PREVIOUS_page_BTN_ID = "previous"
ADD_TO_FAVOURITES = "add_to_fav"
REMOVE_TO_FAVOURITES = "remove_from_fav"
USER_DATA = {}

router = Router()

@router.message(StateFilter(Registration.logged), F.text == 'Искать товары')
async def start_search_query(message: Message, state: FSMContext):
    await state.set_state(Search.START)
    USER_DATA[message.from_user.id] = {}
    USER_DATA[message.from_user.id]['page'] = 1
    await message.answer('Напишите название товара')

@router.message(StateFilter(SearchPaginator.START, SearchProduct.START), F.text == 'Искать товары')
async def continue_search_query(message: Message, state: FSMContext, manager: DialogManager):
    await manager.switch_to(Product.START)
    USER_DATA[message.from_user.id] = {}
    USER_DATA[message.from_user.id]['page'] = 1
    await message.answer('Напишите название товара')

@router.message(StateFilter(SearchPaginator.START, SearchProduct.START), F.text == 'Поиск по артикулу')
async def continue_search_article(message: Message, state: FSMContext, manager: DialogManager):
    await manager.switch_to(Product.START)
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
async def start_a(message: Message, dialog_manager: DialogManager):
    if message.text.isdigit():
        search = parser.search_article(int(message.text))[0]
        if len(search) != 0:
            USER_DATA[message.from_user.id]['product'] = search
            await dialog_manager.start(SearchProduct.START)
        else:
            await message.answer('Товара с таким артикулом не найдено!')
    else:
        await message.answer('Товара с таким артикулом не найдено!')
    


async def page_select(callback: CallbackQuery, button: Button, manager: DialogManager):
    user_products = USER_DATA[callback.from_user.id]['products']
    user_page = USER_DATA[callback.from_user.id]['page']
    if button.callback_prefix()[:-1] == NEXT_page_BTN_ID and user_page < user_products[0]['count']:
        USER_DATA[callback.from_user.id]['page'] += 1
    elif button.callback_prefix()[:-1] == PREVIOUS_page_BTN_ID and user_page > 2:
        USER_DATA[callback.from_user.id]['page'] -= 1

async def search_getter(**kwargs):
    user_id = kwargs['event_from_user'].id
    page = USER_DATA[user_id]['page']
    product = USER_DATA[user_id]['products']
    return {'count': product[0]['count'],
            'id':  product[page]['id'],
            'page_str': f'{page}/{product[0]["count"]}',
            'preview': product[page]['preview'],
            'name': product[page]['name'],
            'link': product[page]['link'],
            'brand': product[page]['brand'],
            'feedbacks': product[page]['feedbacks'],
            'price': product[page]['price'],
            'rating': product[page]['reviewRating'],
            'types': product[page]['types'],
            }

async def product_window(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    user_id = callback.from_user.id
    page = USER_DATA[user_id]['page']
    product_id = button.callback_prefix()[:-1]
    products = USER_DATA[user_id]['products'][page]['types']
    result = list(filter(lambda v: v["id"]==product_id, products.values()))[0]
    USER_DATA[user_id]['product'] = result
    manager.start(SearchPaginator.PRODUCT)

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
        Select(
            Column(
            Format("{item[name]}"),
        ),
            id="s_item",
            item_id_getter=lambda item: item['id'],
            items="types",
            on_click=product_window,
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
            Button(
            Const('Отслеживать'),
            id='add_fav',
            ),
            Button(
                Const('Перестать отслеживать'),
                id='remove_fav',
            ),
            Back(
                Const('Назад'),
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
        ),
        Button(
            Const('Перестать отслеживать'),
            id='remove_fav',
        ),
        Cancel(Const("Закрыть")),
        state=SearchProduct.START,
        getter=product_getter
    )
)