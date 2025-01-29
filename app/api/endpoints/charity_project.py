from datetime import datetime
# Импортируем класс HTTPException.
from fastapi import APIRouter, Depends, HTTPException
# Импортируем класс асинхронной сессии для аннотации параметра.
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_charity_project_in_work,
                                check_charity_project_name_duplicate, check_charity_project_closed)
# Импортируем асинхронный генератор сессий.
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectBase,
                                         CharityProjectCreate,
                                         CharityProjectDB, CharityProjectUpdate)
from app.services.investment import investing_magic

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB]
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    charity_projects = await charity_project_crud.get_multi(session=session)
    return charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_charity_project_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await investing_magic(session)
    await session.refresh(new_project)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def delete_crarity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_in_work(project_id, session)
    charity_project = await charity_project_crud.remove(charity_project, session)
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_charity_project_name_duplicate(obj_in.name, session)
    charity_project = await check_charity_project_closed(project_id, session)
    print(charity_project.__dict__)

    if obj_in.full_amount is not None:
        if obj_in.full_amount < charity_project.invested_amount:
            raise HTTPException(
                status_code=422,
                detail=f'Нельзя уменьшить сумму проекта ниже {charity_project.invested_amount}'
            )
        if obj_in.full_amount == charity_project.invested_amount:
            charity_project.fully_invested = True
            charity_project.close_date = datetime.now()
    
    charity_project = await charity_project_crud.update(charity_project, obj_in, session)
    await investing_magic(session)
    await session.refresh(charity_project)

    return charity_project
