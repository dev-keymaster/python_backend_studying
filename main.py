from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI, Query, status, HTTPException
from uuid import UUID, uuid4
from typing import Annotated

app = FastAPI(
    title="Update/Delete api",
    description="API for updating and deleting resources",
    version="1.0.0",
)

users_db = [
    {
        "id": UUID("550e8400-e29b-41d4-a716-446655440000"),
        "email": "ivan@example.com",
        "first_name": "Ivan",
    },
    {
        "id": UUID("660e8400-e29b-41d4-a716-446655440001"),
        "email": "petr@example.com",
        "first_name": "Petr",
    },
    {
        "id": UUID("770e8400-e29b-41d4-a716-446655440002"),
        "email": "sergey@example.com",
        "first_name": "Sergey",
    },
]


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=2, max_length=50)


class User(UserBase):
    id: UUID = Field(..., default_factory=uuid4)


class UserUpdate(UserBase):
    pass


class UserResponse(User):
    pass


LimitType = Annotated[int, Query(ge=1, le=100)]
OffsetType = Annotated[int, Query(ge=0)]


@app.get("/users/", response_model=list[User])
async def get_users(
    limit: LimitType = 10,
    offset: OffsetType = 0,
):
    return users_db[offset : offset + limit]


@app.post(
    "/users",
    response_model=list[User],
    status_code=status.HTTP_201_CREATED,
)
async def create_user(new_user: User) -> list[User]:
    users_db.append(new_user.model_dump())
    return users_db


@app.put(
    "/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def update_user(user_id: UUID, user_data: UserUpdate) -> UserResponse:
    user = next((user for user in users_db if user["id"] == user_id), None)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    user.update(user_data.model_dump())

    return user


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID) -> None:
    user_to_delete = next((user for user in users_db if user["id"] == user_id), None)

    if not user_to_delete:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")

    users_db.remove(user_to_delete)
