from fastapi import FastAPI
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SecretStr,
    field_validator,
    EmailStr,
    UUID4,
)

from uuid import uuid4

from pydantic.alias_generators import to_camel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: SecretStr = Field(min_length=8, exclude=True)

    @field_validator("email")
    @classmethod
    def email_must_be_valid(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v

    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, strict=True, extra="forbid"
    )

    @field_validator("password")
    @classmethod
    def password_must_be_valid(cls, v):
        if len(v) < 8 or "password" in v.get_secret_value().lower():
            raise ValueError(
                "Password must be at least 8 characters long and not contain 'password'"
            )
        return v


class UserOut(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    email: EmailStr

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/users/register", response_model=UserOut)
async def register_user(user: UserCreate):
    id = uuid4()
    return {"id": id, **user.model_dump()}
