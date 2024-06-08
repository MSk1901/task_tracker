from fastapi import HTTPException


class TaskNotFound(HTTPException):
    def __init__(self):
        detail = f"Task with this id not found"
        super().__init__(status_code=404, detail=detail)
