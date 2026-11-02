from telethon import TelegramClient
import os
import asyncio
from dotenv import load_dotenv
from analyzer import analyze_job
import asyncpg
from database.db import Database
from aiogram import Bot
from config import CHANNELS
from rich.console import Console
from rich.panel import Panel


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MY_TELEGRAM_ID = int(os.getenv("MY_TELEGRAM_ID"))
bot = Bot(token=BOT_TOKEN)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

client = TelegramClient("session_name", API_ID, API_HASH)

console = Console()

async def find_job(db):
    """
        Если уже в базе — пропускаем
        Если новый — анализируем в Groq и сохраняем в Postgres
    """

    async with client:
        print("Загружаем посты из Telegram...")
        for channel in CHANNELS:
            try:
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
                        console.print('[bold green]Ура![/bold green]Вакансия найдена!')
                        console.print(Panel(job_text, title='Junior Python', border_style='green'))


                        clean_channel = channel.replace("@", "")
                        post_url = f"https://t.me/{clean_channel}/{msg.id}"

                        text = f"🔥 **НАЙДЕНА ВАКАНСИЯ!**\n\n**Причина:** {result.get('reason')}\n**Стек:** {result.get('tech_stack')}\n\n🔗 [Ссылка на пост]({post_url})"
                        await bot.send_message(chat_id=MY_TELEGRAM_ID, text=text, parse_mode="Markdown")

                    else:
                        console.print(f"[bold red]❌ Не подходит:[/bold red] {result.get('reason')}")

                    await asyncio.sleep(1)

            except ValueError:
                print("Канал не найден или не существует, пропускаем..")
                continue

            except Exception as e:
                print(f"Ошибка при работе с каналом {channel}: {e}")
                continue


async def main():
    db = Database()
    await db.connect()
    await db.init_db()

    try:
        await find_job(db)

    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())