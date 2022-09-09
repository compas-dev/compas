from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .validators import is_item_iterable


def coerce_sequence_of_tuple(sequence):
    """Make sure all items of a sequence are of type tuple.

    Parameters
    ----------
    sequence : sequence
        A sequence of items.

    Returns
    -------
    list[tuple]
        A list containing the items of the original sequence,
        with each iterable item converted to a tuple,
        and non-iterable items wrapped in a tuple.

    Examples
    --------
    >>> items = coerce_sequence_of_tuple(['a', 1, (None, ), [2.0, 3.0]])
    >>> is_sequence_of_tuple(items)
    True

    """
    items = []
    for item in sequence:
        if not isinstance(item, tuple):
            if not is_item_iterable(item):
                item = (item,)
            else:
                item = tuple(item)
        items.append(item)
    return items


def coerce_sequence_of_list(sequence):
    """Make sure all items of a sequence are of type list.

    Parameters
    ----------
    sequence : sequence
        A sequence of items.

    Returns
    -------
    list[list]
        A list containing the items of the original sequence,
        with each iterable item converted to a list,
        and non-iterable items wrapped in a list.

    Examples
    --------
    >>> items = coerce_sequence_of_list(['a', 1, (None, ), [2.0, 3.0]])
    >>> is_sequence_of_list(items)
    True

    """
    items = []
    for item in sequence:
        if not isinstance(item, list):
            if not is_item_iterable(item):
                item = [item]
            else:
                item = list(item)
        items.append(item)
    return items
