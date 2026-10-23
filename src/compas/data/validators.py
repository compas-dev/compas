from typing import Any


def is_item_iterable(item: Any) -> bool:
    """Determine whether an item implements the iterator protocol.

    Parameters
    ----------
    item
        The item to check.

    Returns
    -------
    bool
        Whether the item is iterable.

    """
    try:
        iter(item)
    except TypeError:
        return False
    return True
