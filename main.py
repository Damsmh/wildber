import asyncio
from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from config_data.config import Config, load_config
from handlers import user_handlers, dialog, admin_handlers, other_handlers
from aiogram.types import BotCommand
from sheduler.sheduler import checkPrice


async def periodic_check_price():
    while True:
        await checkPrice()
        await asyncio.sleep(20)

async def start_bot():
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    main_menu_commands = [
        BotCommand(command='/start',
                   description='Начать'),
        BotCommand(command='/help',
                   description='Помощь'),
        BotCommand(command='/prime',
                   description='Купить Prime'),
    ]
    
    dp.include_router(user_handlers.router)
    dp.include_router(admin_handlers.admin_router)
    # dp.include_router(other_handlers.router)
    dp.include_router(dialog.paginator)
    dp.include_router(dialog.product)
    dp.include_router(dialog.favourite_list)
    dp.include_router(dialog.router)
    
    setup_dialogs(dp)

    await bot.set_my_commands(main_menu_commands)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
async def main():
    await asyncio.gather(start_bot(), periodic_check_price())

if __name__ == '__main__':
    asyncio.run(main())

    


    
    