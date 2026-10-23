from compas.data.validators import is_item_iterable


def test_is_item_iterable_does_not_consume_iterators():
    iterator = iter([1, 2, 3])

    assert is_item_iterable(iterator)
    assert list(iterator) == [1, 2, 3]


def test_is_item_iterable_uses_the_iterator_protocol():
    assert is_item_iterable("abc")
    assert not is_item_iterable(1.0)
