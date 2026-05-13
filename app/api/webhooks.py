from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
import io
from pypdf import PdfReader
from app.core.config import settings
from app.core.database import get_db
from app.users.service import get_or_create_user
from app.rag.ask import ask_rag
from app.rag.store import store_document

router = APIRouter()
LINQ_API_KEY = settings.LINQ_API_KEY
LINQ_BASE_URL = "https://api.linqapp.com"
FROM_NUMBER = settings.LINQ_FROM_NUMBER

async def add_reaction(message_id: str, reaction: str = "like"):
    url = f"{LINQ_BASE_URL}/api/partner/v3/messages/{message_id}/reactions"

    payload = {
        "type": reaction,
        "operation": "add"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers={
                "Authorization": f"Bearer {LINQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload
        )

async def send_message(to_number: str, text: str):
    url = "https://api.linqapp.com/api/partner/v3/chats"

    payload = {
        "from": FROM_NUMBER,
        "to": [to_number],
        "message": {
            "parts": [{"type": "text", "value": text}]
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            headers={
                "Authorization": f"Bearer {LINQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload
        )


async def load_pdf_from_url(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    pdf_file = io.BytesIO(response.content)
    reader = PdfReader(pdf_file)

    return "\n".join(page.extract_text() or "" for page in reader.pages)

@router.post("/linq")
async def linq_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):

    data = await request.json()
    message_id = data.get("data", {}).get("id")
    phone = (
        data.get("from")
        or data.get("data", {}).get("sender_handle", {}).get("handle")
    )

    if not phone:
        return {"status": "ignored"}

    user = await get_or_create_user(db, phone)

    parts = data.get("data", {}).get("parts", [])

    file_url = None
    filename = None
    mime_type = None
    text = None

    for part in parts:
        if part.get("type") == "media":
            file_url = part.get("url")
            filename = part.get("filename")
            mime_type = part.get("mime_type")

        if part.get("type") == "text":
            text = part.get("value")

    if file_url:

        try:
            if mime_type == "application/pdf":
                content = await load_pdf_from_url(file_url)
            else:
                return {"status": "unsupported"}

            doc = await store_document(
                db=db,
                user=user,
                title=filename or "Uploaded file",
                raw_text=content,
                source="file"
            )
            if message_id:
                await add_reaction(message_id, "like")
            else:
                await send_message(phone, "File uploaded and processed successfully.")

            return {"status": "processed"}

        except Exception as e:
            return {"status": "error"}

    if text:
        try:
            answer = await ask_rag(
                db=db,
                user_id=user.id,
                question=text
            )

            await send_message(phone, answer)

            return {"status": "sent"}

        except Exception as e:
            await send_message(phone, "Error generating response")
            return {"status": "error"}

    return {"status": "ignored"}