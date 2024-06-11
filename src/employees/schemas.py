import uuid
from datetime import date, timedelta
from pydantic import BaseModel, Field, field_validator


class EmployeeAddSchema(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    fathers_name: str | None = Field(max_length=50, default=None)
    dob: date
    phone: str | None = Field(pattern=r'^\+79\d{9}$', default=None)
    position: str = Field(max_length=100)

    @field_validator('dob')
    def validate_dob(cls, v):
        if v >= date.today():
            raise ValueError("Date of birth must be in the past")
        elif date.today() - v > timedelta(days=365 * 100):
            raise ValueError("Date of birth can't be more than 100 years ago")
        return v


class EmployeeSchema(EmployeeAddSchema):
    id: int
    user_id: uuid.UUID


class EmployeeUpdateSchema(EmployeeAddSchema):
    first_name: str | None = Field(max_length=50, default=None)
    last_name: str | None = Field(max_length=50, default=None)
    dob: date | None = None
    position: str | None = Field(max_length=100, default=None)


class EmployeeNameSchema(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    fathers_name: str | None = Field(max_length=50, default=None)


class EmployeeNotFoundSchema(BaseModel):
    class Config:
        json_schema_extra = {
            'example':
                {
                    "detail": "Employee with this id not found"
                }
        }


class EmployeeAlreadyExistsSchema(BaseModel):
    class Config:
        json_schema_extra = {
            'example':
                {
                    "detail": "Employee already exists"
                }
        }
