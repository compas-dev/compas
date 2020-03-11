from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

try:
    basestring
except NameError:
    basestring = str


__all__ = [
    'is_sequence_of_str',
    'is_sequence_of_int',
    'is_sequence_of_float',
    'is_sequence_of_tuple',
    'is_sequence_of_list',
    'is_sequence_of_dict',
    'is_sequence_of_iterable',

    'is_item_iterable',

    'coerce_sequence_of_tuple',
    'coerce_sequence_of_list',
]


# ==============================================================================
# check
# ==============================================================================


def is_sequence_of_str(sequence):
    """Determine if all items in a sequence are of type str.

    Parameters
    ----------
    sequence : list or tuple
        The sequence of items.

    Returns
    -------
    bool
        True if all items in the sequence are strings.
        False otherwise.

    Examples
    --------
    >>> is_sequence_of_str(['a', 'b', 'c'])
    True
    """
    return is_sequence_of_type(sequence, basestring)


def is_sequence_of_int(sequence):
    """Determine if all items in a sequence are of type int.

    Parameters
    ----------
    sequence : list or tuple
        The sequence of items.

    Returns
    -------
    bool
        True if all items in the sequence are of type int.
        False otherwise.

    Examples
    --------
    >>> is_sequence_of_int([1, 2, 3])
    True
    """
    return is_sequence_of_type(sequence, int)


def is_sequence_of_float(sequence):
    """Determine if all items in a sequence are of type float.

    Parameters
    ----------
    sequence : list or tuple
        The sequence of items.

    Returns
    -------
    bool
        True if all items in the sequence are of type float.
        False otherwise.

    Examples
    --------
    >>> is_sequence_of_float([1.0, 2.0, 3.0])
    True
    """
    return is_sequence_of_type(sequence, float)


def is_sequence_of_list(sequence):
    """Determine if all items in a sequence are of type list.

    Parameters
    ----------
    sequence : list or tuple
        The sequence of items.

    Returns
    -------
    bool
        True if all items in the sequence are of type list.
        False otherwise.

    Examples
    --------
    >>> is_sequence_of_list([[1], [1], [1]])
    True
    """
    return is_sequence_of_type(sequence, list)


def is_sequence_of_tuple(sequence):
    """Determine if all items in a sequence are of type tuple.

    Parameters
    ----------
    sequence : list or tuple
        The sequence of items.

    Returns
    -------
    bool
        True if all items in the sequence are of type tuple.
        False otherwise.

    Examples
    --------
    >>> is_sequence_of_tuple([(1, ), (1, ), (1, )])
    True
    """
    return is_sequence_of_type(sequence, tuple)


def is_sequence_of_dict(sequence):
    """Determine if all items in a sequence are of type dict.

    Parameters
    ----------
    sequence : list or tuple
        The sequence of items.

    Returns
    -------
    bool
        True if all items in the sequence are of type dict.
        False otherwise.

    Examples
    --------
    >>> is_sequence_of_dict([{'a': 1}, {'b': 2}, {'c': 3}])
    True
    """
    return is_sequence_of_type(sequence, dict)


def is_sequence_of_type(sequence, t):
    """Determine if all items in a sequence are of a specific type.

    Parameters
    ----------
    sequence : list or tuple
        The sequence of items.
    t : object
        The item type.

    Returns
    -------
    bool
        True if all items in the sequence are of the specified type.
        False otherwise.

    Examples
    --------
    >>> is_sequence_of_type([1, 2, 3], int)
    True
    """
    if any(not isinstance(item, t) for item in sequence):
        return False
    return True


def is_item_iterable(item):
    """Determine if an item is iterable.

    Parameters
    ----------
    item : object
        The item to test.

    Returns
    -------
    bool
        True if the item is iterable.
        False otherwise.

    Examples
    --------
    >>> is_item_iterable(1.0)
    False
    >>> is_item_iterable('abc')
    True
    """
    try:
        _ = [_ for _ in item]
    except TypeError:
        return False
    return True


def is_sequence_of_iterable(sequence):
    """Determine if a sequence contains only iterable items.

    Parameters
    ----------
    sequence : list or tuple
        A sequence of items.

    Returns
    -------
    bool
        True if all items in the sequence are iterable.
        False otherwise.

    Examples
    --------
    >>> is_sequence_of_iterable(['abc', [1.0], (2, 'a', None)])
    True
    """
    return all(is_item_iterable(item) for item in sequence)


# ==============================================================================
# coerce
# ==============================================================================

def coerce_sequence_of_tuple(sequence):
    """Make sure all items of a sequence are of type tuple.

    Parameters
    ----------
    sequence : list or tuple
        A sequence of items.

    Returns
    -------
    list of tuple
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
                item = (item, )
            else:
                item = tuple(item)
        items.append(item)
    return items


def coerce_sequence_of_list(sequence):
    """Make sure all items of a sequence are of type list.

    Parameters
    ----------
    sequence : list or tuple
        A sequence of items.

    Returns
    -------
    list of list
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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    doctest.testmod(globs=globals())
