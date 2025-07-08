import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from contextlib import asynccontextmanager
from apps.hand import router
from apps.database.models import async_main


@asynccontextmanager
async def lifespan(dp: Dispatcher):
    # Действия при запуске бота
    print("Бот запускается...")
    
    # Здесь можно добавить инициализацию, например:
    # - Загрузку данных из БД
    # - Создание подключений
    # - Предзагрузку клавиатур и т.д.
    
    yield  # Здесь бот работает
    
    # Действия при остановке бота
    print("Бот останавливается...")
    # Здесь можно добавить:
    # - Сохранение данных
    # - Закрытие подключений
    # - Уведомление админа

async def main():
    # Инициализация базы данных
    await async_main()
    
    # Создаем бота и диспетчер
    bot = Bot(token='8012231156:AAEM8GGGotl_ESmxP4O3kKjKxxtrPqEpTuU')
    
    # Исправлено: storage вместо sotrage
    dp = Dispatcher(
        storage=MemoryStorage(),
        lifespan=lifespan
    )
    
    # Подключаем роутер
    dp.include_router(router)
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())