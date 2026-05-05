from typing import Any
from typing import Iterable
from typing import Sequence
from typing import cast


def is_sequence_of_str(items: Iterable[Any]) -> bool:
    """Verify that the sequence contains only items of type str.

    Parameters
    ----------
    items
        The sequence of items.

    Returns
    -------
    bool
        True if all items are strings.
        False otherwise.

    Examples
    --------
    >>> is_sequence_of_str(["a", "b", "c"])
    True
    >>> is_sequence_of_str(["a", 1, "c"])
    False

    """
    return all(isinstance(item, str) for item in items)


def is_sequence_of_int(items: Iterable[Any]) -> bool:
    """Verify that the sequence contains only integers.

    Parameters
    ----------
    items
        The sequence of items.

    Returns
    -------
    bool

    Examples
    --------
    >>> is_sequence_of_int([1, 2, 3])
    True
    >>> is_sequence_of_int([1, 2.0, 3])
    False

    """
    return all(isinstance(item, int) for item in items)


def is_int3(items: Sequence[Any]) -> bool:
    """Verify that the sequence contains 3 integers.

    Parameters
    ----------
    items
        The sequence of items.

    Returns
    -------
    bool

    Examples
    --------
    >>> is_int3([1, 2, 3])
    True
    >>> is_int3([1, 2, 3, 4])
    False

    """
    return len(items) == 3 and all(isinstance(item, int) for item in items)


def is_sequence_of_float(items: Iterable[Any]) -> bool:
    """Verify that the sequence contains only floats.

    Parameters
    ----------
    items
        The sequence of items.

    Returns
    -------
    bool

    Examples
    --------
    >>> is_sequence_of_float([1.0, 2.0, 3.0])
    True
    >>> is_sequence_of_float([1.0, 2, 3.0])
    False

    """
    return all(isinstance(item, float) for item in items)


def is_sequence_of_uint(items: Iterable[Any]) -> bool:
    """Verify that the sequence contains only unsigned integers.

    Parameters
    ----------
    items
        The sequence of items.

    Returns
    -------
    bool

    Examples
    --------
    >>> is_sequence_of_uint([0, 1, 2])
    True
    >>> is_sequence_of_uint([0, -1, 2])
    False

    """
    return all(isinstance(item, int) and item >= 0 for item in items)


def is_float3(items: Sequence[Any]) -> bool:
    """Verify that the sequence contains 3 floats.

    Parameters
    ----------
    items
        The sequence of items.

    Returns
    -------
    bool

    Examples
    --------
    >>> is_float3([1.0, 2.0, 3.0])
    True
    >>> is_float3([1.0, 2.0, 3])
    False

    """
    return len(items) == 3 and all(isinstance(item, float) for item in items)


def is_float4x4(items: Sequence[Sequence[Any]]) -> bool:
    """Verify that the sequence contains 4 sequences of each 4 floats.

    Parameters
    ----------
    items
        The sequence of items.

    Returns
    -------
    bool

    Examples
    --------
    >>> is_float4x4([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
    True
    >>> is_float4x4([[1.0, 0.0], [0.0, 1.0]])
    False

    """
    return len(items) == 4 and all(len(item) == 4 and all(isinstance(i, float) for i in item) for item in items)


def is_sequence_of_list(items: Iterable[Any]) -> bool:
    """Verify that the sequence contains only items of type list.

    Parameters
    ----------
    items
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
    >>> is_sequence_of_list([[1], (1,), [1]])
    False

    """
    return all(isinstance(item, list) for item in items)


def is_sequence_of_tuple(items: Iterable[Any]) -> bool:
    """Verify that the sequence contains only items of type tuple.

    Parameters
    ----------
    items
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
    >>> is_sequence_of_tuple([(1,), [1], (1,)])
    False

    """
    return all(isinstance(item, tuple) for item in items)


def is_sequence_of_dict(items: Iterable[Any]) -> bool:
    """Verify that the sequence contains only items of type dict.

    Parameters
    ----------
    items
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
    >>> is_sequence_of_dict([{"a": 1}, ["b", 2], {"c": 3}])
    False

    """
    return all(isinstance(item, dict) for item in items)


def is_item_iterable(item: object) -> bool:
    """Verify that an item is iterable.

    Parameters
    ----------
    item
        The item to test.

    Returns
    -------
    bool
        True if the item is iterable.
        False otherwise.

    Examples
    --------
    >>> is_item_iterable("abc")
    True
    >>> is_item_iterable(1.0)
    False

    """
    try:
        _ = [_ for _ in cast(Iterable[Any], item)]
    except TypeError:
        return False
    return True


def is_sequence_of_iterable(items: Iterable[Any]) -> bool:
    """Verify that the sequence contains only iterable items.

    Parameters
    ----------
    items
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
    >>> is_sequence_of_iterable(["abc", 1.0, (2, "a", None)])
    False

    """
    return all(is_item_iterable(item) for item in items)
