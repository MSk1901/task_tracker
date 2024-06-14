from typing import Mapping

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.dependencies import current_user
from src.schemas import ImportantTaskSchema
from src.service import get_important_tasks_and_employees
from src.tasks import service
from src.tasks.dependencies import valid_task_id
from src.tasks.models import Task
from src.tasks.schemas import TaskSchema, TaskNotFoundSchema, TaskAddSchema, TaskUpdateSchema

router = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)


@router.get(
    '',
    response_model=list[TaskSchema]
)
async def get_all_tasks(session: AsyncSession = Depends(get_async_session)):
    tasks = await service.get_all_tasks(session)
    return tasks


@router.get(
    '/important',
    response_model=list[ImportantTaskSchema]
)
async def get_important_tasks(session: AsyncSession = Depends(get_async_session)):
    result = await get_important_tasks_and_employees(session)
    return result


@router.get(
    '/{task_id}',
    response_model=TaskSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': TaskNotFoundSchema,
            'description': "Task not found"
        }
    }
)
async def get_task(task: Task = Depends(valid_task_id)):
    return task


@router.post(
    '',
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
)
async def add_task(task: TaskAddSchema,
                   user=Depends(current_user),
                   session: AsyncSession = Depends(get_async_session)):
    result = await service.add_task(task, session)
    return result


@router.patch(
    '/{task_id}',
    response_model=TaskSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': TaskNotFoundSchema,
            'description': "Task not found"
        }
    }
)
async def update_task(update_data: TaskUpdateSchema,
                      task: Task = Depends(valid_task_id),
                      session: AsyncSession = Depends(get_async_session),
                      user=Depends(current_user)):
    result = await service.update_task(task, update_data, session)
    return result


@router.delete(
    '/{task_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            'model': TaskNotFoundSchema,
            'description': "Task not found"
        }
    }
)
async def delete_task(task: Task = Depends(valid_task_id),
                      session: AsyncSession = Depends(get_async_session),
                      user=Depends(current_user)):
    await service.delete_task(task, session)
