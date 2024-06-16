from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.database import Base, get_async_session
from src.main import app

TEST_DATABASE_URL = (f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}"
                     f"@{settings.db_host}:{settings.db_port}/{settings.test_db_name}")

test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
async def logged_in_ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        login_data = {
            "username": "test@test.ru",
            "password": "Test"
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = await ac.post('auth/login', data=login_data, headers=headers)
        assert response.status_code == 204
        ac.cookies.set('token', response.cookies.get('token'))
        yield ac


@pytest.fixture(scope='session')
async def logged_in_ac_2():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        data_register = {
            "email": "test2@test.ru",
            "password": "Test"
        }

        data_login = {
            "username": "test2@test.ru",
            "password": "Test"
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = await ac.post('auth/register', json=data_register)
        assert response.status_code == 201

        response = await ac.post('auth/login', data=data_login, headers=headers)
        assert response.status_code == 204
        ac.cookies.set('token', response.cookies.get('token'))
        yield ac


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac


@pytest.fixture
def task_data():
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "deadline": "2024-06-30T20:00:00+00:00"
    }


@pytest.fixture
def employee_data():
    return {
        "first_name": "Ivan",
        "last_name": "Ivanov",
        "dob": "1990-08-25",
        "phone": "+79001112233",
        "position": "Test"
    }
