from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    basestring  # type: ignore
except NameError:
    basestring = str


def is_sequence_of_str(items):
    """Verify that the sequence contains only items of type str.

    Parameters
    ----------
    items : sequence
        The sequence of items.

    Returns
    -------
    bool
        True if all items are strings.
        False otherwise.

    """
    return all(isinstance(item, basestring) for item in items)


def is_sequence_of_int(items):
    """Verify that the sequence contains only integers.

    Parameters
    ----------
    items : sequence
        The sequence of items.

    Returns
    -------
    bool

    """
    return all(isinstance(item, int) for item in items)


def is_int3(items):
    """Verify that the sequence contains 3 integers.

    Parameters
    ----------
    items : sequence
        The sequence of items.

    Returns
    -------
    bool

    """
    return len(items) == 3 and all(isinstance(item, int) for item in items)


def is_sequence_of_float(items):
    """Verify that the sequence contains only floats.

    Parameters
    ----------
    items : sequence
        The sequence of items.

    Returns
    -------
    bool

    """
    return all(isinstance(item, float) for item in items)


def is_sequence_of_uint(items):
    """Verify that the sequence contains only unsigned integers.

    Parameters
    ----------
    items : sequence
        The sequence of items.

    Returns
    -------
    bool

    """
    return all(isinstance(item, int) and item >= 0 for item in items)


def is_float3(items):
    """Verify that the sequence contains 3 floats.

    Parameters
    ----------
    items : sequence
        The sequence of items.

    Returns
    -------
    bool

    """
    return len(items) == 3 and all(isinstance(item, float) for item in items)


def is_float4x4(items):
    """Verify that the sequence contains 4 sequences of each 4 floats.

    Parameters
    ----------
    items : sequence
        The sequence of items.

    Returns
    -------
    bool

    """
    return len(items) == 4 and all(len(item) == 4 and all(isinstance(i, float) for i in item) for item in items)


def is_sequence_of_list(items):
    """Verify that the sequence contains only items of type list.

    Parameters
    ----------
    items : sequence
        The items.

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
    return all(isinstance(item, list) for item in items)


def is_sequence_of_tuple(items):
    """Verify that the sequence contains only items of type tuple.

    Parameters
    ----------
    items : sequence
        The sequence of items.

    Returns
    -------
    bool
        True if all items in the sequence are of type tuple.
        False otherwise.

    Examples
    --------
    >>> is_sequence_of_tuple([(1,), (1,), (1,)])
    True

    """
    return all(isinstance(item, tuple) for item in items)


def is_sequence_of_dict(items):
    """Verify that the sequence contains only items of type dict.

    Parameters
    ----------
    items : sequence
        The sequence of items.

    Returns
    -------
    bool
        True if all items in the sequence are of type dict.
        False otherwise.

    Examples
    --------
    >>> is_sequence_of_dict([{"a": 1}, {"b": 2}, {"c": 3}])
    True

    """
    return all(isinstance(item, dict) for item in items)


def is_item_iterable(item):
    """Verify that an item is iterable.

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
    >>> is_item_iterable("abc")
    True

    """
    try:
        _ = [_ for _ in item]
    except TypeError:
        return False
    return True


def is_sequence_of_iterable(items):
    """Verify that the sequence contains only iterable items.

    Parameters
    ----------
    items : sequence
        The items.

    Returns
    -------
    bool
        True if all items in the sequence are iterable.
        False otherwise.

    Examples
    --------
    >>> is_sequence_of_iterable(["abc", [1.0], (2, "a", None)])
    True

    """
    return all(is_item_iterable(item) for item in items)
