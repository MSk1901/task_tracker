from fastapi import FastAPI

from src.auth.auth import auth_backend
from src.auth.schemas import UserRead, UserCreate
from src.dependencies import fastapi_users

from src.employees.router import router as router_employees
from src.tasks.router import router as router_tasks

app = FastAPI()


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_tasks)
app.include_router(router_employees)
