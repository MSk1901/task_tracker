from datetime import date
from typing import Optional, List

from fastapi_users_db_sqlalchemy import UUID_ID
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base


class Employee(Base):
    __tablename__ = 'employee'

    id = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    fathers_name: Mapped[Optional[str]] = mapped_column(String(50))
    dob: Mapped[date]
    user_id: Mapped[UUID_ID] = mapped_column(ForeignKey("user.id"))
    user_data: Mapped[Optional['User']] = relationship(back_populates="employee_data")
    phone: Mapped[Optional[str]] = mapped_column(unique=True)
    position: Mapped[str] = mapped_column(String(100))
    tasks: Mapped[List['Task']] = relationship()
