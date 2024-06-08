from typing import Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy.orm import Mapped, relationship

from src.database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    employee_data: Mapped[Optional["EmployeeOrm"]] = relationship(back_populates="user_data")
