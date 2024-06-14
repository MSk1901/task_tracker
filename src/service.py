from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.employees.service import (get_employee_for_parent_task,
                                   get_least_busy_employee)
from src.tasks.models import StatusEnum, Task
from src.tasks.service import get_important_tasks


async def get_important_tasks_and_employees(session: AsyncSession):
    important_tasks = await get_important_tasks(session)
    least_busy_employee = await get_least_busy_employee(session)
    employees_and_tasks = []

    for task in important_tasks:

        parent_task_employee = await get_employee_for_parent_task(task.parent_task_id, session)

        if parent_task_employee:
            parent_task_employee_active_tasks_count = await session.execute(
                select(func.count(Task.id))
                .where(Task.employee_id == parent_task_employee.id, Task.status == StatusEnum.in_process)
            )
            parent_task_employee_active_tasks_count = parent_task_employee_active_tasks_count.scalar()

            least_busy_employee_active_tasks_count = await session.execute(
                select(func.count(Task.id))
                .where(Task.employee_id == least_busy_employee.id, Task.status == StatusEnum.in_process)
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
