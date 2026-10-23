from compas.geometry import IntersectionResult


def test_empty_result():
    result = IntersectionResult[float]()

    assert not result
    assert result.number_of_results == 0
    assert result.is_empty
    assert not result.is_single
    assert not result.is_multiple
    assert not result.is_unique


def test_single_result():
    result = IntersectionResult((1.0,))

    assert result
    assert result.number_of_results == 1
    assert not result.is_empty
    assert result.is_single
    assert not result.is_multiple
    assert result.is_unique
    assert result[0] == 1.0


def test_multiple_results():
    result = IntersectionResult((1.0, 2.0))

    assert result.number_of_results == 2
    assert not result.is_empty
    assert not result.is_single
    assert result.is_multiple
    assert not result.is_unique
    assert list(result) == [1.0, 2.0]
    assert result[:] == (1.0, 2.0)
