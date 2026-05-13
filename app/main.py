from fastapi import FastAPI
from app.api.webhooks import router as webhook_router
from app.core.database import Base, engine
from sqlalchemy import text


app = FastAPI(title="asklinq", version="1.0.0")

app.include_router(webhook_router, prefix="/webhook")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "API is running"}