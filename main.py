from pydantic import BaseModel, Field, SecretStr, field_validator


class Employee(BaseModel):
    name: str
    email: str
    password: SecretStr = Field(exclude=True)
    salary: int

    @field_validator("name")
    @classmethod
    def name_validator(cls, v):
        if any(char.isdigit() for char in v):
            raise ValueError("Name must not contain numbers")
        return v

    @field_validator("email")
    @classmethod
    def email_validator(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v

    @field_validator("salary")
    @classmethod
    def salary_calidator(cls, v):
        if v < 30000:
            raise ValueError("Salary must be at least 30000")
        return v
