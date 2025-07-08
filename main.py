import asyncio
from aiogram import Bot,Dispatcher,F
from aiogram.types import Message
from aiogram.filters import CommandStart,Command
from apps.hand import router
from apps.database.models import async_main

async def main ():
    await async_main()
    bot = Bot(token='8012231156:AAEM8GGGotl_ESmxP4O3kKjKxxtrPqEpTuU')  # Fixed typo here
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())


