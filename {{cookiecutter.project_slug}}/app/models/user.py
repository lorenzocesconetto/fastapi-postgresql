from app.db.base import ORMBase
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship


class User(ORMBase):
    id = Column(Integer, primary_key=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    items = relationship("Item", back_populates="owner")
