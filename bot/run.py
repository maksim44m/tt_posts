import asyncio

from aiogram import Bot, Dispatcher

from config import TG_TOKEN
from dependensies import get_db_instance
from handlers import router


if __name__ == '__main__':
    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher(bot=bot, db=get_db_instance())
    dp.include_router(router)

    asyncio.run(dp.start_polling(bot))
