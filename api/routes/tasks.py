from fastapi import APIRouter
from pydantic import UUID4

from api.models.tasks.responses import TaskStatusResponse
from api.workers.examples import celery_app

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
def status(task_id: UUID4) -> TaskStatusResponse:
    task_info = celery_app.AsyncResult(str(task_id))
    task_result = task_info.result
    if isinstance(task_result, Exception):
        task_result = None
    return TaskStatusResponse(task_id=task_id, status=task_info.status, result=task_result)
