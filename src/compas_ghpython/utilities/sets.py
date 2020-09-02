from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from System import Array

from Grasshopper import DataTree as Tree
from Grasshopper.Kernel.Data import GH_Path as Path


__all__ = [
    'list_to_ghtree',
    'ghtree_to_list',
]


def list_to_ghtree(items, none_and_holes=False, base_path=[0]):
    """Transforms nestings of lists or tuples to a Grasshopper DataTree.

    Parameters
    ----------
    items : list
        Nesting of lists and/or tuples.
    none_and_holes : bool, optional
    base_path : list, optional

    Examples
    --------
    >>> items = [[1, 2], 3, [], [4, [5]]]
    >>> a = list_to_tree(items)
    >>> b = list_to_tree(items, none_and_holes=True, base_path=[7, 1])

    """
    def process_one_item(items, tree, track):
        path = Path(Array[int](track))
        if len(items) == 0 and none_and_holes:
            tree.EnsurePath(path)
            return
        for i, item in enumerate(items):
            if hasattr(item, '__iter__'):
                track.append(i)
                process_one_item(item, tree, track)
                track.pop()
            else:
                if none_and_holes:
                    tree.Insert(item, path, i)
                elif item is not None:
                    tree.Add(item, path)
    tree = Tree[object]()
    if items is not None:
        process_one_item(items, tree, base_path[:])
    return tree


def ghtree_to_list(tree):
    """Returns a list representation of a Grasshopper DataTree

    Parameters
    ----------
    tree : :class:`Grasshopper.DataTree`

    Returns
    -------
    list

    Examples
    --------
    >>> tree = Tree[object]()
    >>> [tree.Add(str("entry: " + str(i)), Path(Array[int]([i]))) for i in range(3)]
    >>> items = ghtree_to_list(tree)

    """
    def extend_at(path, index, simple_input, rest_list):
        target = path[index]
        if len(rest_list) <= target:
            rest_list.extend([None] * (target - len(rest_list) + 1))
        if index == path.Length - 1:
            rest_list[target] = list(simple_input)
        else:
            if rest_list[target] is None:
                rest_list[target] = []
            extend_at(path, index + 1, simple_input, rest_list[target])
    items = []
    for i in range(tree.BranchCount):
        path = tree.Path(i)
        extend_at(path, 0, tree.Branch(path), items)
    return items


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
