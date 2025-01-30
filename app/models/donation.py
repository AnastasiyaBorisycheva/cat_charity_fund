from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base

from .base_model import CommonMixin


class Donation(CommonMixin, Base):

    user_id = user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
