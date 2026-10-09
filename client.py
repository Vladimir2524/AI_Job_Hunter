from telethon import TelegramClient
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

client = TelegramClient("session_name", API_ID, API_HASH)

async def find_job():
    messages = await client.get_messages('@rabota_razrabotchikc', limit=5)

    for msg in messages:
        print(f'MessageFrom: {msg.id}'
            f', Data: {msg.date}'
            f', Text: {msg.text or "БЕЗ ТЕКСТА "[:100]}')

async def main():

    # start() сам всё разрулит: если надо - спросит, если уже залогинен - просто подключится
    await client.start()
    print("✅ Подключено!")

    await find_job()

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())