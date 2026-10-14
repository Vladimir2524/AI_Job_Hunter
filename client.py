from turtledemo.paint import changecolor

from telethon import TelegramClient
import os
import asyncio
from dotenv import load_dotenv
from analyzer import analyze_job
import asyncpg
from database.db import Database
from aiogram import Bot


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MY_TELEGRAM_ID = int(os.getenv("MY_TELEGRAM_ID"))
bot = Bot(token=BOT_TOKEN)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

db = Database()
client = TelegramClient("session_name", API_ID, API_HASH)

CHANNELS = [
    'rabota_razrabotchikn',
    'python_jobs',
    'rabota_razrabotchikc',
    'rabotaw_razrabotchik'
    'backend_jobs_feed',
    'python_job_feed',
    'tproger_itjobs',
]

async def find_job():
    """
    Если уже в базе — пропускаем
    Если новый — анализируем в Groq и сохраняем в Postgres

    """
    print("Загружаем посты из Telegram...")
    for channel in CHANNELS:
        print(f"\n📡 Сканируем канал: {channel}")
        await client.get_messages(channel)

        messages = await client.get_messages(channel, limit=5)
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

                clean_channel = channel.replace("@", "")
                post_url = f"https://t.me/{clean_channel}/{msg.id}"

                text = f"🔥 **НАЙДЕНА ВАКАНСИЯ!**\n\n**Причина:** {result.get('reason')}\n**Стек:** {result.get('tech_stack')}\n\n🔗 [Ссылка на пост]({post_url})"
                await bot.send_message(chat_id=MY_TELEGRAM_ID, text=text, parse_mode="Markdown")

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