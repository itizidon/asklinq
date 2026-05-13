from openai import AsyncOpenAI
from app.core.config import settings
from typing import List

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def embed_text(text: str) -> List[float]:
    response = await client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

async def embed_many(texts: List[str]) -> List[List[float]]:
    response = await client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [item.embedding for item in response.data]