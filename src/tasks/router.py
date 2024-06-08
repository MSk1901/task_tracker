from typing import Mapping

from fastapi import APIRouter, Depends, status

from src.employees.service import get_important_tasks_and_employees
from src.schemas import SImportantTask
from src.tasks import service
from src.tasks.dependencies import valid_task_id
from src.tasks.schemas import STaskAdd, STask, STaskNotFound, STaskUpdate

router = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)


@router.get(
    '',
    response_model=list[STask]
)
async def get_all_tasks():
    tasks = await service.get_all_tasks()
    return tasks


@router.get(
    '/important',
    response_model=list[SImportantTask]
)
async def get_important_tasks():
    result = await get_important_tasks_and_employees()
    return result


@router.get(
    '/{task_id}',
    response_model=STask,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': STaskNotFound,
            'description': "Task not found"
        }
    }
)
async def get_task(task: Mapping = Depends(valid_task_id)):
    return task


@router.post(
    '',
    response_model=STask,
    status_code=status.HTTP_201_CREATED,
)
async def add_task(task: STaskAdd):
    result = await service.add_task(task)
    return result


@router.patch(
    '/{task_id}',
    response_model=STask,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': STaskNotFound,
            'description': "Task not found"
        }
    }
)
async def update_task(update_data: STaskUpdate, task: Mapping = Depends(valid_task_id)):
    result = await service.update_task(task, update_data)
    return result


@router.delete(
    '/{task_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': STaskNotFound,
            'description': "Task not found"
        }
    }
)
async def delete_task(task: Mapping = Depends(valid_task_id)):
    await service.delete_task(task)


