from fastapi import FastAPI
from app.api.webhooks import router as webhook_router
from app.core.database import Base, engine


app = FastAPI(title="asklinq", version="1.0.0")

app.include_router(webhook_router, prefix="/webhook")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "API is running"}