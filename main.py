from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel


app = FastAPI()


users_db = [
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "email": "test@test.com",
        "first_name": "Ivan",
    },
    {
        "id": "660e8400-e29b-41d4-a716-446655440001",
        "email": "test@test.com",
        "first_name": "Petr",
    },
    {
        "id": "770e8400-e29b-41d4-a716-446655440002",
        "email": "test@test.com",
        "first_name": "Sergey",
    },
    {
        "id": "880e8400-e29b-41d4-a716-446655440003",
        "email": "test@test.com",
        "first_name": "Dmitry",
    },
]


class User(BaseModel):
    id: str
    email: str
    first_name: str


@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(
    user_id: str = Path(
        ..., description="The ID of the user to get", min_length=36, max_length=36
    )
):
    user = next((u for u in users_db if u["id"] == user_id), None)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user


@app.get("/users", response_model=list[User])
def get_users_list(offset: int = Query(0, ge=0), limit: int = Query(100, ge=1)):
    return users_db[offset : offset + limit]
