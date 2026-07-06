import asyncio
import logging
from datetime import datetime,timedelta
from aiogram import Bot,Dispatcher,F
from aiogram.types import Message,CallbackQuery,InlineKeyboardMarkup,InlineKeyboardButton,FSInputFile,PreCheckoutQuery,LabeledPrice
from aiogram.filters import CommandStart
from texts import txt1,txt2,btn1,btn2,btn_crypto,btn_back,btn_privet
BOT_TOKEN="8838578995:AAF9u9tmbnYxBby0Wr4gLP91xiswYV0wTIo"
ADMIN_ID=5981813410
CHANNEL_ID=-1002348225190
bot=Bot(token=BOT_TOKEN)
dp=Dispatcher()
def main_menu():
 return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=btn1,callback_data="pack_half")],[InlineKeyboardButton(text=btn2,callback_data="pack_full")]])
def pay_menu():
 return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Cloudtips",url="https://pay.cloudtips.ru/p/c069b4fc")],[InlineKeyboardButton(text=btn_crypto,callback_data="crypto")],[InlineKeyboardButton(text=btn_back,callback_data="back_main")]])
@dp.message(CommandStart())
async def start(message:Message):
 await message.answer_photo(FSInputFile("welcome.jpg"),caption=btn_privet,reply_markup=main_menu())
@dp.callback_query(F.data=="pack_half")
async def pack_half(callback:CallbackQuery):
 await callback.message.answer_photo(FSInputFile("pack_half.jpg"),caption=txt1,reply_markup=pay_menu())
 await callback.answer()
@dp.callback_query(F.data=="pack_full")
async def pack_full(callback:CallbackQuery):
 await callback.message.answer_photo(FSInputFile("pack_full.jpg"),caption=txt2,reply_markup=pay_menu())
 await callback.answer()
@dp.callback_query(F.data=="back_main")
async def back_main(callback:CallbackQuery):
 await callback.message.answer_photo(FSInputFile("welcome.jpg"),caption=btn_privet,reply_markup=main_menu())
 await callback.answer()
@dp.callback_query(F.data=="crypto")
async def crypto(callback:CallbackQuery):
 await callback.message.answer("USDT TRC20: TBajonLpnM53CARU9yJasz5ezCdQPq5CHp. Posle perevoda napishi @DeskDollG3")
 await callback.answer()
@dp.message(F.text.startswith("/give"))
async def give_access(message:Message):
 if message.from_user.id!=ADMIN_ID:
  return
 try:
  _,user_id,pack=message.text.split()
  user_id=int(user_id)
  if pack=="half":
   exp=datetime.now()+timedelta(days=365)
   lnk=await bot.create_chat_invite_link(chat_id=CHANNEL_ID,member_limit=1,expire_date=exp)
   await bot.send_message(user_id,"Dostup vydan! 1 god. Ssylka: "+lnk.invite_link)
  else:
   lnk=await bot.create_chat_invite_link(chat_id=CHANNEL_ID,member_limit=1)
   await bot.send_message(user_id,"Dostup vydan navsegda! Ssylka: "+lnk.invite_link)
  await message.answer("Gotovo!")
 except Exception as e:
  await message.answer("Oshibka: "+str(e))
async def main():
 logging.basicConfig(level=logging.INFO)
 await dp.start_polling(bot)
if __name__=="__main__":
 asyncio.run(main())
