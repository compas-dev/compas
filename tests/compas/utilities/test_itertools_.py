import pytest

from compas.utilities import iterable_like


# ==============================================================================
# iterable_like
# ==============================================================================

@pytest.mark.parametrize(("target", "base"),
                         [("hello", [0.5])]
)
def test_iterable_like_string_and_float(target, base):
    a = [_ for _ in iterable_like(target, base)]
    assert a == [0.5, None, None, None, None]

@pytest.mark.parametrize(("target", "base", "fillvalue"),
                         [(['foo', 'bar', 'baz'], {'key_1': 'a', 'key_2': 'b'}, 'key_3')]
)
def test_iterable_like_list_and_dict(target, base, fillvalue):
    a = [_ for _ in iterable_like(target, base, fillvalue)]
    assert a == ['key_1', 'key_2', 'key_3']


@pytest.mark.parametrize(("target", "base", "fillvalue", "as_single"),
                         [(range(2), ['a', 'b'], 0, False)
                         ]
)
def test_iterable_like_generator_and_list(target, base, fillvalue, as_single):
    a = [_ for _ in iterable_like(target, base, fillvalue, as_single)]
    print('a is {}'.format(a))
    assert a == ['a', 'b']
