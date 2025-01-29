# app/crud/meeting_room.py
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.crud.base import CRUDBase
from app.models import Donation, User


# Создаем новый класс, унаследованный от CRUDBase.
class CRUDDonation(CRUDBase):
    async def get_by_user(
        self,
        user: User,
        session: AsyncSession
    ) -> list[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)