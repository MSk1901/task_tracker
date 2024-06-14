from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from src.tasks.models import StatusEnum


class TaskAddSchema(BaseModel):
    """Схема создания задачи"""
    title: str = Field(max_length=100)
    description: str
    employee_id: int | None = None
    deadline: datetime
    parent_task_id: int | None = None

    @field_validator('deadline')
    def check_deadline_is_aware(cls, v):
        """
        Валидатор даты
        проверяет, что указана таймзона
        """
        if v.tzinfo is None or v.tzinfo.utcoffset(v) is None:
            raise ValueError('deadline must be an aware datetime with timezone info')
        return v

    class ConfigDict:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
        use_enum_values = True


class TaskSchema(TaskAddSchema):
    """Схема чтения задачи"""
    id: int
    status: StatusEnum
    created_at: datetime
    updated_at: datetime | None

    class ConfigDict:
        from_attributes = True


class TaskUpdateSchema(TaskAddSchema):
    """Схема обновления задачи"""
    title: str | None = Field(max_length=100, default=None)
    description: str | None = None
    status: StatusEnum | None = None
    deadline: datetime | None = None


class TaskNotFoundSchema(BaseModel):
    """Схема ошибки TaskNotFound"""
    class ConfigDict:
        json_schema_extra = {
            'example':
                {
                    "detail": "Task with this id not found"
                }
        }
