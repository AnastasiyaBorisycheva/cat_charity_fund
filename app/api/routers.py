# app/api/routers.py
from fastapi import APIRouter

# from app.api.endpoints.meeting_room import router as meeting_room_router
# from app.api.endpoints.reservation import router as reservation_router
# Две длинных строчки импортов заменяем на одну короткую.
from app.api.endpoints import user_router, charity_project_router, donation_router

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(charity_project_router, prefix='/charity_project', tags=['Charity_Projects'])
main_router.include_router(donation_router, prefix='/donation', tags=['Donations'])