from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, func
from datetime import datetime

from sqlalchemy.orm import relationship, declarative_mixin
from pydantic.types import PositiveInt, NonNegativeInt

from app.core.db import Base

@declarative_mixin
class CommonMixin:
    full_amount: PositiveInt = Column(Integer, nullable=False)
    invested_amount: NonNegativeInt = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now, nullable=False)
    close_date = Column(DateTime, nullable=True, default=None)
