from pydantic import BaseModel, Field


class CeleryTaskMetaData(BaseModel):
    id: str = Field(..., alias="task_id")
    status: str

    class Config:
        allow_population_by_field_name = True
