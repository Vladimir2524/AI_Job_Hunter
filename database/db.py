import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

class Database:

    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
        self.conn = None

    async def connect(self):
        self.conn = await asyncpg.connect(self.db_url)

    async def close(self):
        if self.conn:
            await self.conn.close()

    async def init_db(self):
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS channels (
                id SERIAL PRIMARY KEY,
                message_id BIGINT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

    """
    У ASYNCPG НЕТУ COMMIT() она автосохранение делает.
    Кстати, у меня была ошибка с запятой вот тут - created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, потому что :
    Когда база видит запятую, она ожидает, что сейчас пойдет описание следующей колонки.
    А видит закрывающую скобку ). Отсюда и крик о помощи syntax error at or near ")"
    """


    async def is_job_processed(self, message_id: int) -> bool:
        row = await self.conn.fetchrow("""SELECT message_id FROM channels WHERE message_id = $1""", message_id)
        return row is not None

    async def add_processed_job(self, message_id: int):
        await self.conn.execute(
            "INSERT INTO channels (message_id) VALUES ($1) ON CONFLICT DO NOTHING",
            message_id,
        )

    async def get_jobs(self):
        sql = "SELECT id, message_id, created_at FROM channels ORDER BY id DESC LIMIT 50;"
        return await self.conn.fetch(sql)

