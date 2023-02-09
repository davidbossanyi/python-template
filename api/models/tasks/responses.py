from pydantic import UUID4, BaseModel, validator


class TaskStatusResponse(BaseModel):
    task_id: UUID4
    status: str
    result: str | None


class CeleryTaskIdList(BaseModel):
    task_ids: list[str]


class CeleryTaskStatistics(BaseModel):
    total: int
    pending: int
    succeeded: int
    failed: int
    success_rate: float | None

    @validator("success_rate", always=True)
    def calculate_success_rate(cls, value: float, values: dict[str, int | float]) -> float:
        total = values["total"]
        return float(values["succeeded"] / total if total > 0 else 1)
