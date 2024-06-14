## API Трекера задач сотрудников
**Backend-часть веб-приложения для трекинга задач.**
- Асинхронный backend
- CRUD для моделей задач и сотрудников
- Регистрация, авторизация с помощью библиотеки FastAPI Users
### Стек технологий:
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.2-blue?logo=FastAPI)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.7.4-blue?logo=Pydantic)](https://docs.pydantic.dev/latest/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.29-blue?logo=SQLAlchemy)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-1.13.1-blue)](https://alembic.sqlalchemy.org/en/latest/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)
[![Pytest](https://img.shields.io/badge/Pytest-8.2.2-blue?logo=Pytest)](https://docs.pytest.org/en/8.2.x/)

- `Python`
- `FastAPI`
- `Pydantic`
- `SQLAlchemy`
- `Alembic`
- `postgreSQL`
- `Pytest`

## Содержание

<details>
<summary>Инструкция по развертыванию проекта</summary>

#### 1. Клонируйте проект:
```
git clone https://github.com/MSk1901/task_tracker.git
```
#### 2. Перейдите в корневую директорию проекта 
#### 3. Настройте переменные окружения: 

   1. Создайте файл `.env` в корневой директории 
   2. Скопируйте в него содержимое файла `.env.example` и подставьте свои значения
   

#### 4. Cоздайте виртуальное окружение и установите зависимости:
```
poetry shell
```
```
poetry install
```
#### 4. Примените миграции:
```
alembic upgrade head
```
</details>

<details>
<summary>Использование</summary>

#### 1. Запустите сервер разработки:
```
uvicorn src.main:app
```
Сервер будет запущен на http://localhost:8000
#### 2. Перейдите в документацию:
В Swagger можно будет посмотреть доступные эндпоинты, и взаимодействовать с API
</details>

## Документация
Документация по API доступна по адресам:
- Swagger - http://localhost:8000/docs
- Redoc - http://localhost:8000/redoc



Автор проекта Мария Кузнецова - [kuznetsova19.m@gmail.com](mailto:kuznetsova19.m@gmail.com)
