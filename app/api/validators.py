from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_charity_project_name_duplicate(
        charity_project_name: str,
        session: AsyncSession,
) -> None:
    charity_project_id = await charity_project_crud.get_by_attribute(
        'name',
        charity_project_name,
        session)
    if charity_project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(
        charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_in_work(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await check_charity_project_exists(
        charity_project_id, session)
    if charity_project.invested_amount > 0 or charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект уже инвестированы средства'
        )
    return charity_project


async def check_charity_project_closed(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await check_charity_project_exists(
        charity_project_id, session)
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект закрыт'
        )
    return charity_project
