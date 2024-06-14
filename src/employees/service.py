from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload

from src.auth.models import User
from sqlalchemy import insert, select, update, delete, func, desc

from src.employees.exceptions import EmployeeAlreadyExists
from src.employees.models import Employee
from src.employees.schemas import EmployeeAddSchema, EmployeeUpdateSchema
from src.tasks.models import Task, StatusEnum


async def get_all_employees(session: AsyncSession):
    employees = await session.scalars(select(Employee))
    return employees


async def get_employee_by_id(employee_id: int,
                             session: AsyncSession):
    employee = await session.get(Employee, employee_id)
    return employee


async def add_employee(employee: EmployeeAddSchema,
                       user: User,
                       session: AsyncSession):
    existing_employee = await session.scalars(
        select(Employee).where(Employee.user_id == user.id)
    )
    if existing_employee.first():
        detail = 'User already has a registered employee'
        raise EmployeeAlreadyExists(detail)

    employee_data = employee.model_dump()
    employee_data['user_id'] = user.id
    try:
        result = await session.scalars(insert(Employee).
                                       values(**employee_data).
                                       returning(Employee))
        created_employee = result.first()
        await session.commit()
        return created_employee
    except IntegrityError:
        detail = 'Employee with this phone number already exists'
        await session.rollback()
        raise EmployeeAlreadyExists(detail)


async def update_employee(employee: Employee,
                          update_data: EmployeeUpdateSchema,
                          session: AsyncSession):
    update_dict = update_data.model_dump(exclude_unset=True)
    try:
        result = await session.scalars(
            update(Employee)
            .where(Employee.id == employee.id)
            .values(**update_dict)
            .returning(Employee)
        )
        updated_employee = result.first()
        await session.commit()
        return updated_employee
    except IntegrityError:
        detail = 'Employee with this phone number already exists'
        await session.rollback()
        raise EmployeeAlreadyExists(detail)


async def delete_employee(employee: Employee,
                          session: AsyncSession):
    stmt = delete(Employee).where(Employee.id == employee.id)
    await session.execute(stmt)
    await session.commit()


async def get_busy_employees(session: AsyncSession):
    active_tasks = aliased(Task)
    query = (
        select(Employee, func.count(Employee.tasks).label('active_task_count'))
        .outerjoin(active_tasks,
                   (Employee.id == active_tasks.employee_id) &
                   (active_tasks.status == StatusEnum.in_process))
        .group_by(Employee.id)
        .order_by(desc('active_task_count'))
        .options(joinedload(Employee.tasks))
    )
    result = await session.execute(query)
    return result.unique().scalars()


async def get_least_busy_employee(session: AsyncSession):
    active_tasks = aliased(Task)
    query = (
        select(Employee, func.count(active_tasks.id).label('active_task_count'))
        .outerjoin(active_tasks,
                   (Employee.id == active_tasks.employee_id) &
                   (active_tasks.status == StatusEnum.in_process))
        .group_by(Employee.id)
        .order_by('active_task_count')
        .limit(1)
    )
    result = await session.execute(query)
    return result.scalar()


async def get_employee_for_parent_task(parent_task_id: int,
                                       session: AsyncSession):
    query = (
        select(Employee)
        .join(Task, Task.employee_id == Employee.id)
        .where(Task.id == parent_task_id)
    )
    result = await session.execute(query)
    return result.scalar()
