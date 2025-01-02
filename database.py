from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "bot_database"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

async def setup_database():
    """Создание индексов для коллекций."""
    await db.users.create_index("chat_id", unique=True)
    await db.logs.create_index("timestamp")

async def add_user_to_db(chat_id: int, username: str):
    """Добавление пользователя в базу данных."""
    await db.users.update_one(
        {"chat_id": chat_id},
        {"$setOnInsert": {
            "chat_id": chat_id,
            "username": username,
            "join_date": datetime.utcnow()
        }},
        upsert=True
    )

async def log_query(chat_id: int, command: str, query: str, response: str):
    """Логирование запросов пользователей."""
    await db.logs.insert_one({
        "chat_id": chat_id,
        "command": command,
        "query": query,
        "response": response,
        "timestamp": datetime.utcnow()
    })


