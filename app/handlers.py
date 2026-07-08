from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile

from app.keyboards import (
    main_menu,
    payment_menu,
    check_payment_menu,
    admin_payment_menu
)

from app.texts import WELCOME_TEXT, tariff_text
from app.tariffs import TARIFFS

from database import Database
from config import ADMIN_ID, CHANNEL_LINK


router = Router()

db = Database()


FULL_PHOTO = FSInputFile("pack_full.jpg")
HALF_PHOTO = FSInputFile("pack_half.jpg")
USDT_QR = FSInputFile("usdt_qr.jpg")


USDT_ADDRESS = "TBajonLpnM53CARU9yJasz5ezCdQPq5CHp"



@router.message(CommandStart())
async def start_handler(message: Message):

    print("START ПОЛУЧЕН")

    db.add_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name
    )


    await message.answer(
    WELCOME_TEXT,
    reply_markup=main_menu()
)


@router.callback_query(F.data.startswith("tariff_"))
async def tariff_handler(callback: CallbackQuery):

    tariff_id = callback.data.replace(
        "tariff_",
        ""
    )


    tariff = TARIFFS.get(tariff_id)


    if not tariff:
        await callback.answer("Ошибка тарифа")
        return


    db.set_tariff(
        callback.from_user.id,
        tariff_id,
        None
    )


    await callback.message.answer_photo(
        photo=HALF_PHOTO,
        caption=tariff_text(
            tariff["name"],
            tariff["price"]
        ),
        reply_markup=payment_menu()
    )


    await callback.answer()



@router.callback_query(F.data == "cloudtips")
async def cloudtips_handler(callback: CallbackQuery):

    user = db.get_user(
        callback.from_user.id
    )

    tariff = TARIFFS.get(user[4])


    await callback.message.answer_photo(
        photo=HALF_PHOTO,

        caption=f"""
💳 Оплата через CloudTips


📦 Тариф:
{tariff["name"]}


💰 Сумма:
{tariff["price"]} ₽


Нажмите на ссылку для оплаты:

https://pay.cloudtips.ru/p/c069b4fc


После оплаты нажмите:
✅ Я оплатил
""",

        reply_markup=check_payment_menu()
    )


    await callback.answer()



@router.callback_query(F.data == "crypto")
async def crypto_handler(callback: CallbackQuery):

    user = db.get_user(
        callback.from_user.id
    )

    if not user:
        await callback.message.answer(
            "❌ Сначала выберите тариф."
        )
        await callback.answer()
        return


    tariff = TARIFFS.get(user[4])


    await callback.message.answer_photo(
        photo=USDT_QR,

        caption=f"""
💎 Оплата USDT (TRC20)


📦 Тариф:
{tariff["name"]}


💰 Сумма:
{tariff["price"]} ₽


📷 Отсканируйте QR-код сверху


💳 Адрес кошелька:

TBajonLpnM53CARU9yJasz5ezCdQPq5CHp


После оплаты нажмите:
✅ Я оплатил
""",

        reply_markup=check_payment_menu()
    )


    await callback.answer()



@router.callback_query(F.data == "check_payment")
async def check_payment_handler(callback: CallbackQuery):

    user = db.get_user(
        callback.from_user.id
    )

    tariff = TARIFFS.get(user[4])


    await callback.message.answer(
        "⏳ Заявка отправлена.\n\n"
        "Ожидайте подтверждения администратора."
    )


    username = callback.from_user.username

    if username:
        username = f"@{username}"
    else:
        username = "Нет username"



    await callback.bot.send_message(
        ADMIN_ID,

        f"""
💰 Новая заявка на оплату


👤 Пользователь:
{callback.from_user.full_name}


🔗 Username:
{username}


🆔 ID:
{callback.from_user.id}


📦 Тариф:
{tariff["name"]}


💵 Сумма:
{tariff["price"]} ₽
""",

        reply_markup=admin_payment_menu(
            callback.from_user.id
        )
    )


    await callback.answer()



@router.callback_query(F.data.startswith("approve_"))
async def approve_payment(callback: CallbackQuery):

    user_id = int(
        callback.data.replace(
            "approve_",
            ""
        )
    )


    db.set_payment_status(
        user_id,
        "paid"
    )


    await callback.bot.send_message(
        user_id,

        "✅ Оплата подтверждена!\n\n"
        "Доступ открыт.\n\n"
        f"Ссылка на канал:\n{CHANNEL_LINK}"
    )


    await callback.message.edit_text(
        "✅ Оплата подтверждена"
    )


    await callback.answer()



@router.callback_query(F.data.startswith("reject_"))
async def reject_payment(callback: CallbackQuery):

    user_id = int(
        callback.data.replace(
            "reject_",
            ""
        )
    )


    db.set_payment_status(
        user_id,
        "rejected"
    )


    await callback.bot.send_message(
        user_id,

        "❌ Оплата не подтверждена."
    )


    await callback.message.edit_text(
        "❌ Оплата отклонена"
    )


    await callback.answer()