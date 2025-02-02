from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationDBAll
from app.services.investment import investing_magic

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDBAll],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    '/my',
    response_model=list[DonationDB],
    dependencies=[Depends(current_user)],
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donations = await donation_crud.get_by_user(user, session)

    return donations


@router.post(
    '/',
    response_model=DonationDB,
    dependencies=[Depends(current_user)]
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    donation = await donation_crud.create(donation, session, user)

    await investing_magic(session)
    await session.refresh(donation)

    return donation
