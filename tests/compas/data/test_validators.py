import compas
import pytest

from compas.data import is_sequence_of_int
from compas.data import is_sequence_of_uint
from compas.data import is_sequence_of_float

from compas.data import is_int3
from compas.data import is_float3
from compas.data import is_float4x4


@pytest.mark.parametrize(
    "sequence,result",
    [
        (range(10), True),
        (range(+10, -10, -1), True),
        (list(range(10)), True),
        (list(range(+10, -10, -1)), True),
        ([1, 2, 3, 4.0], False),
        ([1, 2, "3"], False),
        ([], True),
    ],
)
def test_is_sequence_of_int(sequence, result):
    assert is_sequence_of_int(sequence) is result


@pytest.mark.parametrize(
    "sequence,result",
    [
        (range(10), True),
        (range(0, -10, -1), False),
        (range(+10, -10, -1), False),
        ([1, 2, 3.0], False),
        ([1, 2, "3"], False),
        ([], True),
    ],
)
def test_is_sequence_of_uint(sequence, result):
    assert is_sequence_of_uint(sequence) is result


@pytest.mark.parametrize(
    "sequence,result",
    [
        (range(10), False),
        (range(+10, -10, -1), False),
        ([1, 2, 3.0], False),
        ([1, 2, "3"], False),
        ([], True),
        (map(float, range(10)), True),
        (map(float, range(+10, -10, -1)), True),
    ],
)
def test_is_sequence_of_float(sequence, result):
    assert is_sequence_of_float(sequence) is result


@pytest.mark.parametrize(
    "sequence,result",
    [
        (range(3), True),
        (range(+1, -2, -1), True),
        (range(4), False),
        (range(2), False),
        ([1, 2, 3.0], False),
        ([1, 2, "3"], False),
        ([], False),
    ],
)
def test_is_int3(sequence, result):
    assert is_int3(sequence) is result


@pytest.mark.parametrize(
    "sequence,result",
    [
        (list(map(float, range(3))), True),
        (list(map(float, range(+1, -2, -1))), True),
        (list(map(float, range(4))), False),
        (list(map(float, range(2))), False),
        ([1, 2, 3.0], False),
        ([1, 2, "3"], False),
        ([], False),
    ],
)
def test_is_float3(sequence, result):
    assert is_float3(sequence) is result


if compas.PY3:

    @pytest.mark.parametrize(
        "sequence,result",
        [
            (map(float, range(3)), False),
            (map(float, range(+1, -2, -1)), False),
        ],
    )
    def test_is_float3_invalid(sequence, result):
        with pytest.raises(TypeError):
            assert is_float3(sequence) is result


@pytest.mark.parametrize(
    "sequence,result",
    [
        ([list(map(float, range(4))) for _ in range(4)], True),
        ([list(map(float, range(+2, -2, -1))) for _ in range(4)], True),
        ([list(map(float, range(5))) for _ in range(4)], False),
        ([list(map(float, range(3))) for _ in range(4)], False),
        ([list(map(float, range(4))) for _ in range(5)], False),
        ([list(map(float, range(4))) for _ in range(3)], False),
        ([[1, 2, 3.0, 4.0] for _ in range(4)], False),
        ([[1, 2, "3", 4.0] for _ in range(4)], False),
        ([], False),
    ],
)
def test_is_float4x4(sequence, result):
    assert is_float4x4(sequence) is result


if compas.PY3:

    @pytest.mark.parametrize(
        "sequence,result",
        [
            ([map(float, range(4)) for _ in range(4)], True),
            ([map(float, range(+2, -2, -1)) for _ in range(4)], True),
        ],
    )
    def test_is_float4x4_invalid(sequence, result):
        with pytest.raises(TypeError):
            assert is_float4x4(sequence) is result
