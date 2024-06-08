from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import aliased, joinedload

from src.auth.models import User
from src.database import get_async_session
from sqlalchemy import insert, select, update, delete, func, desc

from src.employees.exceptions import EmployeeAlreadyExists
from src.employees.models import EmployeeOrm
from src.employees.schemas import SEmployeeAdd, SEmployeeUpdate
from src.tasks.models import TaskOrm, StatusEnum
from src.tasks.service import get_important_tasks


async def get_all_employees():
    async for session in get_async_session():
        employees = await session.scalars(select(EmployeeOrm))
        return employees


async def get_employee_by_id(employee_id: int):
    async for session in get_async_session():
        employee = await session.get(EmployeeOrm, employee_id)
        return employee


async def add_employee(employee: SEmployeeAdd, user: User):
    async for session in get_async_session():
        existing_employee = await session.scalars(
            select(EmployeeOrm).where(EmployeeOrm.user_id == user.id)
        )
        if existing_employee.first():
            detail = 'User already has a registered employee'
            raise EmployeeAlreadyExists(detail)

        employee_data = employee.dict()
        employee_data['user_id'] = user.id
        try:
            result = await session.scalars(insert(EmployeeOrm).
                                           values(**employee_data).
                                           returning(EmployeeOrm))
            created_employee = result.first()
            await session.commit()
            return created_employee
        except IntegrityError:
            detail = 'Employee with this phone number already exists'
            await session.rollback()
            raise EmployeeAlreadyExists(detail)


async def update_employee(employee, update_data: SEmployeeUpdate):
    async for session in get_async_session():
        update_dict = update_data.dict(exclude_unset=True)
        try:
            result = await session.scalars(
                update(EmployeeOrm)
                .where(EmployeeOrm.id == employee.id)
                .values(**update_dict)
                .returning(EmployeeOrm)
            )
            updated_employee = result.first()
            await session.commit()
            return updated_employee
        except IntegrityError:
            detail = 'Employee with this phone number already exists'
            await session.rollback()
            raise EmployeeAlreadyExists(detail)


async def delete_employee(employee):
    async for session in get_async_session():
        stmt = delete(EmployeeOrm).where(EmployeeOrm.id == employee.id)
        await session.execute(stmt)
        await session.commit()


async def get_busy_employees():
    async for session in get_async_session():
        active_tasks = aliased(TaskOrm)
        query = (
            select(EmployeeOrm, func.count(EmployeeOrm.tasks).label('active_task_count'))
            .outerjoin(active_tasks,
                       (EmployeeOrm.id == active_tasks.employee_id) &
                       (active_tasks.status == StatusEnum.in_process))
            .group_by(EmployeeOrm.id)
            .order_by(desc('active_task_count'))
            .options(joinedload(EmployeeOrm.tasks))
        )
        result = await session.execute(query)
        return result.unique().scalars()


async def get_least_busy_employee():
    async for session in get_async_session():
        active_tasks = aliased(TaskOrm)
        query = (
            select(EmployeeOrm, func.count(active_tasks.id).label('active_task_count'))
            .outerjoin(active_tasks,
                       (EmployeeOrm.id == active_tasks.employee_id) &
                       (active_tasks.status == StatusEnum.in_process))
            .group_by(EmployeeOrm.id)
            .order_by('active_task_count')
            .limit(1)
        )
        result = await session.execute(query)
        return result.scalar()


async def get_employee_for_parent_task(parent_task_id: int):
    async for session in get_async_session():
        query = (
            select(EmployeeOrm)
            .join(TaskOrm, TaskOrm.employee_id == EmployeeOrm.id)
            .where(TaskOrm.id == parent_task_id)
        )
        result = await session.execute(query)
        return result.scalar()


async def get_important_tasks_and_employees():
    important_tasks = await get_important_tasks()
    least_busy_employee = await get_least_busy_employee()
    employees_and_tasks = []

    async for session in get_async_session():
        for task in important_tasks:
            parent_task_employee = await get_employee_for_parent_task(task.parent_task_id)
            if parent_task_employee:
                parent_task_employee_active_tasks_count = await session.execute(
                    select(func.count(TaskOrm.id))
                    .where(TaskOrm.employee_id == parent_task_employee.id, TaskOrm.status == StatusEnum.in_process)
                )
                parent_task_employee_active_tasks_count = parent_task_employee_active_tasks_count.scalar()

                least_busy_employee_active_tasks_count = await session.execute(
                    select(func.count(TaskOrm.id))
                    .where(TaskOrm.employee_id == least_busy_employee.id, TaskOrm.status == StatusEnum.in_process)
                )
                least_busy_employee_active_tasks_count = least_busy_employee_active_tasks_count.scalar()

                if parent_task_employee_active_tasks_count <= least_busy_employee_active_tasks_count + 2:
                    task.employee = parent_task_employee
                    employees_and_tasks.append(task)
                else:
                    task.employee = least_busy_employee
                    employees_and_tasks.append(task)
            else:
                task.employee = least_busy_employee
                employees_and_tasks.append(task)

    return employees_and_tasks
