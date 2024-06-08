from fastapi import HTTPException


class EmployeeNotFound(HTTPException):
    def __init__(self):
        detail = f"Employee with this id not found"
        super().__init__(status_code=404, detail=detail)


class UserNotAuthorized(HTTPException):
    def __init__(self):
        detail = f"Only the employee creator can perform this action"
        super().__init__(status_code=403, detail=detail)


class EmployeeAlreadyExists(HTTPException):
    def __init__(self, detail=None):
        if not detail:
            detail = f"Employee already exists"
        super().__init__(status_code=400, detail=detail)

