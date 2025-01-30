from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator
from pydantic.types import NonNegativeInt, PositiveInt

CREATE_DATE = (datetime.now()).isoformat(timespec='seconds')


class CharityProjectBase(BaseModel):

    id: int
    name: str = Field(None, min_length=1, max_length=100)
    description: str = Field(None, min_length=1)
    full_amount: PositiveInt
    invested_amount: NonNegativeInt = Field(default=0)
    fully_invested: bool = Field(default=False)
    create_date: datetime = Field(default=CREATE_DATE)
    close_date: Optional[datetime]


class CharityProjectCreate(BaseModel):
    name: str = Field(None, min_length=1, max_length=100)
    description: str = Field(None, min_length=1)
    full_amount: PositiveInt

    @validator('name', 'description', pre=True, always=True)
    def name_cant_be_null(cls, value: str):
        if value is None:
            raise ValueError('Имя или описание не может быть Null')
        return value


class CharityProjectUpdate(BaseModel):

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = 'forbid'


class CharityProjectDB(CharityProjectBase):

    class Config:
        orm_mode = True
