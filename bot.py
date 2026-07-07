import asyncio
import os

from aiohttp import web
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import Database
from app.handlers import router


async def start_web_server():

    async def handle(request):
        return web.Response(
            text="Bot is running"
        )

    app = web.Application()

    app.router.add_get(
        "/",
        handle
    )

    runner = web.AppRunner(app)

    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        int(os.getenv("PORT", 10000))
    )

    await site.start()



async def main():

    await start_web_server()


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