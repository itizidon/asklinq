from pgvector.sqlalchemy import Vector
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Chunk
from app.rag.embedding import embed_text
from typing import List
import uuid

async def search_chunks(
    db: AsyncSession,
    user_id: uuid.UUID,
    query: str,
    limit: int = 5
) -> List[Chunk]:

    query_embedding = await embed_text(query)

    stmt = (
        select(Chunk)
        .where(Chunk.user_id == user_id)
        .order_by(Chunk.embedding.cosine_distance(query_embedding))
        .limit(limit)
    )

    result = await db.execute(stmt)

    return result.scalars().all()