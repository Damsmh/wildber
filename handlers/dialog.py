from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row, Url, ListGroup, Back
from aiogram_dialog.widgets.common import WhenCondition

from parser.parser import parser

from states.states import SearchPaginator, Search, Registration, Product

NEXT_page_BTN_ID = "next"
PREVIOUS_page_BTN_ID = "previous"
ADD_TO_FAVOURITES = "add_to_fav"
REMOVE_TO_FAVOURITES = "remove_from_fav"
USER_DATA = {}

router = Router()

@router.message(StateFilter(Registration.logged), (F.text == 'Искать товары'))
async def start_search(message: Message, state: FSMContext):
    await state.set_state(Search.START)
    USER_DATA[message.from_user.id] = {}
    USER_DATA[message.from_user.id]['page'] = 1
    await message.answer('Напишите название товара')

@router.message(StateFilter(Registration.logged), F.text == 'Артикул')
async def start_search_article(message: Message, manager: DialogManager, state: FSMContext, dialog_manager: DialogManager):
    if message.from_user.id in USER_DATA:
        USER_DATA[message.from_user.id]['type'] = parser.search_article(message.text)
        await dialog_manager.start(Product.START)
    else:
        USER_DATA[message.from_user.id] = {}
        USER_DATA[message.from_user.id]['type'] = parser.search_article(message.text)
        await dialog_manager.start(Product.START)


@router.message(Search.START)
async def start_s(message: Message, dialog_manager: DialogManager):
    USER_DATA[message.from_user.id]['products'] = parser.search_query(message.text)
    await dialog_manager.start(SearchPaginator.START)

@router.message(Product.START)
async def start_a(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    USER_DATA[callback.from_user.id]['type'] = parser.search_article(button.callback_prefix()[:-1])


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
            'types': product[page]['types']
            }

async def product_getter(**kwargs):
    user_id = kwargs['event_from_user'].id
    product = USER_DATA[user_id]['type']
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
                id=None,
            ),
            Button(
            Const(">"),
            id=NEXT_page_BTN_ID,
            on_click=page_select,
            ),
        ),
        Const('Выберите вид товара:'),
        ListGroup(
            Button(
            Format("{item[name]}"),
            id="button",
            ),
            id="select_search",
            item_id_getter=lambda item: item["id"],
            items="types",
        ),
        Url(
            Const("Открыть в Wildberries"),
            Format('{link}'),
        ),
        state=SearchPaginator.START,
        getter=search_getter
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
        Back(
            Const('Назад'),
            id='back',
        ),
        Button(
            Const('Отслеживать'),
            id='add_fav',
        ),
        Button(
            Const('Перестать отслеживать'),
            id='remove_fav',
        ),
        state=Product.START,
        getter=product_getter
    )
)