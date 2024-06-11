from typing import Mapping

from fastapi import APIRouter, Depends, status

from src.auth.models import User
from src.dependencies import current_user
from src.employees import service
from src.employees.dependencies import valid_employee_id, authorized_user
from src.employees.schemas import SEmployee, SEmployeeNotFound, SEmployeeAdd, SEmployeeUpdate, SEmployeeAlreadyExists
from src.schemas import SEmployeeTasks

router = APIRouter(
    prefix='/employees',
    tags=['employees']
)


@router.get(
    '',
    response_model=list[SEmployee]
)
async def get_all_employees():
    employees = await service.get_all_employees()
    return employees


@router.get(
    '/busy',
    response_model=list[SEmployeeTasks]
)
async def get_busy_employees():
    employees = await service.get_busy_employees()
    return employees


@router.get(
    '/{employee_id}',
    response_model=SEmployee,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': SEmployeeNotFound,
            'description': "Employee not found"
        }
    }
)
async def get_employee(employee: Mapping = Depends(valid_employee_id)):
    return employee


@router.post(
    '',
    response_model=SEmployee,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'model': SEmployeeAlreadyExists,
            'description': "Employee already exists"
        }
    }
)
async def add_employee(employee: SEmployeeAdd, user: User = Depends(current_user)):
    result = await service.add_employee(employee, user)
    return result


@router.patch(
    '/{employee_id}',
    response_model=SEmployee,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': SEmployeeNotFound,
            'description': "Employee not found"
        }
    }
)
async def update_employee(update_data: SEmployeeUpdate, employee: Mapping = Depends(authorized_user)):
    result = await service.update_employee(employee, update_data)
    return result


@router.delete(
    '/{employee_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': SEmployeeNotFound,
            'description': "Employee not found"
        }
    }
)
async def delete_employee(employee: Mapping = Depends(authorized_user)):
    await service.delete_employee(employee)
