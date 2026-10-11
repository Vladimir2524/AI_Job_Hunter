from telethon import TelegramClient
import os
import asyncio
from dotenv import load_dotenv
from analyzer import analyze_job

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

client = TelegramClient("session_name", API_ID, API_HASH)

async def find_job():
    print("Загружаем посты из Telegram...")
    messages = await client.get_messages('@rabota_razrabotchikc', limit=5)

    for msg in messages:
        job_text = msg.text or ""

        if len(job_text) < 30:
            continue

        print(f'\n Обрабатываем пост ID {msg.id}...')

        result = await analyze_job(job_text)

        if result.get("is_match") is True:
            print("Найдена подходящая вакансия!")
            print(f"Причина: {result.get('reason')}")
            print(f"Стек: {result.get('tech_stack')}")
        else:
            print(f'Не подходит: {result.get("reason")}')

        await asyncio.sleep(1)


async def main():

    # start() сам всё разрулит: если надо - спросит, если уже залогинен - просто подключится
    await client.start()
    print("✅ Телеграм подключен!")

    await find_job()

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())