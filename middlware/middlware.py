from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import *
from config_data.config import Config, load_config

config: Config = load_config()

class AdminCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, message: Message, data):
        if message.from_user.id not in config.admin_ids.ids:
            await  message.answer(text='Вы не админ!')
            return
        return await handler(message, data)
    
class BanCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, message: Message, data):
        if message.from_user.id not in config.admin_ids.ids:
            await  message.answer(text='Вы не админ!')
            return
        return await handler(message, data)
        