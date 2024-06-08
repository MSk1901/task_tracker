from typing import Mapping

from fastapi import Depends

from src.auth.models import User
from src.dependencies import current_user
from src.employees import service
from src.employees.exceptions import EmployeeNotFound, UserNotAuthorized


async def valid_employee_id(employee_id: int) -> Mapping:
    employee = await service.get_employee_by_id(employee_id)
    if not employee:
        raise EmployeeNotFound()

    return employee


async def authorized_user(employee: Mapping = Depends(valid_employee_id),
                          user: User = Depends(current_user)) -> Mapping:
    if employee.user_id != user.id:
        raise UserNotAuthorized()

    return employee
