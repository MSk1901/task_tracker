from typing import Mapping

from src.tasks import service
from src.tasks.exceptions import TaskNotFound


async def valid_task_id(task_id: int) -> Mapping:
    task = await service.get_task_by_id(task_id)
    if not task:
        raise TaskNotFound()

    return task
