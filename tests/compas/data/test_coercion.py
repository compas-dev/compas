import pytest

from compas.data.coercion import coerce_sequence_of_list
from compas.data.coercion import coerce_sequence_of_tuple


def test_coerce_sequence_of_tuple_converts_iterables_and_scalars():
    sequence = [(1, 2), [3, 4], range(2), 5]

    assert coerce_sequence_of_tuple(sequence) == [(1, 2), (3, 4), (0, 1), (5,)]


def test_coerce_sequence_of_tuple_treats_strings_as_iterable():
    assert coerce_sequence_of_tuple(["ab", ""]) == [("a", "b"), ()]


def test_coerce_sequence_of_tuple_accepts_iterators():
    sequence = (item for item in ([1, 2], 3))

    assert coerce_sequence_of_tuple(sequence) == [(1, 2), (3,)]


def test_coerce_sequence_of_list_converts_iterables_and_scalars():
    sequence = [[1, 2], (3, 4), range(2), 5]

    assert coerce_sequence_of_list(sequence) == [[1, 2], [3, 4], [0, 1], [5]]


def test_coerce_sequence_of_list_treats_strings_as_iterable():
    assert coerce_sequence_of_list(["ab", ""]) == [["a", "b"], []]


def test_coerce_sequence_of_list_accepts_iterators():
    sequence = (item for item in ((1, 2), 3))

    assert coerce_sequence_of_list(sequence) == [[1, 2], [3]]


@pytest.mark.parametrize("coerce", [coerce_sequence_of_tuple, coerce_sequence_of_list])
def test_coerce_sequence_requires_an_iterable_sequence(coerce):
    with pytest.raises(TypeError):
        coerce(1)


@pytest.mark.parametrize("coerce", [coerce_sequence_of_tuple, coerce_sequence_of_list])
def test_coerce_sequence_handles_empty_sequences(coerce):
    assert coerce([]) == []
