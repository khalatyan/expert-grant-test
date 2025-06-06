import asyncio
import os

from sqlalchemy import Column, Integer, String, select, func, text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost/postsdb"
)

engine = create_async_engine(DATABASE_URL, echo=False)

Base = declarative_base()
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    content = Column(String)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        sample_posts = [
            Post(category="tech", content="FastAPI is a modern web framework."),
            Post(category="tech", content="Python and asyncio are powerful."),
            Post(category="life", content="Life is beautiful and unpredictable."),
            Post(category="tech", content="Python is great for backend development."),
        ]
        # await conn.execute(text("DELETE FROM posts"))  # Очистка
        await conn.execute(Post.__table__.insert(), [p.__dict__ for p in sample_posts])