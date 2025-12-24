import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, ReplyKeyboardMarkup, 
    KeyboardButton, WebAppInfo,
)
from config import TG_BOT_TOKEN, APP_URL

bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    bot_username = (await bot.get_me()).username
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="Открыть Mini App",
                web_app=WebAppInfo(url=APP_URL)
            )]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await message.answer(
        "Привет! Нажми кнопку ниже, чтобы открыть Mini App:",
        reply_markup=keyboard
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
