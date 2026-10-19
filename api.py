from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.db import Database

db = Database()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.close()

app = FastAPI(lifespan=lifespan)

@app.get("/jobs")
async def get_jobs():
    raw_jobs = await db.get_jobs()
    jobs_list = [dict(job) for job in raw_jobs]
    return jobs_list

