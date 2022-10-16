from pydantic import BaseModel


class CeleryTaskMetaData(BaseModel):
    id: str
    status: str
