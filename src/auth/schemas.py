import uuid

from fastapi_users import schemas
from pydantic import ConfigDict


class UserRead(schemas.BaseUser[uuid.UUID]):
    """Схема для чтения пользователя"""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания пользователя"""

    model_config = ConfigDict(
        json_schema_extra={'example': {
            'email': 'user@email.com',
            'password': 'password'
        }
        }
    )


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления пользователя"""
    pass
