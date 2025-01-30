from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.types import NonNegativeInt, PositiveInt

CREATE_DATE = (datetime.now()).isoformat(timespec='seconds')


class DonationBase(BaseModel):

    id: int
    comment: Optional[str]
    full_amount: PositiveInt
    create_date: datetime = Field(default=CREATE_DATE)


class DonationCreate(BaseModel):

    full_amount: PositiveInt
    comment: Optional[str]


class DonationAll(DonationBase):

    invested_amount: NonNegativeInt = Field(default=0)
    fully_invested: bool = Field(default=False)
    user_id: int
    close_date: Optional[datetime]


class DonationDB(DonationBase):

    class Config:
        orm_mode = True


class DonationDBAll(DonationBase):

    invested_amount: NonNegativeInt = Field(default=0)
    fully_invested: bool = Field(default=False)
    user_id: int
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
