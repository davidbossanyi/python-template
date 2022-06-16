from pydantic import BaseModel


class CeleryTaskResponse(BaseModel):
    task_id: str
