from fastapi import FastAPI
from app.api.webhooks import router as webhook_router

app = FastAPI(title="asklinq", version="1.0.0")

app.include_router(webhook_router, prefix="/webhook")

@app.get("/")
async def root():
    return {"message": "API is running"}