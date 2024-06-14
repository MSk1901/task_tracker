from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.tasks import service
from src.tasks.exceptions import TaskNotFound
from src.tasks.models import Task


async def valid_task_id(task_id: int,
                        session: AsyncSession = Depends(get_async_session)) -> Task:
    """Зависимость, проверяющая что задача с указанным id существует"""
    task = await service.get_task_by_id(task_id, session)
    if not task:
        raise TaskNotFound()

    return task
