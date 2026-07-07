import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import Database

from app.handlers import router


async def main():

    bot = Bot(
        token=BOT_TOKEN
    )


    dp = Dispatcher()


    dp.include_router(router)


    db = Database()
    db.create_tables()


    print("Бот запущен")


    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())