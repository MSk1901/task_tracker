from fastapi import HTTPException


class TaskNotFound(HTTPException):
    """Исключение для случая, когда задача с указанным id не найдена."""
    def __init__(self):
        detail = "Task with this id not found"
        super().__init__(status_code=404, detail=detail)
