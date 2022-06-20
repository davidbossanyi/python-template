from typing import Optional

from pydantic import UUID4, BaseModel


class TaskStatusResponse(BaseModel):
    task_id: UUID4
    status: str
    result: Optional[str]
