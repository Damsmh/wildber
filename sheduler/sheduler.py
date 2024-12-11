from db.functions import FavouriteUser, UpdateProductPrice
from parser.parser import Parser
from config_data.config import load_config, Config
from aiogram import Bot
from keyboards.keyboard import shedule_builder
from aiogram.types import InlineKeyboardButton

parser = Parser()

async def checkPrice():
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token)
    users_favourite = FavouriteUser()
    for user in users_favourite:
        for product in users_favourite[user]:
            product_now = parser.search_article(product.product_id)
            if product.price != product_now[0]['price']:
                kb = shedule_builder.add(InlineKeyboardButton(text='Открыть в Wildberries', url=product_now[0]['link'])).as_markup()
                await bot.send_message(chat_id=user, text=f'''Цена на ваш товар\n
    {product.name} изменилась!\n
    Старая цена: {product.price}P   Новая цена: {product_now[0]['price']}P''', reply_markup=kb)
                try:
                    await UpdateProductPrice(product.product_id, product_now[0]['price'])
                except:
                    print('Не удалось обновить цену')
            
