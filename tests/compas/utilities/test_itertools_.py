import pytest

from compas.utilities import match_length


# ==============================================================================
# match_length
# ==============================================================================

@pytest.mark.parametrize(("base", "target"),
                         [(0,"hello")]
)
def test_match_length_float_to_string(base, target):
    assert match_length(base, target) == [0, 0, 0, 0, 0]

@pytest.mark.parametrize(("base", "target"),
                         [(['foo', 'bar'], {'key_1': 'a', 'key_2': 'b'})]
)
def test_match_length_list_to_dict(base, target):
    assert match_length(base, target) == ['foo', 'bar']