from typing import Optional
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud

from app.models import Donation, CharityProject


async def investing_magic(
        session: AsyncSession   
):
    print('This is investment magic')
    opened_projects = await session.execute(
        select(CharityProject).where(CharityProject.fully_invested == 0)
    )

    opened_project = opened_projects.scalars().first()

    opened_donations = await session.execute(
        select(Donation).where(Donation.fully_invested == 0)
    )

    opened_donation = opened_donations.scalars().first()

    while opened_project is not None and opened_donation is not None:
        delta_project = opened_project.full_amount - opened_project.invested_amount
        delta_donation = opened_donation.full_amount - opened_donation.invested_amount

        if delta_project > delta_donation:
            new_project_invested_amount = opened_project.invested_amount + delta_donation
            setattr(opened_project, 'invested_amount', new_project_invested_amount)

            new_donation_invested_amount = opened_donation.invested_amount + delta_donation
            setattr(opened_donation, 'invested_amount', new_donation_invested_amount)

        elif delta_project <= delta_donation:
            new_project_invested_amount = opened_project.invested_amount + delta_project
            setattr(opened_project, 'invested_amount', new_project_invested_amount)

            new_donation_invested_amount = opened_donation.invested_amount + delta_project
            setattr(opened_donation, 'invested_amount', new_donation_invested_amount)

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

        opened_projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested == 0)
        )

        opened_project = opened_projects.scalars().first()

        opened_donations = await session.execute(
            select(Donation).where(Donation.fully_invested == 0)
        )

        opened_donation = opened_donations.scalars().first()

        # session.add(opened_project)
        # session.add(opened_donation)


        # await session.commit()

        # await session.refresh(opened_project)
        # await session.refresh(opened_donation)


    return 'Magic'