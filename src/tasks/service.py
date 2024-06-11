from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import aliased

from src.database import get_async_session
from src.tasks.models import Task, StatusEnum
from src.tasks.schemas import TaskUpdateSchema, TaskAddSchema


async def get_all_tasks():
    async for session in get_async_session():
        tasks = await session.scalars(select(Task))
        return tasks


async def get_important_tasks():
    async for session in get_async_session():
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


async def get_task_by_id(task_id: int):
    async for session in get_async_session():
        task = await session.get(Task, task_id)
        return task


async def add_task(task: TaskAddSchema):
    async for session in get_async_session():
        result = await session.scalars(insert(Task).values(**task.dict()).returning(Task))
        created_task = result.first()
        await session.commit()
        return created_task


async def update_task(task, update_data: TaskUpdateSchema):
    async for session in get_async_session():
        update_dict = update_data.dict(exclude_unset=True)
        result = await session.scalars(
            update(Task)
            .where(Task.id == task.id)
            .values(**update_dict)
            .returning(Task)
        )
        updated_task = result.first()
        await session.commit()
        return updated_task


async def delete_task(task):
    async for session in get_async_session():
        stmt = delete(Task).where(Task.id == task.id)
        await session.execute(stmt)
        await session.commit()
