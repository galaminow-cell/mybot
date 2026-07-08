import asyncio

from aiogram import Bot, Dispatcher
from aiohttp import web

from config import BOT_TOKEN
from database import Database
from app.handlers import router


async def health_check(request):
    return web.Response(text="Bot is running")


async def start_web_server():

    app = web.Application()

    app.router.add_get("/", health_check)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        10000
    )

    await site.start()



async def main():

    bot = Bot(
        token=BOT_TOKEN
    )


    dp = Dispatcher()

    dp.include_router(router)


    db = Database()
    db.create_tables()


    print("Бот запущен")


    await start_web_server()


    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())