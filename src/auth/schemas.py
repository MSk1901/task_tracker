import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    """Схема для чтения пользователя"""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания пользователя"""
    class ConfigDict:
        json_schema_extra = {'example': {
            'email': 'user e-mail',
            'password': 'user password'
        }
        }


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления пользователя"""
    pass
