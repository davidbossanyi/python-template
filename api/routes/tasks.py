from fastapi import APIRouter

from api.models.tasks.responses import TaskStatusResponse
from api.workers.celery_workers import celery_app

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
def status(task_id: str) -> TaskStatusResponse:
    task_info = celery_app.AsyncResult(task_id)
    task_result = task_info.result
    if isinstance(task_result, Exception):
        task_result = None
    return TaskStatusResponse(
        task_id=task_id, status=task_info.status, result=task_result
    )
