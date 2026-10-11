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
    Стек : Python, AsyncIO, aiogram 3, Telethon, SQlite, FastApi.
    Цель: Junior Python Developer
    """

    prompt = f"""
    Ты - HR-ассистент. Проанализируй вакансию и ответь, подходит ли она кандидату.
    Профиль кандидата: {user_profile}
    Текст вакансии: {job_text}
    
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