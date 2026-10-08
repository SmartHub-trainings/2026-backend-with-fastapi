from db_config import Base
from sqlalchemy import Integer, String, DateTime, Boolean, func
from sqlalchemy.orm import Mapped,mapped_column
from datetime import datetime


class User(Base):
    __tablename__="users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name:Mapped[str]=mapped_column(String(20),nullable=False)
    last_name:Mapped[str]=mapped_column(String(20),nullable=False)
    email:Mapped[str]=mapped_column(String(20),nullable=False,unique=True)
    age:Mapped[int]=mapped_column(Integer)
    password:Mapped[str]=mapped_column(String(60),nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now)
    is_verified:Mapped[bool]=mapped_column(Boolean,default=False)
