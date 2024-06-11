import enum
from datetime import datetime
from typing import Optional, List

from sqlalchemy import Integer, String, ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base
from src.employees.models import EmployeeOrm


class StatusEnum(enum.Enum):
    created = 'создана'
    in_process = 'в процессе'
    finished = 'завершена'


class TaskOrm(Base):
    __tablename__ = 'task'

    id = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]]
    status: Mapped[StatusEnum] = mapped_column(default=StatusEnum.created)
    employee_id: Mapped[Optional[int]] = mapped_column(ForeignKey("employee.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now())
    deadline: Mapped[datetime]
    parent_task_id: Mapped[Optional[int]] = mapped_column(ForeignKey('task.id'))
    parent_task: Mapped[Optional['TaskOrm']] = relationship("TaskOrm", remote_side=[id],
                                                            back_populates="sub_tasks")
    sub_tasks: Mapped[List['TaskOrm']] = relationship("TaskOrm", back_populates="parent_task",
                                                      cascade="all, delete-orphan")
