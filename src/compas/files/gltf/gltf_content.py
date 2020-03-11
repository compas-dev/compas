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
    Class for managing the content of a glTF file.
    Attributes
    ----------
    scenes : dict
        Dictionary containing (int, :class:`compas.files.GLTFScene`) pairs.
    default_scene_key : int or None
        Key of the scene to be displayed on loading the glTF.
    nodes : dict
        Dictionary containing (int, :class:`compas.files.GLTFNode`) pairs.
    meshes : dict
        Dictionary containing (int, :class:`compas.files.MeshData`) pairs.
    cameras : dict
        Dictionary containing (int, :class:`compas.files.data_classes.CameraData`) pairs.
    animations : dict
        Dictionary containing (int, :class:`compas.files.data_classes.AnimationData`) pairs.
    skins : dict
        Dictionary containing (int, :class:`compas.files.data_classes.SkinData`) pairs.
    materials : dict
        Dictionary containing (int, :class:`compas.files.data_classes.MaterialData`) pairs.
    textures : dict
        Dictionary containing (int, :class:`compas.files.data_classes.TextureData`) pairs.
    samplers : dict
        Dictionary containing (int, :class:`compas.files.data_classes.SamplerData`) pairs.
    images : dict
        Dictionary containing (int, :class:`compas.files.data_classes.ImageData`) pairs.
    extras : object
    extensions : object
    """
    def __init__(self):
        self.scenes = {}
        self.default_scene_key = None
        self.nodes = {}
        self.meshes = {}
        self.cameras = {}
        self.animations = {}
        self.skins = {}
        self.materials = {}
        self.textures = {}
        self.samplers = {}
        self.images = {}
        self.extras = None
        self.extensions = None

    def check_is_forest(self):
        visited_nodes = set()

        def visit(key):
            node = self.nodes[key]
            if key in visited_nodes:
                raise Exception('Nodes do not form a rooted forest.')
            visited_nodes.add(key)
            for child_key in node.children:
                visit(child_key)

        for scene in self.scenes.values():
            for node_key in scene.children:
                visit(node_key)

    def remove_orphans(self):
        node_visit_log = {key: False for key in self.nodes}
        mesh_visit_log = {key: False for key in self.meshes}
        camera_visit_log = {key: False for key in self.cameras}
        material_visit_log = {key: False for key in self.materials}
        texture_visit_log = {key: False for key in self.textures}
        sampler_visit_log = {key: False for key in self.samplers}
        image_visit_log = {key: False for key in self.images}

        def visit_node(key):
            node = self.nodes[key]
            node_visit_log[key] = True
            if node.mesh_key:
                mesh_visit_log[node.mesh_key] = True
            if node.camera:
                camera_visit_log[node.camera] = True
            for child_key in node.children:
                visit_node(child_key)

        # walk through scenes and update visit logs of nodes, meshes, and cameras.
        for scene in self.scenes.values():
            for node_key in scene.children:
                visit_node(node_key)

        # remove unvisited nodes
        for key, visited in node_visit_log.items():
            if not visited:
                del self.nodes[key]

        # remove unvisited meshes
        for key, visited in mesh_visit_log.items():
            if not visited:
                del self.meshes[key]

        # remove unvisited cameras
        for key, visited in camera_visit_log.items():
            if not visited:
                del self.cameras[key]

        # remove animations referencing no existing nodes
        for animation_key, animation in self.animations.items():
            visited_sampler_keys = []
            for channel in animation.channels:
                if not node_visit_log[channel.target.node]:
                    animation.channels.remove(channel)
                else:
                    visited_sampler_keys.append(channel.sampler)
            animation.samplers_dict = {key: value for key, value in animation.samplers_dict if key in visited_sampler_keys}
            if not animation.samplers_dict:
                del self.animations[animation_key]

        # remove skins referencing no existing nodes
        for key, skin_data in self.skins.items():
            for joint_key in skin_data.joints:
                if not node_visit_log[joint_key]:
                    skin_data.joints.remove(joint_key)
            if not skin_data.joints:
                del self.skins[key]

        # walk through existing meshes and update materials visit log
        for mesh in self.meshes.values():
            if mesh.material:
                material_visit_log[mesh.material] = True

        # remove unvisited materials
        for key, visited in material_visit_log.items():
            if not visited:
                del self.materials[key]

        # walk through existing materials and update textures visit log
        for material in self.materials.values():
            if material.normal_texture:
                texture_visit_log[material.normal_texture.index] = True
            if material.occlusion_texture:
                texture_visit_log[material.occlusion_texture.index] = True
            if material.emissive_texture:
                texture_visit_log[material.emissive_texture.index] = True
            if material.pbr_metallic_roughness:
                if material.pbr_metallic_roughness.base_color_texture:
                    texture_visit_log[material.pbr_metallic_roughness.base_color_texture.index] = True
                if material.pbr_metallic_roughness.metallic_roughness_texture:
                    texture_visit_log[material.pbr_metallic_roughness.metallic_roughness_texture.index] = True

        # remove unvisited textures
        for key, visited in texture_visit_log.items():
            if not visited:
                del self.textures[key]

        # walk through existing textures and update visit logs of samplers and images
        for texture in self.textures.values():
            if texture.sampler:
                sampler_visit_log[texture.sampler] = True
            if texture.source:
                image_visit_log[texture.source] = True

        # remove unvisited samplers
        for key, visited in sampler_visit_log.items():
            if not visited:
                del self.samplers[key]

        # remove unvisited images
        for key, visited in image_visit_log.items():
            if not visited:
                del self.images[key]

    def update_node_transforms_and_positions(self):
        """Method to walk through all nodes and update their transforms and positions.  To be used in
        the case that the nodes' matrices or TRS attributes have been set or updated."""
        for scene in self.scenes.values():
            self.update_scene_transforms_and_positions(scene)

    def update_scene_transforms_and_positions(self, scene):
        """Method to walk through the scene tree and update the transforms and positions.  To be used in
        the case that the nodes' matrices or TRS attributes have been set or updated."""
        origin = [0, 0, 0]
        for node_key in scene.children:
            node = self.nodes[node_key]
            node.transform = node.matrix or node.get_matrix_from_trs()
            node.position = transform_points([origin], node.transform)[0]
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

    def get_mesh_data_for_node(self, node):
        if node.mesh_key is None:
            return None
        return self.find_mesh(node.mesh_key)

    def get_node_faces(self, node):
        mesh_data = self.get_mesh_data_for_node(node)
        return mesh_data.faces

    def get_node_vertices(self, node):
        mesh_data = self.get_mesh_data_for_node(node)
        if node.weights is None:
            return mesh_data.vertices
        return get_weighted_mesh_vertices(mesh_data, node.weights)

    def add_scene(self, name=None, extras=None):
        return GLTFScene(self, name=name, extras=extras)

    def add_node_to_scene(self, scene, node_name=None, node_extras=None):
        if scene not in self.scenes:
            raise Exception('Cannot find scene.')
        node = GLTFNode(self, node_name, node_extras)
        scene.nodes.append(node.key)
        return node

    def add_child_to_node(self, parent_node, child_name=None, child_extras=None):
        child_node = GLTFNode(self, child_name, child_extras)
        parent_node.children.append(child_node.key)
        return child_node

    def add_mesh(self, mesh):
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
            mesh_data = self.add_mesh(mesh)
        node.mesh_key = mesh_data.key
        return mesh_data

    def get_nodes_from_scene(self, scene):
        """Returns dictionary of nodes in the given scene, without a specified root."""
        node_dict = {}

        def visit(key):
            node_dict[key] = self.nodes[key]
            for child in self.nodes[key].children:
                visit(child)

        for child_key in scene.children:
            visit(child_key)

        return node_dict

    def get_scene_positions_and_edges(self, scene):
        """Returns a tuple containing a dictionary of positions and a list of tuples representing edges."""
        positions_dict = {'root': [0, 0, 0]}
        edges_list = []

        def visit(node, key):
            for child_key in node.children:
                positions_dict[child_key] = self.nodes[child_key].position
                edges_list.append((key, child_key))
                visit(self.nodes[child_key], child_key)

        visit(scene, 'root')

        return positions_dict, edges_list
