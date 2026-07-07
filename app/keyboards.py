from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🔥 Неделя • 110 ₽",
                    callback_data="tariff_week"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📅 Месяц • 240 ₽",
                    callback_data="tariff_month"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⭐ Полгода • 370 ₽",
                    callback_data="tariff_halfyear"
                )
            ],

            [
                InlineKeyboardButton(
                    text="👑 Год • 550 ₽",
                    callback_data="tariff_year"
                )
            ],

            [
                InlineKeyboardButton(
                    text="💎 Вечный • 1299 ₽",
                    callback_data="tariff_forever"
                )
            ]

        ]
    )



def payment_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="💳 CloudTips",
                    callback_data="cloudtips"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🪙 Оплата USDT",
                    callback_data="crypto"
                )
            ]

        ]
    )



def check_payment_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="✅ Я оплатил",
                    callback_data="check_payment"
                )
            ]

        ]
    )



def admin_payment_menu(user_id):

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="✅ Подтвердить",
                    callback_data=f"approve_{user_id}"
                )
            ],

            [
                InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data=f"reject_{user_id}"
                )
            ]

        ]
    )