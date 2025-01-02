from aiogram import Router, F
from aiogram.types import Message
from gpt_handler import generate_response
from DDG_handler import duckduckgo_search
from database import add_user_to_db, log_query

router = Router()

@router.message(F.text.startswith("/start"))
async def start_command(message: Message):
    """Команда /start: приветствие и регистрация пользователя."""
    await add_user_to_db(message.chat.id, message.from_user.username)
    await message.answer(
        "Привет! Я могу ответить на ваши вопросы с помощью искусственного интеллекта.\n"
        "Просто напишите команду /ask и ваш вопрос!"
    )

@router.message(F.text.startswith("/ask"))
async def ask_command(message: Message):
    """Обработка команды /ask."""
    query = message.text[len("/ask "):].strip()
    if not query:
        await message.answer("Пожалуйста, напишите ваш вопрос после команды /ask.")
        return

    await message.answer("Генерирую ответ, пожалуйста, подождите...")

    # Выполняем поиск через DuckDuckGo
    search_results = duckduckgo_search(query)

    if not search_results or isinstance(search_results, str):
        search_context = "К сожалению, в интернете ничего не найдено."
    else:
        search_context = "Вот информация, найденная в интернете:\n"
        for i, result in enumerate(search_results[:3], 1):
            search_context += f"{i}. {result['title']}: {result['body'][:150]}...\n"

    # Генерация ответа через GPT, включая результаты поиска
    combined_prompt = (
        f"Пользователь задал вопрос: {query}\n"
        f"{search_context}\n\n"
        "На основе этой информации, напиши чёткий и полезный ответ."
    )
    response = generate_response(combined_prompt)

    # Логирование и отправка ответа
    await log_query(message.chat.id, "ask", query, response)
    await message.answer(response)

def register_handlers(dp):
    """Регистрация маршрутов для бота."""
    dp.include_router(router)
