try:
    from Grasshopper import DataTree as Tree
    from Grasshopper.Kernel.Data import GH_Path as Path
    from System import Array
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise

__all__ = [
    'list_to_ghtree',
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
