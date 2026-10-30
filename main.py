from analyzer import analyze_job
import asyncio


async def main():
    job_text = "Текст вакансии..."

    # ТЕПЕРЬ МОЖНО: мы внутри async def!
    analysis = await analyze_job(job_text)
    print(analysis)


if __name__ == "__main__":
    asyncio.run(main())

"""
                  ┌────────────────────┐
                  │   user_profile.py  │  (Твой стек, стоп-слова)
                  └─────────┬──────────┘
                            │ (Импорт данных)
                            ▼
┌─────────────┐   Текст   ┌────────────────────┐   JSON   ┌─────────────┐
│  client.py  ├──────────►│    analyzer.py     ├─────────►│    db.py    │
│ (Telethon)  │  вакансии │ (Groq + LLaMA 3)   │  оценка  │ (PostgreSQL)│
└──────┬──────┘           └────────────────────┘          └──────▲──────┘
       │                                                         │
       └────────────────── Запуск и Пул БД ──────────────────────┘
                                  │
                       ┌──────────┴──────────┐
                       │       main.py       │  (Дирижер завода)
                       └─────────────────────┘
"""
