from src.employees.schemas import EmployeeNameSchema, EmployeeSchema
from src.tasks.schemas import TaskSchema


class EmployeeTasksSchema(EmployeeSchema):
    """Схема сотрудника со списком его задач"""
    tasks: list[TaskSchema]


class ImportantTaskSchema(TaskSchema):
    """Схема задачи, в которой указано ФИО сотрудника"""
    employee: EmployeeNameSchema
