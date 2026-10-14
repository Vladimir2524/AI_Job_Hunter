import dotenv
from dotenv import load_dotenv
from groq import AsyncGroq
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

async def analyze_job(job_text: str):
    """
    Отправляем текст вакансии в LLMA и получаем вердикт.
    """

    # Наш профиль, чтобы ии знал с чем сравнить
    user_profile = """
    Роль: Junior / Junior+ Python Backend / Automation Developer
    Основной стек: Python 3, AsyncIO, FastAPI, aiogram 3, Telethon, PostgreSQL (asyncpg), SQLite, Git, Pytest.
    Навыки: Работа с REST API, Webhooks, JSON/CSV, ООП, асинхронный парсинг, интеграция LLM API, базовый Docker, Linux.
    Опыт: Есть 2 мощных завершенных проекта (SteamTrustFactor с 100% pytest покрытием и AI Job Hunter на асинхронном бэкенде).
    """

    prompt = f"""
    Ты — карьерый ментор и HR-эксперт. Оцени, подходит ли вакансия кандидату.
    Профиль кандидата: {user_profile}
    Текст вакансии: {job_text}
    
    ПРАВИЛА ОЦЕНКИ:
    1. Ставь "is_match": true, если вакансия на Python / Backend / Automation / Junior / Junior+ / Trainee, и основной стек совпадает с кандидатом (Python, AsyncIO, FastAPI, Postgres, API, Боты).
    2. НЕ бракуй вакансию, если там просят "1-2 года опыта", но стек наш. Для Джуна это норма.
    3. НЕ бракуй вакансию из-за отсутствия Docker/Redis/Linux — кандидат быстро подтянет это на практике.
    4. Ставь "is_match": false СТРОГО если: это Senior/Lead позиция (от 3+ лет опыта), абсолютно другой язык (C++, Java, PHP, Go), или непрограммистская вакансия (курьер, мануальный тестировщик, менеджер продаж).
    
    ответь СТРОГО в формате JSON:
    {{
        "is_match" : true/false,
        "reason": "короткое пояснение (1 предложение)",
        "tech_stack": ["список", "технологий"]
    }}
    """

    # Вызываем ИИ
    chat_completion = await client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="openai/gpt-oss-120b",  # или другая модель
        response_format={"type": "json_object"}  # Чтобы Groq выдал чистый JSON
    )

    # Достаем ответ
    response_text = chat_completion.choices[0].message.content

    # Защита
    try:
        return json.loads(response_text)
    except json.decoder.JSONDecodeError:
        return {
            "is_match": False,
            "reason": "Ошибка парсинга ответа от ИИ",
            "tech_stack": []
    }

if __name__ == "__main__":
    import asyncio

    # Тестовая вакансия для проверки
    test_job = """
    Ищем Junior Python разработчика!
    Требования: Python, AsyncIO, FastAPI, SQLite, понимание асинхронности.
    Задачи: писать ботов и скрипты автоматизации.
    ЗП: 70 000 руб.
    """

    async def main():
        print("🤖 Отправляем вакансию на анализ в Groq...")
        result = await analyze_job(test_job)
        print("\n✅ ОТВЕТ ОТ НЕЙРОСЕТИ:")
        print(result)
        print(f"Подходит? -> {result.get('is_match')}")
        print(f"Причина -> {result.get('reason')}")

    asyncio.run(main())