import re
from collections import Counter
from typing import Optional

from models import Post
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import and_

from pydantic_models import PaginatedResponse, PostOut


def count_words(text: str) -> dict:
    words = re.findall(r"\w+", text.lower())
    return dict(Counter(words))


async def process_posts(
    session: AsyncSession,
    category: Optional[str] = None,
    keywords: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
) -> PaginatedResponse:
    filters = []

    if category:
        filters.append(Post.category == category)
    if keywords:
        for word in keywords.lower().split():
            filters.append(Post.content.ilike(f"%{word}%"))

    base_query = select(Post).where(and_(*filters)) if filters else select(Post)
    total_query = select(func.count()).select_from(base_query.subquery())

    total_result = await session.execute(total_query)
    total = total_result.scalar()

    result = await session.execute(base_query.limit(limit).offset(offset))
    posts = result.scalars()

    processed = []
    for post in posts:
        word_freq = count_words(post.content)
        processed.append(PostOut(id=post.id, category=post.category, word_freq=word_freq))

    return PaginatedResponse(total=total, posts=processed)

