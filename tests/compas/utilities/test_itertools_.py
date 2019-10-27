import pytest

from compas.utilities import list_like


# ==============================================================================
# match_length
# ==============================================================================

@pytest.mark.parametrize(("target", "base"),
                         [("hello", [0.5])]
)
def test_match_length_float_to_string(target, base):
    assert list_like(target, base) == [0.5, None, None, None, None]

@pytest.mark.parametrize(("target", "base"),
                         [(['foo', 'bar'], {'key_1': 'a', 'key_2': 'b'})]
)
def test_match_length_list_to_dict(target, base):
    assert list_like(target, base) == ['key_1', 'key_2']