from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from compas.files.gltf.constants import DEFAULT_ROOT_NAME
from compas.files.gltf.gltf_node import GLTFNode
from compas.geometry import identity_matrix
from compas.geometry import multiply_matrices
from compas.geometry import transform_points


class GLTFScene(object):
    """Object representing the base of a scene.

    Attributes
    ----------
    name : str
        Name of the scene.
    nodes : dict
        Dictionary of (node_key, :class:`compas.files.GLTFNode`) pairs.
        Node representing the root must be named ``compas.files.DEFAULT_ROOT_NAME``.
    extras : object
    """
    def __init__(self):
        self.name = None
        self.nodes = {}
        root_node = self.get_default_root_node()
        self.nodes[root_node.name] = root_node

        self.extras = None

    def get_default_root_node(self):
        root_node = GLTFNode()
        root_node.name = DEFAULT_ROOT_NAME
        root_node.node_key = DEFAULT_ROOT_NAME
        root_node.position = [0, 0, 0]
        root_node.transform = identity_matrix(4)
        root_node.matrix = identity_matrix(4)
        root_node.children = []
        return root_node

    def update_node_transforms_and_positions(self):
        """Method to walk through the tree and update the transforms and positions.  To be used in
        the case that the nodes' matrices or TRS attributes have been set or updated."""
        queue = [DEFAULT_ROOT_NAME]
        while queue:
            cur_key = queue.pop(0)
            cur = self.nodes[cur_key]
            for child_key in cur.children:
                child = self.nodes[child_key]
                child.transform = multiply_matrices(
                    cur.transform,
                    child.matrix or child.get_matrix_from_trs()
                )
                child.position = transform_points([self.nodes[DEFAULT_ROOT_NAME].position], child.transform)[0]
                queue.append(child_key)

    def is_tree(self, msg, object_name):
        visited = {node_key: False for node_key in self.nodes}
        queue = [DEFAULT_ROOT_NAME]
        while queue:
            cur = queue.pop(0)
            if visited[cur]:
                raise Exception(msg.format(object_name))
            visited[cur] = True
            queue.extend(self.nodes[cur].children)
        return True

    def find_node(self, key):
        if key not in self.nodes:
            raise Exception('Cannot find node {}.'.format(key))
        return self.nodes[key]

    def add_node_as_leaf(self, node, parent_key):
        if not isinstance(node, GLTFNode):
            raise Exception('Expected node to be of type GLTFNode.')
        if node.node_key is None:
            node.node_key = len(self.nodes)
        if node.node_key in self.nodes:
            raise Exception('Node with key {} already exists in this scene.'.format(node.node_key))
        parent = self.find_node(parent_key)
        self.nodes[node.node_key] = node
        parent.children.append(node.node_key)
        node.children = []
