import pytest

from .validators import is_sequence_of_list
from .validators import is_sequence_of_tuple


@pytest.fixture(autouse=True)
def add_is_sequence_of(doctest_namespace):
    doctest_namespace["is_sequence_of_list"] = is_sequence_of_list
    doctest_namespace["is_sequence_of_tuple"] = is_sequence_of_tuple
