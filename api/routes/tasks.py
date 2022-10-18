import datetime as dt
from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import UUID4

from api.dependencies import azure_blob_celery_repository
from api.models.tasks.responses import CeleryTaskIdList, CeleryTaskStatistics, TaskStatusResponse
from api.repositories.celery import ICeleryRepository
from api.utils.date_utils import to_utc_datetime
from api.workers.run import celery_app

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
def status(task_id: UUID4) -> TaskStatusResponse:
    task_info = celery_app.AsyncResult(str(task_id))
    task_result = task_info.result
    if isinstance(task_result, Exception):
        task_result = None
    return TaskStatusResponse(task_id=task_id, status=task_info.status, result=task_result)


@router.get("/failures", response_model=CeleryTaskIdList)
def failures(
    date_from: Optional[dt.datetime | dt.date] = Query(
        None, alias="from", description="date in UTC after which failures should be included"
    ),
    date_to: Optional[dt.datetime | dt.date] = Query(
        None, alias="to", description="date in UTC before which failures should be included"
    ),
    repo: ICeleryRepository = Depends(azure_blob_celery_repository),
) -> CeleryTaskIdList:
    date_from = to_utc_datetime(date_from)
    date_to = to_utc_datetime(date_to)
    return repo.get_failures(date_from=date_from, date_to=date_to)


@router.get("/statistics", response_model=CeleryTaskStatistics)
def statistics(
    date_from: Optional[dt.datetime | dt.date] = Query(
        None, alias="from", description="date in UTC after which statistics should be included"
    ),
    date_to: Optional[dt.datetime | dt.date] = Query(
        None, alias="to", description="date in UTC before which statistics should be included"
    ),
    repo: ICeleryRepository = Depends(azure_blob_celery_repository),
) -> CeleryTaskStatistics:
    date_from = to_utc_datetime(date_from)
    date_to = to_utc_datetime(date_to)
    return repo.get_statistics(date_from=date_from, date_to=date_to)
