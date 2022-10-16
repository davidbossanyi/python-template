from typing import Optional

from pydantic import UUID4, BaseModel, validator


class TaskStatusResponse(BaseModel):
    task_id: UUID4
    status: str
    result: Optional[str]


class CeleryTaskIdList(BaseModel):
    task_ids: list[str]


class CeleryTaskStatistics(BaseModel):
    total: int
    pending: int
    succeeded: int
    failed: int
    success_rate: Optional[float]

    @validator("success_rate", always=True)
    def calculate_success_rate(cls, value: float, values: dict) -> float:
        total = values["total"]
        return values["succeeded"] / total if total > 0 else 1
