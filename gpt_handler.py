import os
import requests
import logging
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Конфигурация модели
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "openai/gpt-4o-mini"
MAX_TOKENS = 300
TEMPERATURE = 0.3  # Для более точных и предсказуемых ответов

def generate_response(prompt: str, search_results: str = "") -> str:
    """Генерация ответа через OpenRouter (GPT-4o mini)."""
    # Новые правила и системное сообщение
    system_message = (
        "Ты являешься самым квалифицированным экспертом и обязан отвечать на вопросы с максимальной точностью, "
        "используя предоставленные данные. Используй найденную информацию, формулируй чёткие и лаконичные ответы "
        "на русском языке. Если требуется, включай дату или факты. Никогда не упоминай, что данные были найдены "
        "в интернете, и не перенаправляй пользователя на внешние сайты."
    )

    # Объединяем запрос пользователя и результаты поиска
    combined_prompt = f"Вопрос: {prompt}\n\nВот данные для ответа:\n{search_results}\n\nОтветь только на основе предоставленных данных."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": combined_prompt}
        ],
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE
    }

    try:
        # Отправка запроса к OpenRouter API
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        logger.info("Успешный запрос к OpenRouter.")
        return result["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка сети: {e}")
        return "Ошибка: проблема с подключением к API."
    except KeyError as e:
        logger.error(f"Ошибка структуры ответа API: {e}")
        return "Ошибка: получен некорректный ответ от API."
    except Exception as e:
        logger.error(f"Непредвиденная ошибка: {e}")
        return f"Ошибка при генерации ответа: {e}"

def test_connection():
    """Проверка подключения к OpenRouter API."""
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": MODEL_NAME,
            "messages": [{"role": "system", "content": "Ping"}],
            "max_tokens": 5
        }
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        logger.info("Успешное подключение к OpenRouter API.")
        return True
    except Exception as e:
        logger.error(f"Ошибка подключения к OpenRouter API: {e}")
        return False
