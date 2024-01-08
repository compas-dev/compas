********************************************************************************
Trees
********************************************************************************

.. rst-class:: lead

A :class:`compas.datastructures.Tree` is a data structure that can be used to
represent hierarchical relationships between data. It starts with a single root
node, and each node can have a number of children nodes. Each node can
store arbitrary attributes.


.. note::

    Please refer to the API for a complete overview of all functionality:

    * :class:`compas.datastructures.Tree`

Tree Construction
=================

Trees can be constructed in a number of ways:
* by adding nodes to a tree instance, specifiying parent node,
* by adding nodes directly to another node instance that belongs to a tree, or
* directly loaded from a serilised json file.

Adding To Tree
--------------

>>> from compas.datastructures import Tree
>>> from compas.datastructures import TreeNode
>>> tree = Tree()
>>> root_node = TreeNode('root')
>>> tree.add(root_node)
>>> branch_node = TreeNode('branch')
>>> tree.add(branch_node, parent=root_node)
>>> leaf_node1 = TreeNode('leaf1')
>>> tree.add(leaf_node1, parent=branch_node)
>>> leaf_node2 = TreeNode('leaf2')
>>> tree.add(leaf_node2, parent=branch_node)
>>> tree.print_hierarchy()
└── <TreeNode root>
    └── <TreeNode branch>
        ├── <TreeNode leaf1>
        └── <TreeNode leaf2>

Adding To Node
--------------

>>> from compas.datastructures import Tree
>>> from compas.datastructures import TreeNode
>>> tree = Tree()
>>> root_node = TreeNode('root')
>>> tree.add(root_node)
>>> branch_node = TreeNode('branch')
>>> root_node.add(branch_node)
>>> leaf_node1 = TreeNode('leaf1')
>>> branch_node.add(leaf_node1)
>>> leaf_node2 = TreeNode('leaf2')
>>> branch_node.add(leaf_node2)
└── <TreeNode root>
    └── <TreeNode branch>
        ├── <TreeNode leaf1>
        └── <TreeNode leaf2>

Loading From File
-----------------

>>> from compas.data import json_load
>>> tree = json_load('tree.json')
>>> tree.print_hierarchy()
└── <TreeNode root>
    └── <TreeNode branch>
        ├── <TreeNode leaf1>
        └── <TreeNode leaf2>

Remove Node
-----------

>>> tree.remove(leaf_node2) # Or branch_node.remove(leaf_node2)
>>> tree.print_hierarchy()
└── <TreeNode root>
    └── <TreeNode branch>
        └── <TreeNode leaf1>


Tree Traversal
==============
The tree can be traversed in a number of ways, including depth-first and breadth-first.
For depth-first traversal, there are additional options for pre-order and post-order.

Depth-First
-----------
The algorithm starts at the root node and explores as far as possible along each branch before backtracking. 
The traversal can be done in pre-orderor post-order. In pre-order, the parent node is visited before its children. In post-order,
the parent node is visited after its children.

>>> from compas.datastructures import Tree
>>> from compas.datastructures import TreeNode
>>> tree = Tree()
>>> root_node = TreeNode('root')
>>> tree.add(root_node)
>>> branch_node1 = TreeNode('branch1')
>>> root_node.add(branch_node1)
>>> leaf_node1 = TreeNode('leaf1')
>>> branch_node1.add(leaf_node1)
>>> leaf_node2 = TreeNode('leaf2')
>>> branch_node1.add(leaf_node2)
>>> branch_node2 = TreeNode('branch2')
>>> root_node.add(branch_node2)
>>> leaf_node3 = TreeNode('leaf3')
>>> branch_node2.add(leaf_node3)
>>> leaf_node4 = TreeNode('leaf4')
>>> branch_node2.add(leaf_node4)
>>> tree.print_hierarchy()
└── <TreeNode root>
    ├── <TreeNode branch1>
    │   ├── <TreeNode leaf1>
    │   └── <TreeNode leaf2>
    └── <TreeNode branch2>
        ├── <TreeNode leaf3>
        └── <TreeNode leaf4>

>>> for node in tree.traverse(strategy='depthfirst', order='preorder'):
...     print(node)
<TreeNode root>
<TreeNode branch1>
<TreeNode leaf1>
<TreeNode leaf2>
<TreeNode branch2>
<TreeNode leaf3>
<TreeNode leaf4>

>>> for node in tree.traverse(strategy='depthfirst', order='postorder'):
...     print(node)
<TreeNode leaf1>
<TreeNode leaf2>
<TreeNode branch1>
<TreeNode leaf3>
<TreeNode leaf4>
<TreeNode branch2>
<TreeNode root>


Breadth-First
-------------
The algorithm starts at the root node and explores the neighbour nodes first, before moving to the next level neighbours.

>>> for node in tree.traverse(strategy='breadthfirst'):
...     print(node)
<TreeNode root>
<TreeNode branch1>
<TreeNode branch2>
<TreeNode leaf1>
<TreeNode leaf2>
<TreeNode leaf3>
<TreeNode leaf4>


Node Attributes
===============

>>> nodes = tree.get_nodes_by_name('branch1')
>>> nodes
[<TreeNode branch1>]

>>> node = tree.get_node_by_name('branch1')
>>> node
<TreeNode branch1>

>>> node.is_root
False
>>> node.is_leaf
False
>>> node.is_branch
True

>>> node.parent
<TreeNode root>
>>> node.children
[<TreeNode leaf1>, <TreeNode leaf2>]

>>> leaf1 = node.children[0]
>>> list(leaf1.ancestors)
[<TreeNode branch1>, <TreeNode root>]
>>> root = leaf1.ancestors[-1]
>>> list(root.descendants)
[<TreeNode branch1>, <TreeNode leaf1>, <TreeNode leaf2>, <TreeNode branch2>, <TreeNode leaf3>, <TreeNode leaf4>]

