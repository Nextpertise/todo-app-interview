from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
import uuid

class Todo(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    parent_uuid: Optional[str] = None

    def __repr__(self):
        return f"Todo(id={self.uuid}, title={self.title}, description={self.description}, parent_id={self.parent_uuid})"

    model_config = ConfigDict(arbitrary_types_allowed=True)


class TodoWithChildren(Todo):
    children: List[str] = Field(default_factory=list)