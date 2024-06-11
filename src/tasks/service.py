from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import aliased

from src.database import get_async_session
from src.tasks.models import TaskOrm, StatusEnum
from src.tasks.schemas import STaskUpdate, STaskAdd


async def get_all_tasks():
    async for session in get_async_session():
        tasks = await session.scalars(select(TaskOrm))
        return tasks


async def get_important_tasks():
    async for session in get_async_session():
        important_tasks = aliased(TaskOrm)
        dependent_tasks = aliased(TaskOrm)

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
        task = await session.get(TaskOrm, task_id)
        return task


async def add_task(task: STaskAdd):
    async for session in get_async_session():
        result = await session.scalars(insert(TaskOrm).values(**task.dict()).returning(TaskOrm))
        created_task = result.first()
        await session.commit()
        return created_task


async def update_task(task, update_data: STaskUpdate):
    async for session in get_async_session():
        update_dict = update_data.dict(exclude_unset=True)
        result = await session.scalars(
            update(TaskOrm)
            .where(TaskOrm.id == task.id)
            .values(**update_dict)
            .returning(TaskOrm)
        )
        updated_task = result.first()
        await session.commit()
        return updated_task


async def delete_task(task):
    async for session in get_async_session():
        stmt = delete(TaskOrm).where(TaskOrm.id == task.id)
        await session.execute(stmt)
        await session.commit()
