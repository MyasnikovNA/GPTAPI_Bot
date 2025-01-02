import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import register_handlers
from database import setup_database

# Загрузка токена из .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def on_startup():
    await setup_database()

async def main():
    await on_startup()
    register_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
