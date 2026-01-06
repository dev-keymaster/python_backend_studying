from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class TaskStatus(str, Enum):
    PENDING = "pending"
    FINISHED = "finished"


class Task(BaseModel):
    id: int = Field(gt=0)
    content: str = Field(min_length=1)
    completed: bool = False
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)


def complete_task(task: Task):
    task.completed = True
    task.status = TaskStatus.FINISHED
    print(
        f"Task {task.id} is completed({task.completed}): {task.content} at {task.created_at} with status {task.status}"
    )


def print_all_tasks(tasks: list[Task]):
    for task in tasks:
        complete_task(task)


task1 = Task(id=1, content="task1")
task2 = Task(id=2, content="task2")
task3 = Task(id=3, content="task3")

tasks_list = [task1, task2, task3]

print_all_tasks(tasks_list)
