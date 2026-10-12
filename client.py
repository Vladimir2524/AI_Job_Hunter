from telethon import TelegramClient
import os
import asyncio
from dotenv import load_dotenv
from analyzer import analyze_job
import asyncpg
from database.db import Database



load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

db = Database()
client = TelegramClient("session_name", API_ID, API_HASH)


async def find_job():
    """
    Если уже в базе — пропускаем
    Если новый — анализируем в Groq и сохраняем в Postgres

    """
    print("Загружаем посты из Telegram...")
    messages = await client.get_messages('@rabota_razrabotchikc', limit=5)

    for msg in messages:
        job_text = msg.text or ""

        if await db.is_job_processed(msg.id):
            print(f"⏩ Пост {msg.id} уже был обработан, пропускаем.")
            continue

        if len(job_text) < 30:
            continue

        print(f'\n Обрабатываем пост ID {msg.id}...')

        result = await analyze_job(job_text)
        await db.add_processed_job(msg.id)

        if result.get("is_match") is True:
            print("Найдена подходящая вакансия!")
            print(f"Причина: {result.get('reason')}")
            print(f"Стек: {result.get('tech_stack')}")
        else:
            print(f'Не подходит: {result.get("reason")}')

        await asyncio.sleep(1)


async def main():

    """
    start() сам всё разрулит: если надо - спросит, если уже залогинен - просто подключится
    СХЕМА :
    1. Подключаемся к Postgres и создаем таблицу
    2. Запускаем Телеграм
    3. Выполняем поиск
    4. Отключаем базу и телеграм
    """

    await client.start()
    print("✅ Телеграм подключен!")

    await db.connect()
    await db.init_db()

    await client.start()

    await find_job()

    await client.disconnect()
    await db.close()

if __name__ == "__main__":
    asyncio.run(main())