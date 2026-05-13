from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User
import uuid

async def get_or_create_user(db: AsyncSession, phone_number: str):

    result = await db.execute(
        select(User).where(User.phone_number == phone_number)
    )

    user = result.scalar_one_or_none()

    if user:
        return user

    user = User(
        id=uuid.uuid4(),
        phone_number=phone_number
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user