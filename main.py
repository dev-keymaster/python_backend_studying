from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from uuid import UUID, uuid4

app = FastAPI(title="Task Manager API", version="1.0.0")


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    priority: int = Field(default=3, ge=1, le=5)
    is_completed: bool = False


class TaskCreate(TaskBase):
    pass


class TaskOut(TaskBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


@app.post("/tasks/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate) -> TaskOut:
    task_out = TaskOut(**task.model_dump())
    return task_out
