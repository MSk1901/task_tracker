from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.database import get_async_session
from src.dependencies import current_user
from src.employees import service
from src.employees.exceptions import EmployeeNotFound, UserNotAuthorized
from src.employees.models import Employee


async def valid_employee_id(employee_id: int,
                            session: AsyncSession = Depends(get_async_session)) -> Employee:
    employee = await service.get_employee_by_id(employee_id, session)
    if not employee:
        raise EmployeeNotFound()

    return employee


async def authorized_user(employee: Employee = Depends(valid_employee_id),
                          user: User = Depends(current_user)) -> Employee:
    if employee.user_id != user.id:
        raise UserNotAuthorized()

    return employee
