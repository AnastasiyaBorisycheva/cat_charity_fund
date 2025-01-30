from datetime import datetime

from pydantic.types import NonNegativeInt, PositiveInt
from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class CommonMixin:
    full_amount: PositiveInt = Column(Integer, nullable=False)
    invested_amount: NonNegativeInt = Column(
        Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    close_date = Column(DateTime, nullable=True, default=None)
