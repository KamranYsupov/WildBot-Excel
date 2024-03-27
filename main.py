import asyncio

from aiogram import Bot, Dispatcher

from config import TELEGRAM_BOT_TOKEN, bot
from handlers.basic import basic_router


async def start():
    dp = Dispatcher()

    dp.include_router(basic_router)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
