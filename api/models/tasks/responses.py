from pydantic import UUID4, BaseModel


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

    @property
    def success_rate(self) -> float:
        return (self.succeeded / self.total) if self.total > 0 else 1
