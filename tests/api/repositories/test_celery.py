import datetime as dt

import pytest
from _pytest.fixtures import FixtureRequest
from azure.storage.blob import ContainerClient

from api.models.tasks.metadata import CeleryTaskMetaData
from api.models.tasks.responses import CeleryTaskIdList, CeleryTaskStatistics
from api.repositories.celery import AzureBlobCeleryRepository, ICeleryRepository, InMemoryCeleryRepository


@pytest.mark.integration
class TestCeleryRepositoryContract:
    _tz = dt.timezone.utc
    _failed_task = CeleryTaskMetaData(id="a", status="FAILURE")
    _succeeded_task = CeleryTaskMetaData(id="b", status="SUCCESS")

    @pytest.fixture(params=["in-memory", "azure-blob"], scope="class")
    def repository(self, request: FixtureRequest, celery_container_client: ContainerClient) -> ICeleryRepository:
        repo: ICeleryRepository = (
            InMemoryCeleryRepository()
            if request.param == "in-memory"
            else AzureBlobCeleryRepository(celery_container_client)
        )
        repo.save([self._failed_task, self._succeeded_task])
        return repo

    def test_get_failures_with_no_start_or_end_date(self, repository: ICeleryRepository) -> None:
        actual = repository.get_failures()
        expected = CeleryTaskIdList(task_ids=[self._failed_task.id])
        assert actual == expected

    def test_get_failures_with_start_date(self, repository: ICeleryRepository) -> None:
        actual = repository.get_failures(date_from=dt.datetime.now(self._tz))
        expected = CeleryTaskIdList(task_ids=[])
        assert actual == expected

    def test_get_failures_with_end_date(self, repository: ICeleryRepository) -> None:
        actual = repository.get_failures(date_to=dt.datetime.now(self._tz))
        expected = CeleryTaskIdList(task_ids=[self._failed_task.id])
        assert actual == expected

    def test_get_failures_with_start_and_end_date(self, repository: ICeleryRepository) -> None:
        actual = repository.get_failures(date_from=dt.datetime.now(self._tz), date_to=dt.datetime.now(self._tz))
        expected = CeleryTaskIdList(task_ids=[])
        assert actual == expected

    def test_get_statistics_with_no_start_or_end_date(self, repository: ICeleryRepository) -> None:
        actual = repository.get_statistics()
        expected = CeleryTaskStatistics(total=2, pending=0, succeeded=1, failed=1, success_rate=0.5)
        assert actual == expected

    def test_get_statistics_with_start_date(self, repository: ICeleryRepository) -> None:
        actual = repository.get_statistics(date_from=dt.datetime.now(self._tz))
        expected = CeleryTaskStatistics(total=0, pending=0, succeeded=0, failed=0, success_rate=1)
        assert actual == expected

    def test_get_statistics_with_end_date(self, repository: ICeleryRepository) -> None:
        actual = repository.get_statistics(date_to=dt.datetime.now(self._tz))
        expected = CeleryTaskStatistics(total=2, pending=0, succeeded=1, failed=1, success_rate=0.5)
        assert actual == expected

    def test_get_statistics_with_start_and_end_date(self, repository: ICeleryRepository) -> None:
        actual = repository.get_statistics(date_from=dt.datetime.now(self._tz), date_to=dt.datetime.now(self._tz))
        expected = CeleryTaskStatistics(total=0, pending=0, succeeded=0, failed=0, success_rate=1)
        assert actual == expected
