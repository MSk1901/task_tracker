import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    class ConfigDict:
        json_schema_extra = {'example': {
            'email': 'user e-mail',
            'password': 'user password'
        }
        }


class UserUpdate(schemas.BaseUserUpdate):
    pass
