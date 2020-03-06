from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from compas.files.gltf.data_classes import MeshData
from compas.files.gltf.gltf_node import GLTFNode
from compas.files.gltf.gltf_scene import GLTFScene
from compas.files.gltf.helpers import get_weighted_mesh_vertices
from compas.geometry import transform_points
from compas.geometry import multiply_matrices


class GLTFContent(object):
    """
    Parameters
    ----------
    scenes : Iterable of :class:`compas.files.GLTFScene`
        List or other iterable of scenes to be included in the file.
    default_scene_index : int
        Index of the scene to be displayed on loading the glTF.  Defaults to 0.
    meshes : dict
        Dictionary containing (int, :class:`compas.files.MeshData`) pairs.
    nodes : dict
        Dictionary containing (int, :class:`compas.files.GLTFNode`) pairs.
    extras : object
    ancillaries : dict
        Dictionary containing all animation, camera, and material data.
    """
    def __init__(self, scenes=None, default_scene_index=None, meshes=None, nodes=None, extras=None, ancillaries=None):
        self.scenes = scenes
        self.default_scene_index = default_scene_index
        self.meshes = meshes
        self.nodes = nodes
        self.extras = extras
        self.ancillaries = ancillaries

    def check_is_forest(self):
        # This assumes that orphans have been removed.  Maybe I should just call it...
        visited_nodes = set()

        def visit(key):
            node = self.nodes[key]
            if key in visited_nodes:
                raise Exception('Nodes do not form a rooted forest.')
            visited_nodes.add(key)
            for child_key in node.children:
                visit(child_key)

        for scene in self.scenes:
            for node_key in scene.nodes:
                visit(node_key)

    def remove_orphans(self):
        # what about cameras, etc?  that would involve reindexing, making all of those guys dicts as well
        node_visit_log = {key: False for key in self.nodes}
        mesh_visit_log = {key: False for key in self.meshes}

        def visit(key):
            node = self.nodes[key]
            node_visit_log[key] = True
            if node.mesh_key:
                mesh_visit_log[node.mesh_key] = True
            for child_key in node.children:
                visit(child_key)

        for scene in self.scenes:
            for node_key in scene.nodes:
                visit(node_key)

        for key, visited in node_visit_log.items():
            if not visited:
                del self.nodes[key]

        for key, visited in mesh_visit_log.items():
            if not visited:
                del self.meshes[key]

    def update_node_transforms_and_positions(self):
        """Method to walk through all nodes and update the transforms and positions.  To be used in
        the case that the nodes' matrices or TRS attributes have been set or updated."""
        for scene in self.scenes:
            self.update_scene_transforms_and_positions(scene)

    def update_scene_transforms_and_positions(self, scene):
        """Method to walk through the scene tree and update the transforms and positions.  To be used in
        the case that the nodes' matrices or TRS attributes have been set or updated."""
        origin = [0, 0, 0]
        for node_key in scene.nodes:
            node = self.nodes[node_key]
            node.transform = node.matrix
            node.position = transform_points([origin], node.transform)
            queue = [node_key]
            while queue:
                cur_key = queue.pop(0)
                cur = self.nodes[cur_key]
                for child_key in cur.children:
                    child = self.nodes[child_key]
                    child.transform = multiply_matrices(
                        cur.transform,
                        child.matrix or child.get_matrix_from_trs()
                    )
                    child.position = transform_points([origin], child.transform)[0]
                    queue.append(child_key)

    def find_mesh(self, mesh_key):
        if mesh_key not in self.meshes:
            raise Exception('Mesh {} not found.'.format(mesh_key))
        return self.meshes[mesh_key]

    def check_node_for_mesh(self, node):
        if node.mesh_key is None:
            raise Exception('Node {} has no attached mesh.'.format(node.key))

    def get_mesh_data_for_node(self, node):
        self.check_node_for_mesh(node)
        return self.find_mesh(node.mesh_key)

    def get_node_faces(self, node):
        mesh_data = self.get_mesh_data_for_node(node)
        return mesh_data.faces

    def get_node_vertices(self, node):
        # should i also apply the transform?
        mesh_data = self.get_mesh_data_for_node(node)
        if node.weights is None:
            return mesh_data.vertices
        return get_weighted_mesh_vertices(mesh_data, node.weights)

    def add_scene(self, name=None, extras=None):
        scene = GLTFScene(self, name=name, extras=extras)
        self.scenes.append(scene)
        return scene

    def _add_node(self, name=None, extras=None):
        node = GLTFNode(self, name=name, extras=extras)
        key = len(self.nodes)
        if key in self.nodes:
            raise Exception('!!!')
        node.key = key
        self.nodes[key] = node
        return node

    def add_node_to_scene(self, scene, node_name=None, node_extras=None):
        if scene not in self.scenes:
            raise Exception('Cannot find scene.')
        node = self._add_node(node_name, node_extras)
        scene.nodes.append(node.key)
        return node

    def add_child_to_node(self, parent_node, child_name=None, child_extras=None):
        child_node = self._add_node(child_name, child_extras)
        parent_node.children.append(child_node.key)
        return child_node

    def _add_mesh(self, mesh):
        mesh_data = MeshData.from_mesh(mesh)
        key = len(self.meshes)
        if key in self.meshes:
            raise Exception('!!!')
        mesh_data.key = key
        self.meshes[key] = mesh_data
        return mesh_data

    def add_mesh_to_node(self, node, mesh):
        if isinstance(mesh, int):
            mesh_data = self.find_mesh(mesh)
        else:
            mesh_data = self._add_mesh(mesh)
        node.mesh_key = mesh_data.key
        return mesh_data
