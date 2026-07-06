import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from texts import txt1, txt2, btn1, btn2, btn_crypto, btn_back, btn_privet

BOT_TOKEN = "8838578995:AAF9u9tmbnYxBby0Wr4gLP91xiswYV0wTIo"
ADMIN_ID = 5981813410
CHANNEL_ID = -1002348225190

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


# ================= KEYBOARDS =================

def main_menu():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton(btn1, callback_data="pack_half")
    ).add(
        InlineKeyboardButton(btn2, callback_data="pack_full")
    )


def pay_menu():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Cloudtips", url="https://pay.cloudtips.ru/p/c069b4fc"))
    kb.add(InlineKeyboardButton(btn_crypto, callback_data="crypto"))
    kb.add(InlineKeyboardButton(btn_back, callback_data="back_main"))
    return kb


# ================= START =================

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer_photo(
        open("welcome.jpg", "rb"),
        caption=btn_privet,
        reply_markup=main_menu()
    )


# ================= PACKS =================

@dp.callback_query_handler(lambda c: c.data == "pack_half")
async def pack_half(callback: types.CallbackQuery):
    await callback.message.answer_photo(
        open("pack_half.jpg", "rb"),
        caption=txt1,
        reply_markup=pay_menu()
    )
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data == "pack_full")
async def pack_full(callback: types.CallbackQuery):
    await callback.message.answer_photo(
        open("pack_full.jpg", "rb"),
        caption=txt2,
        reply_markup=pay_menu()
    )
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data == "back_main")
async def back_main(callback: types.CallbackQuery):
    await callback.message.answer_photo(
        open("welcome.jpg", "rb"),
        caption=btn_privet,
        reply_markup=main_menu()
    )
    await callback.answer()


@dp.callback_query_handler(lambda c: c.data == "crypto")
async def crypto(callback: types.CallbackQuery):
    await callback.message.answer(
        "USDT TRC20: TBajonLpnM53CARU9yJasz5ezCdQPq5CHp\nПосле оплаты напиши админу."
    )
    await callback.answer()


# ================= ADMIN =================

@dp.message_handler(lambda m: m.text and m.text.startswith("/give"))
async def give_access(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        _, user_id, pack = message.text.split()
        user_id = int(user_id)

        if pack == "half":
            exp = datetime.now() + timedelta(days=365)
            link = await bot.create_chat_invite_link(
                chat_id=CHANNEL_ID,
                member_limit=1,
                expire_date=exp
            )
            await bot.send_message(user_id, "Доступ на 1 год: " + link.invite_link)

        else:
            link = await bot.create_chat_invite_link(
                chat_id=CHANNEL_ID,
                member_limit=1
            )
            await bot.send_message(user_id, "Доступ навсегда: " + link.invite_link)

        await message.answer("Готово!")

    except Exception as e:
        await message.answer("Ошибка: " + str(e))


# ================= RUN =================

if name == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)