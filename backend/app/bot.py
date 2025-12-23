import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, 
    InlineKeyboardButton, InlineKeyboardMarkup,
    WebAppInfo
)
from config import TG_BOT_TOKEN, APP_URL

bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Open Mini App",
            web_app=WebAppInfo(url=APP_URL)
        )]
    ])
    await message.answer("Welcome! Open the Mini App:", reply_markup=keyboard)

async def main():
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
