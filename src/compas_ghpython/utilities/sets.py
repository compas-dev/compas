from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

try:
    from Grasshopper import DataTree as Tree
    from Grasshopper.Kernel.Data import GH_Path as Path
    from System import Array
except ImportError:
    compas.raise_if_ironpython()


__all__ = [
    'list_to_ghtree',
    'ghtree_to_list',
]


def list_to_ghtree(alist, none_and_holes=False, base_path=[0]):
    """Transforms nestings of lists or tuples to a Grasshopper DataTree.

    Examples:
        >>> mytree = [ [1,2], 3, [],[ 4,[5]] ]
        >>> a = list_to_tree(mytree)
        >>> b = list_to_tree(mytree, none_and_holes=True, base_path=[7,1])
    """
    def process_one_item(alist, tree, track):
        path = Path(Array[int](track))
        if len(alist) == 0 and none_and_holes:
            tree.EnsurePath(path)
            return
        for i, item in enumerate(alist):
            if hasattr(item, '__iter__'):  # if list or tuple
                track.append(i)
                process_one_item(item, tree, track)
                track.pop()
            else:
                if none_and_holes:
                    tree.Insert(item, path, i)
                elif item is not None:
                    tree.Add(item, path)

    tree = Tree[object]()
    if alist is not None:
        process_one_item(alist, tree, base_path[:])
    return tree


def ghtree_to_list(atree):
    """Returns a list representation of a Grasshopper DataTree

    Examples:
        >>> atree=Tree[object]()
        >>> [atree.Add(str("entry: " + str(i)), Path(Array[int]([i]))) for i in range(3)]
        >>> alist = ghtree_to_list(atree)
    """
    def extend_at(path, index, simple_input, rest_list):
        target = path[index]
        if len(rest_list) <= target: 
            rest_list.extend([None]*(target-len(rest_list)+1))
        if index == path.Length - 1:
            rest_list[target] = list(simple_input)
        else:
            if rest_list[target] is None: 
                rest_list[target] = []
            extend_at(path, index+1, simple_input, rest_list[target])
            
    all = []
    for i in range(atree.BranchCount):
        path = atree.Path(i)
        extend_at(path, 0, atree.Branch(path), all)
    return all