from fastapi import HTTPException


class EmployeeNotFound(HTTPException):
    """Исключение для случая, когда сотрудник с указанным id не найден."""
    def __init__(self):
        detail = "Employee with this id not found"
        super().__init__(status_code=404, detail=detail)


class UserNotAuthorized(HTTPException):
    """Исключение для случая, когда пользователь не является создателем сотрудника."""
    def __init__(self):
        detail = "Only the employee creator can perform this action"
        super().__init__(status_code=403, detail=detail)


class EmployeeAlreadyExists(HTTPException):
    """Исключение для случая, сотрудник уже существует."""
    def __init__(self, detail=None):
        if not detail:
            detail = "Employee already exists"
        super().__init__(status_code=400, detail=detail)
