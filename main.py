from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, AliasChoices


class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class StatusType(str, Enum):
    TRIVIAL = "trivial"
    MINOR = "minor"
    MAJOR = "major"
    BLOCKER = "blocker"


class UserTask(BaseModel):
    uid: int = Field(validation_alias=AliasChoices("uid", "task_id", "id"))
    title: str = Field(min_length=5)
    priority: PriorityLevel = PriorityLevel.MEDIUM
    notes: str | None = None
    tags: list[str] = Field(default_factory=list[str])
