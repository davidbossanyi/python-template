from pydantic import BaseModel, ConfigDict, Field


class CeleryTaskMetaData(BaseModel):
    id: str = Field(..., alias="task_id")
    status: str

    model_config = ConfigDict(populate_by_name=True)
