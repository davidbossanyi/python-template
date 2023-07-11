import datetime as dt
import json
import time
from typing import ClassVar, Protocol

from azure.storage.blob import ContainerClient

from api.models.tasks.metadata import CeleryTaskMetaData
from api.models.tasks.responses import CeleryTaskIdList, CeleryTaskStatistics


class ICeleryRepository(Protocol):
    def save(self, tasks: list[CeleryTaskMetaData]) -> None:
        ...

    def get_failures(
        self, date_from: dt.datetime | None = None, date_to: dt.datetime | None = None
    ) -> CeleryTaskIdList:
        ...

    def get_statistics(
        self, date_from: dt.datetime | None = None, date_to: dt.datetime | None = None
    ) -> CeleryTaskStatistics:
        ...


class InMemoryCeleryRepository(ICeleryRepository):
    _store: ClassVar[dict[dt.datetime, CeleryTaskMetaData]] = {}
    _tz = dt.timezone.utc

    def save(self, tasks: list[CeleryTaskMetaData]) -> None:
        for task in tasks:
            now = dt.datetime.now(self._tz)
            self._store[now] = task
            time.sleep(0.001)

    def get_failures(
        self, date_from: dt.datetime | None = None, date_to: dt.datetime | None = None
    ) -> CeleryTaskIdList:
        task_ids = [
            task.id
            for date, task in self._store.items()
            if (not date_from or date >= date_from) and (not date_to or date <= date_to) and task.status == "FAILURE"
        ]
        return CeleryTaskIdList(task_ids=task_ids)

    def get_statistics(
        self, date_from: dt.datetime | None = None, date_to: dt.datetime | None = None
    ) -> CeleryTaskStatistics:
        tasks = [
            task
            for date, task in self._store.items()
            if (not date_from or date >= date_from) and (not date_to or date <= date_to)
        ]
        total = len(tasks)
        pending = len([task for task in tasks if task.status == "PENDING"])
        succeeded = len([task for task in tasks if task.status == "SUCCESS"])
        failed = len([task for task in tasks if task.status == "FAILURE"])
        return CeleryTaskStatistics(total=total, pending=pending, succeeded=succeeded, failed=failed)


class AzureBlobCeleryRepository(ICeleryRepository):
    _prefix = "celery-task-meta-"

    def __init__(self, container_client: ContainerClient):
        self._container_client = container_client

    def save(self, tasks: list[CeleryTaskMetaData]) -> None:
        for task in tasks:
            self._container_client.upload_blob(name=f"{self._prefix}{task.id}", data=task.json(), overwrite=True)

    def get_failures(
        self, date_from: dt.datetime | None = None, date_to: dt.datetime | None = None
    ) -> CeleryTaskIdList:
        blobs = [
            blob.name
            for blob in self._container_client.list_blobs(name_starts_with=self._prefix)
            if (not date_from or blob.creation_time >= date_from)  # type: ignore[operator]
            and (not date_to or blob.creation_time <= date_to)  # type: ignore[operator]
        ]
        tasks = [self._get_blob_contents(blob) for blob in blobs]  # type: ignore[arg-type]
        task_ids = [task.id for task in tasks if task.status == "FAILURE"]
        return CeleryTaskIdList(task_ids=task_ids)

    def get_statistics(
        self, date_from: dt.datetime | None = None, date_to: dt.datetime | None = None
    ) -> CeleryTaskStatistics:
        blobs = [
            blob.name
            for blob in self._container_client.list_blobs(name_starts_with=self._prefix)
            if (not date_from or blob.creation_time >= date_from)  # type: ignore[operator]
            and (not date_to or blob.creation_time <= date_to)  # type: ignore[operator]
        ]
        tasks = [self._get_blob_contents(blob) for blob in blobs]  # type: ignore[arg-type]
        total = len(tasks)
        pending = len([task for task in tasks if task.status == "PENDING"])
        succeeded = len([task for task in tasks if task.status == "SUCCESS"])
        failed = len([task for task in tasks if task.status == "FAILURE"])
        return CeleryTaskStatistics(total=total, pending=pending, succeeded=succeeded, failed=failed)

    def _get_blob_contents(self, blob: str) -> CeleryTaskMetaData:
        blob_content = json.loads(self._container_client.download_blob(blob=blob).readall().decode())
        return CeleryTaskMetaData.parse_obj(blob_content)
