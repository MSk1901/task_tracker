from fastapi import HTTPException
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src.employees.service import get_employee_by_id
from src.tasks.models import StatusEnum, Task
from src.tasks.schemas import TaskAddSchema, TaskUpdateSchema


async def get_all_tasks(session: AsyncSession):
    tasks = await session.scalars(select(Task))
    return tasks


async def get_important_tasks(session: AsyncSession):
    important_tasks = aliased(Task)
    dependent_tasks = aliased(Task)

    query = (
        select(important_tasks)
        .outerjoin(dependent_tasks, important_tasks.id == dependent_tasks.parent_task_id)
        .where(important_tasks.status == StatusEnum.created,
               dependent_tasks.status == StatusEnum.in_process)
    )
    result = await session.execute(query)
    return result.scalars().all()


async def get_task_by_id(task_id: int,
                         session: AsyncSession):
    task = await session.get(Task, task_id)
    return task


async def add_task(task: TaskAddSchema,
                   session: AsyncSession):
    task_dict = task.model_dump(exclude_unset=True)

    parent_task_id = task_dict.get('parent_task_id')
    employee_id = task_dict.get('employee_id')

    if type(parent_task_id) is int:
        data = await get_task_by_id(parent_task_id, session)
        if not data:
            message = 'Task with this id does not exist'
            raise HTTPException(status_code=400, detail=message)
    if type(employee_id) is int:
        data = await get_employee_by_id(employee_id, session)
        if not data:
            message = 'Employee with this id does not exist'
            raise HTTPException(status_code=400, detail=message)

    result = await session.scalars(
        insert(Task).
        values(task_dict)
        .returning(Task))
    created_task = result.first()
    await session.commit()
    return created_task


async def update_task(task: Task,
                      update_data: TaskUpdateSchema,
                      session: AsyncSession):
    update_dict = update_data.model_dump(exclude_unset=True)

    parent_task_id = update_dict.get('parent_task_id')
    employee_id = update_dict.get('employee_id')

    if type(parent_task_id) is int:
        data = await get_task_by_id(parent_task_id, session)
        if not data:
            message = 'Task with this id does not exist'
            raise HTTPException(status_code=400, detail=message)
    if type(employee_id) is int:
        data = await get_employee_by_id(employee_id, session)
        if not data:
            message = 'Employee with this id does not exist'
            raise HTTPException(status_code=400, detail=message)

    result = await session.scalars(
        update(Task)
        .where(Task.id == task.id)
        .values(**update_dict)
        .returning(Task)
    )
    updated_task = result.first()
    await session.commit()
    return updated_task


async def delete_task(task: Task, session: AsyncSession):
    stmt = delete(Task).where(Task.id == task.id)
    await session.execute(stmt)
    await session.commit()
