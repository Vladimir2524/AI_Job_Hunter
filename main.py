from analyzer import analyze_job
import asyncio


async def main():
    job_text = "Текст вакансии..."

    # ТЕПЕРЬ МОЖНО: мы внутри async def!
    analysis = await analyze_job(job_text)
    print(analysis)


if __name__ == "__main__":
    asyncio.run(main())

