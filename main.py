import asyncio

from typing import Optional

from fastapi import FastAPI, Query
from sqlalchemy.ext.asyncio import async_sessionmaker

from models import engine, init_db
from pydantic_models import PaginatedResponse
from utils import process_posts

async_session = async_sessionmaker(engine, expire_on_commit=False)
app = FastAPI()


@app.get("/posts", response_model=PaginatedResponse)
async def get_posts(
    category: Optional[str] = None,
    keywords: Optional[str] = Query(None, description="Пробел-разделённые ключевые слова"),
    limit: int = 10,
    offset: int = 0,
):
    async with async_session() as session:
        return await process_posts(session, category, keywords, limit, offset)

if __name__ == "__main__":
    asyncio.run(init_db())