from openai import AsyncOpenAI
from app.core.config import settings
from app.rag.search import search_chunks

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def ask_rag(db, user_id, question: str):

    chunks = await search_chunks(db, user_id, question, limit=5)

    context = "\n\n".join(
        f"[Chunk {c.chunk_index}]\n{c.content}"
        for c in chunks
    )

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. "
                    "Use ONLY the provided context. "
                    "If answer is not in context, say you don't know."
                )
            },
            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{question}
"""
            }
        ]
    )

    return response.choices[0].message.content