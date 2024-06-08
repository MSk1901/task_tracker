from src.employees.schemas import SEmployee, SEmployeeName
from src.tasks.schemas import STask


class SEmployeeTasks(SEmployee):
    tasks: list[STask]


class SImportantTask(STask):
    employee: SEmployeeName
