from fastapi import APIRouter, Query

from api.models.examples.responses import CeleryTaskResponse
from api.workers.examples import wait_for

router = APIRouter(prefix="/api/examples", tags=["Examples"])


@router.get("/wait", response_model=CeleryTaskResponse)
def wait(seconds: int = Query(10, description="number of seconds to wait")) -> CeleryTaskResponse:
    task = wait_for.delay(seconds=seconds)
    return CeleryTaskResponse(task_id=task.id)
