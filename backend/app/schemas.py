from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

Status = Literal["todo", "shooting", "done"]


class ShotBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: Status = "todo"


class ShotCreate(ShotBase):
    pass


class ShotUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: Status | None = None


class ShotRead(ShotBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
