from db.functions import FavouriteUser, UpdateProductPrice, update_price_history
from parser.parser import Parser
from config_data.config import load_config, Config
from aiogram import Bot
from keyboards.keyboard import shedule_builder
from aiogram.types import InlineKeyboardButton
import matplotlib.pyplot as plt
import io


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
                    await update_price_history(product.product_id, product_now[0]['price'])
                except:
                    print('Не удалось обновить цену')

def plot_price_history(article, price_data):
    timestamps = [record.timestamp for record in price_data]
    prices = [record.price for record in price_data]

    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, prices, marker='o', linestyle='-', color='b', label=f'Article {article}')
    plt.xlabel('Дата')
    plt.ylabel('Цена')
    plt.title(f'История цен товара с пртикулом: {article}')
    plt.legend()
    plt.grid(True)

    # Сохранение графика в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf