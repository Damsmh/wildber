import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram_dialog import setup_dialogs
from config_data.config import Config, load_config
from handlers import user_handlers, dialog


async def main():
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    dp.include_router(user_handlers.router)
    dp.include_router(dialog.paginator)
    dp.include_router(dialog.router)
    setup_dialogs(dp)

    await dp.start_polling(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())