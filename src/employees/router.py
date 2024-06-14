from typing import Mapping

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.database import get_async_session
from src.dependencies import current_user
from src.employees import service
from src.employees.dependencies import valid_employee_id, authorized_user
from src.employees.models import Employee
from src.employees.schemas import EmployeeSchema, EmployeeNotFoundSchema, EmployeeAlreadyExistsSchema, \
    EmployeeAddSchema, EmployeeUpdateSchema
from src.schemas import EmployeeTasksSchema

router = APIRouter(
    prefix='/employees',
    tags=['employees']
)


@router.get(
    '',
    response_model=list[EmployeeSchema]
)
async def get_all_employees(session: AsyncSession = Depends(get_async_session)):
    employees = await service.get_all_employees(session)
    return employees


@router.get(
    '/busy',
    response_model=list[EmployeeTasksSchema]
)
async def get_busy_employees(session: AsyncSession = Depends(get_async_session)):
    employees = await service.get_busy_employees(session)
    return employees


@router.get(
    '/{employee_id}',
    response_model=EmployeeSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': EmployeeNotFoundSchema,
            'description': "Employee not found"
        }
    }
)
async def get_employee(employee: Employee = Depends(valid_employee_id)):
    return employee


@router.post(
    '',
    response_model=EmployeeSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            'model': EmployeeAlreadyExistsSchema,
            'description': "Employee already exists"
        }
    }
)
async def add_employee(employee: EmployeeAddSchema,
                       user: User = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    result = await service.add_employee(employee, user, session)
    return result


@router.patch(
    '/{employee_id}',
    response_model=EmployeeSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': EmployeeNotFoundSchema,
            'description': "Employee not found"
        }
    }
)
async def update_employee(update_data: EmployeeUpdateSchema,
                          employee: Employee = Depends(authorized_user),
                          session: AsyncSession = Depends(get_async_session)):
    result = await service.update_employee(employee, update_data, session)
    return result


@router.delete(
    '/{employee_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': EmployeeNotFoundSchema,
            'description': "Employee not found"
        }
    }
)
async def delete_employee(employee: Employee = Depends(authorized_user),
                          session: AsyncSession = Depends(get_async_session)):
    await service.delete_employee(employee, session)
