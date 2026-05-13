from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Document, Chunk
from app.rag.chunker import chunk_text
from app.rag.embedding import embed_many
from typing import List

async def store_document(
    db,
    user,
    title: str,
    raw_text: str,
    source: str = "sms"
):
    document = Document(
        user_id=user.id,
        title=title,
        source=source
    )

    db.add(document)
    await db.flush()
    chunks = chunk_text(raw_text)
    embeddings = await embed_many(chunks)
    for i, (content, embedding) in enumerate(zip(chunks, embeddings)):
        db.add(Chunk(
            user_id=user.id,
            document_id=document.id,
            chunk_index=i,
            content=content,
            embedding=embedding
        ))

    await db.commit()

    return document