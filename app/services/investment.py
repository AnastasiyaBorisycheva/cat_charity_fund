from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def get_open_project_donation(session: AsyncSession):

    opened_projects = await session.execute(
        select(CharityProject).where(CharityProject.fully_invested == 0)
    )
    opened_project = opened_projects.scalars().first()

    opened_donations = await session.execute(
        select(Donation).where(Donation.fully_invested == 0)
    )
    opened_donation = opened_donations.scalars().first()

    return opened_project, opened_donation


async def investing_magic(
        session: AsyncSession
):
    opened_project, opened_donation = await get_open_project_donation(session)

    while opened_project is not None and opened_donation is not None:
        delta_project = (
            opened_project.full_amount - opened_project.invested_amount
        )
        delta_donation = (
            opened_donation.full_amount - opened_donation.invested_amount
        )

        if delta_project > delta_donation:
            common_delta = delta_donation
        else:
            common_delta = delta_project

        new_project_amount = (
            opened_project.invested_amount + common_delta
        )

        new_donation_amount = (
            opened_donation.invested_amount + common_delta
        )

        setattr(opened_project, 'invested_amount', new_project_amount)
        setattr(opened_donation, 'invested_amount', new_donation_amount)

        if opened_project.invested_amount == opened_project.full_amount:
            setattr(opened_project, 'fully_invested', True)
            setattr(opened_project, 'close_date', datetime.now())

        if opened_donation.invested_amount == opened_donation.full_amount:
            setattr(opened_donation, 'fully_invested', True)
            setattr(opened_donation, 'close_date', datetime.now())

        session.add(opened_project)
        session.add(opened_donation)

        await session.commit()

        await session.refresh(opened_project)
        await session.refresh(opened_donation)

        opened_project, opened_donation = await get_open_project_donation(
            session)

    return 'Investment Done'
