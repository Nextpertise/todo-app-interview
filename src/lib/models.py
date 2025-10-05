from pydantic import BaseModel, ConfigDict, Field
from typing import List
from uuid import UUID, uuid4


class Todo(BaseModel):
    uuid: UUID = Field(default_factory=lambda: uuid4())
    title: str
    description: str
    parent_uuid: UUID | None = None

    def __repr__(self):
        return f"Todo(id={self.uuid}, title={self.title}, description={self.description}, parent_id={self.parent_uuid})"

    model_config = ConfigDict(arbitrary_types_allowed=True)


class TodoWithChildren(Todo):
    children: List[UUID] = []
