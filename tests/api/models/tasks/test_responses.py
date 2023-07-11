from api.models.tasks.responses import CeleryTaskStatistics


def test_calculates_success_rate_as_one_if_total_is_zero() -> None:
    model = CeleryTaskStatistics(total=0, pending=3, succeeded=1, failed=9)
    assert model.success_rate == 1


def test_calculates_success_rate_as_succeeded_out_of_total() -> None:
    model = CeleryTaskStatistics(total=12, pending=3, succeeded=3, failed=9)
    assert model.success_rate == 0.25
