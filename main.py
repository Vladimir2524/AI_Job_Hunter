import asyncio

from client import find_job
from database.db import Database


async def main():
    try:
        db = Database()
        await db.connect()
        await db.init_db()

        print("Запускаем парсер..")
        await find_job(db)


    except Exception as e:
        print(f'Ошибка в работе приложения: {e}')


    finally:
        print('Закрываем соеденение с бд...')
        await db.close()
        print('Работа завершена 👋')

asyncio.run(main())

