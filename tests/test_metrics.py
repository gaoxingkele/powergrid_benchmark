from powergrid_benchmark.evaluation import mae, rmse


def test_mae() -> None:
    assert mae([1.0, 2.0, 3.0], [1.0, 3.0, 1.0]) == 1.0


def test_rmse() -> None:
    assert round(rmse([1.0, 2.0], [1.0, 4.0]), 6) == round(2**0.5, 6)
