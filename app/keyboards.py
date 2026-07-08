from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="🔥 Неделя • 149 ₽",
                    callback_data="tariff_week"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📅 Месяц • 299 ₽",
                    callback_data="tariff_month"
                )
            ],

            [
                InlineKeyboardButton(
                    text="👑 Год • 599 ₽ ⭐ Самый популярный",
                    callback_data="tariff_year"
                )
            ],

            [
                InlineKeyboardButton(
                    text="💎 Навсегда • 1299 ₽",
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
                    text="💎 USDT (TRC20)",
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