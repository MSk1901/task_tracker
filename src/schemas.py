from src.employees.schemas import EmployeeSchema, EmployeeNameSchema
from src.tasks.schemas import TaskSchema


class EmployeeTasksSchema(EmployeeSchema):
    tasks: list[TaskSchema]


class ImportantTaskSchema(TaskSchema):
    employee: EmployeeNameSchema
