from fastapi import APIRouter, Query

from api.models.examples.responses import CeleryTaskResponse
from api.workers.run import wait_for

router = APIRouter(prefix="/api/run", tags=["Examples"])


@router.get("/wait", response_model=CeleryTaskResponse)
def wait(
    seconds: int = Query(10, description="number of seconds to wait"),
    fail: bool = Query(False, description="cause the task to fail"),
) -> CeleryTaskResponse:
    task = wait_for.delay(seconds=seconds, fail=fail)
    return CeleryTaskResponse(task_id=task.id)
