from pydantic import UUID4, BaseModel


class CeleryTaskResponse(BaseModel):
    task_id: UUID4
