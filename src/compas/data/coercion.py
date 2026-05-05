from typing import Any
from typing import Sequence

from .validators import is_item_iterable


def coerce_sequence_of_tuple(sequence: Sequence[Any]) -> list[tuple[Any, ...]]:
    """Make sure all items of a sequence are of type tuple.

    Parameters
    ----------
    sequence
        A sequence of items.

    Returns
    -------
    list[tuple]
        A list containing the items of the original sequence,
        with each iterable item converted to a tuple,
        and non-iterable items wrapped in a tuple.

    Examples
    --------
    >>> items = coerce_sequence_of_tuple(["a", 1, (None,), [2.0, 3.0]])
    >>> all(isinstance(item, tuple) for item in items)
    True

    """
    items: list[tuple[Any, ...]] = []
    for item in sequence:
        if not isinstance(item, tuple):
            if not is_item_iterable(item):
                item = (item,)
            else:
                item = tuple(item)
        items.append(item)
    return items


def coerce_sequence_of_list(sequence: Sequence[Any]) -> list[list[Any]]:
    """Make sure all items of a sequence are of type list.

    Parameters
    ----------
    sequence
        A sequence of items.

    Returns
    -------
    list[list]
        A list containing the items of the original sequence,
        with each iterable item converted to a list,
        and non-iterable items wrapped in a list.

    Examples
    --------
    >>> items = coerce_sequence_of_list(["a", 1, (None,), [2.0, 3.0]])
    >>> all(isinstance(item, list) for item in items)
    True

    """
    items: list[list[Any]] = []
    for item in sequence:
        if not isinstance(item, list):
            if not is_item_iterable(item):
                item = [item]
            else:
                item = list(item)
        items.append(item)
    return items
