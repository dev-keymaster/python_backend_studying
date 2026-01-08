from enum import Enum
from pydantic import BaseModel, Field, computed_field


class Employee(BaseModel):
    name: str = Field(min_length=8, max_length=50)
    role: str = Field(min_length=5, max_length=30)
    subordinates: list["Employee"] = Field(default_factory=list)

    @computed_field
    @property
    def is_manager(self) -> bool:
        return bool(self.subordinates)

    def get_total_team_size(self) -> int:
        total_size = 0
        for subordinate in self.subordinates:
            total_size += subordinate.get_total_team_size()
        return total_size
