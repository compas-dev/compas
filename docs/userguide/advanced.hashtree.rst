********************************************************************************
Hash Tree
********************************************************************************

Hash tree (or Merkle tree) is a tree data structure in which every leaf node is labelled with the hash of a data block and every non-leaf node is labelled with the cryptographic hash of the labels of its child nodes. 
Hash trees are useful because they allow efficient and secure verification of the contents of large data structures. It is widly used in modern distributed version control systems like Git as well as peer-to-peer systems like Blockchain.
COMPAS provides a simple implementation of a hash tree that can be used for detecting and locating changes in a complex data structure. In context of AEC, this feature can also be useful for many real-world applications,
such as detecting changes in a complicated Building Information Model, tracking minor deformation in structural assessments, or even detecting robot joint movements in a digital fabracation process, and many more. 

Hash Tree From Dict
===================

A COMPAS hash tree can be created from any raw python dictionary using the `HashTree.from_dict` method.

>>> from compas.datastructures import HashTree
>>> data = {'a': 1, 'b': 2, 'c': {'d': 3, 'e': 4}}
>>> tree = HashTree.from_dict(data)

The structure of the hash tree and crypo hash on each node can be visualised using the `print` function.

>>> print(tree)
<Tree with 6 nodes>
└── ROOT @ b2e1c
    ├── .a:1 @ 4d9a8
    ├── .b:2 @ 82b86
    └── .c @ 664a3
        ├── .d:3 @ 76d82
        └── .e:4 @ ebe84

Once the original data is modified, a new hash tree can be created from the modified data and the changes can be detected by comparing the two hash trees.

>>> data['c']['d'] = 5
>>> del data["b"]
>>> data["f"] = True
>>> new_tree = HashTree.from_dict(data)
>>> print(new_tree)
<Tree with 6 nodes>
└── ROOT @ a8c1b
    ├── .a:1 @ 4d9a8
    ├── .c @ e1701
    │   ├── .d:5 @ 98b1e
    │   └── .e:4 @ ebe84
    └── .f:True @ 753e5

>>> new_tree.diff(tree)
{'added': [{'path': '.f', 'value': True}], 'removed': [{'path': '.b', 'value': 2}], 'modified': [{'path': '.c.d', 'old': 3, 'new': 5}]}

Hash Tree From COMPAS Data
==========================

A COMPAS hash tree can also be created from any classes that inherit from the base `Data` class in COMPAS, such as `Mesh`, `Graph`, `Shape`, `Geometry`, etc.
This is done by hashing the serilised data of the object.

>>> from compas.datastructures import Mesh
>>> mesh = Mesh.from_polyhedron(6)
>>> tree = HashTree.from_object(mesh)
>>> print(tree)
<Tree with 58 nodes>
└── ROOT @ 44cc1
    ├── .attributes @ 3370c
    ├── .default_vertex_attributes @ 84700
    │   ├── .x:0.0 @ 5bc2d
    │   ├── .y:0.0 @ 1704b
    │   └── .z:0.0 @ 6199e
    ├── .default_edge_attributes @ 5e834
    ├── .default_face_attributes @ 5a8d9
    ├── .vertex @ ff6d0
    │   ├── .0 @ 84ec1
    │   │   ├── .x:-1.1547005383792517 @ 874f4
    │   │   ├── .y:-1.1547005383792517 @ d2b16
    │   │   └── .z:-1.1547005383792517 @ bd9f0
    │   ├── .1 @ 316d3
...

>>> mesh.vertex_attribute(0, "x", 1.0)
>>> mesh.delete_face(3)
>>> new_tree = HashTree.from_object(mesh)
>>> new_tree.diff(tree)
{'added': [], 'removed': [{'path': '.face.3', 'value': [4, 2, 3, 5]}, {'path': '.facedata.3', 'value': None}], 'modified': [{'path': '.vertex.0.x', 'old': -1.1547005383792517, 'new': 1.0}]}

