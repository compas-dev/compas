from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from compas.files.gltf.gltf_mesh import GLTFMesh
from compas.files.gltf.gltf_node import GLTFNode
from compas.files.gltf.gltf_scene import GLTFScene
from compas.files.gltf.helpers import get_weighted_mesh_vertices
from compas.geometry import transform_points
from compas.geometry import multiply_matrices
from compas.utilities import download_file_from_remote


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
        Dictionary containing (int, :class:`compas.files.GLTFMesh`) pairs.
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

    @property
    def default_or_first_scene(self):
        key = self.default_scene_key or 0
        return self.scenes[key]

    def check_if_forest(self):
        """Raises an exception if :attr:`compas.files.GLTFContent.nodes` is not a disjoint
        union of rooted trees.

        Returns
        -------

        """
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
        """Removes orphaned objects.

        Returns
        -------

        """
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
            if node.mesh_key is not None:
                mesh_visit_log[node.mesh_key] = True
            if node.camera is not None:
                camera_visit_log[node.camera] = True
            for child_key in node.children:
                visit_node(child_key)

        # walk through scenes and update visit logs of nodes, meshes, and cameras.
        for scene in self.scenes.values():
            for node_key in scene.children:
                visit_node(node_key)

        # remove unvisited nodes
        self._remove_unvisited(node_visit_log, self.nodes)

        # remove unvisited meshes
        self._remove_unvisited(mesh_visit_log, self.meshes)

        # remove unvisited cameras
        self._remove_unvisited(camera_visit_log, self.cameras)

        # remove animations referencing no existing nodes
        for animation_key, animation in self.animations.items():
            visited_sampler_keys = []
            for channel in animation.channels:
                if not node_visit_log[channel.target.node]:
                    animation.channels.remove(channel)
                else:
                    visited_sampler_keys.append(channel.sampler)
            animation.samplers_dict = {
                key: animation.samplers_dict[key]
                for key in animation.samplers_dict
                if key in visited_sampler_keys
            }
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
            for primitive in mesh.primitive_data_list:
                if primitive.material is not None:
                    material_visit_log[primitive.material] = True

        # remove unvisited materials
        self._remove_unvisited(material_visit_log, self.materials)

        # walk through existing materials and update textures visit log
        for material in self.materials.values():
            if material.normal_texture is not None:
                texture_visit_log[material.normal_texture.index] = True
            if material.occlusion_texture is not None:
                texture_visit_log[material.occlusion_texture.index] = True
            if material.emissive_texture is not None:
                texture_visit_log[material.emissive_texture.index] = True
            if material.pbr_metallic_roughness is not None:
                if material.pbr_metallic_roughness.base_color_texture is not None:
                    texture_visit_log[material.pbr_metallic_roughness.base_color_texture.index] = True
                if material.pbr_metallic_roughness.metallic_roughness_texture is not None:
                    texture_visit_log[material.pbr_metallic_roughness.metallic_roughness_texture.index] = True

        # remove unvisited textures
        self._remove_unvisited(texture_visit_log, self.textures)

        # walk through existing textures and update visit logs of samplers and images
        for texture in self.textures.values():
            if texture.sampler is not None:
                sampler_visit_log[texture.sampler] = True
            if texture.source is not None:
                image_visit_log[texture.source] = True

        # remove unvisited samplers
        self._remove_unvisited(sampler_visit_log, self.samplers)

        # remove unvisited images
        self._remove_unvisited(image_visit_log, self.images)

    def _remove_unvisited(self, log, dictionary):
        for key, visited in log.items():
            if not visited:
                del dictionary[key]

    def update_node_transforms_and_positions(self):
        """Walks through all nodes and updates their transforms and positions.  To be used when
        scene or nodes have been added or the nodes' matrices or TRS attributes have been set or updated.

        Returns
        -------

        """
        for scene in self.scenes.values():
            self.update_scene_transforms_and_positions(scene)

    def update_scene_transforms_and_positions(self, scene):
        """Walks through the scene tree and updates transforms and positions.  To be used when
        nodes have been added or the nodes' matrices or TRS attributes have been set or updated.

        Parameters
        ----------
        scene : :class:`compas.files.GLTFScene`

        Returns
        -------

        """
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

    def get_node_faces(self, node):
        """Returns the faces of the mesh at ``node``, if any.

        Parameters
        ----------
        node : :class:`compas.files.GLTFNode`

        Returns
        -------
        list
        """
        mesh_data = self.meshes.get(node.mesh_key)
        if mesh_data is None:
            return None
        return mesh_data.faces

    def get_node_vertices(self, node):
        """Returns the vertices of the mesh at ``node``, if any.

        Parameters
        ----------
        node : :class:`compas.files.GLTFNode`

        Returns
        -------
        list
        """
        mesh_data = self.meshes.get(node.mesh_key)
        if mesh_data is None:
            return None
        if node.weights is None:
            return mesh_data.vertices
        return get_weighted_mesh_vertices(mesh_data, node.weights)

    def add_scene(self, name=None, extras=None):
        """Adds a scene to the content.

        Parameters
        ----------
        name : str
        extras : object

        Returns
        -------
        :class:`compas.files.GLTFScene`
        """
        return GLTFScene(self, name=name, extras=extras)

    def add_node_to_scene(self, scene, node_name=None, node_extras=None):
        """Creates a :class:`compas.files.GLTFNode` and adds this node to the children of ``scene``.

        Parameters
        ----------
        scene : :class:`compas.files.GLTFScene`
        node_name : str
        node_extras : object

        Returns
        -------
        :class:`compas.files.GLTFNode`
        """
        if scene not in self.scenes.values():
            raise Exception('Cannot find scene.')
        node = GLTFNode(self, node_name, node_extras)
        scene.children.append(node.key)
        return node

    def add_child_to_node(self, parent_node, child_name=None, child_extras=None):
        """Creates a :class:`compas.files.GLTFNode` and adds this node to the children of ``parent_node``.

        Parameters
        ----------
        parent_node : :class:`compas.files.GLTFNode`
        child_name : str
        child_extras : object

        Returns
        -------
        :class:`compas.files.GLTFNode`
        """
        child_node = GLTFNode(self, child_name, child_extras)
        parent_node.children.append(child_node.key)
        return child_node

    def add_mesh(self, mesh):
        """Creates a :class:`compas.files.GLTFMesh` object from a compas mesh, and adds this
        to the content.

        Parameters
        ----------
        mesh : :class:`compas.datastructures.Mesh`

        Returns
        -------
        :class:`compas.files.GLTFMesh`
        """
        return GLTFMesh.from_mesh(self, mesh)

    def add_mesh_to_node(self, node, mesh):
        """Adds an existing mesh to ``node`` if ``mesh`` is a valid mesh key, or through ``add_mesh`` creates and adds a
        mesh to ``node``.

        Parameters
        ----------
        node : :class:`compas.files.GLTFNode`
        mesh : Union[:class:`compas.datastructures.Mesh`, int]

        Returns
        -------
        :class:`compas.files.GLTFMesh`
        """
        if isinstance(mesh, int):
            mesh_data = self.meshes[mesh]
        else:
            mesh_data = self.add_mesh(mesh)
        node.mesh_key = mesh_data.key
        return mesh_data

    def get_nodes_from_scene(self, scene):
        """Returns dictionary of nodes in the given scene, without a specified root.

        Parameters
        ----------
        scene : :class:`compas.files.GLTFScene`

        Returns
        -------
        dict
        """
        node_dict = {}

        def visit(key):
            node_dict[key] = self.nodes[key]
            for child in self.nodes[key].children:
                visit(child)

        for child_key in scene.children:
            visit(child_key)

        return node_dict

    def get_scene_positions_and_edges(self, scene):
        """Returns a tuple containing a dictionary of positions and a list of tuples representing edges.

        Parameters
        ----------
        scene : :class:`compas.files.GLTFScene`

        Returns
        -------
        tuple
        """
        positions_dict = {'root': [0, 0, 0]}
        edges_list = []

        def visit(node, key):
            for child_key in node.children:
                positions_dict[child_key] = self.nodes[child_key].position
                edges_list.append((key, child_key))
                visit(self.nodes[child_key], child_key)

        visit(scene, 'root')

        return positions_dict, edges_list


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import os
    import compas

    from compas.datastructures import Mesh
    from compas.files.gltf.gltf import GLTF

    source = 'https://raw.githubusercontent.com/ros-industrial/abb/kinetic-devel/abb_irb6600_support/meshes/irb6640/visual/link_1.stl'
    stl_filepath = os.path.join(compas.APPDATA, 'data', 'meshes', 'ros', 'link_1.stl')

    download_file_from_remote(source, stl_filepath, overwrite=False)

    gltf_filepath = os.path.join(compas.APPDATA, 'data', 'gltfs', 'double_link_1.gltf')

    mesh = Mesh.from_stl(stl_filepath)
    cnt = GLTFContent()
    scene = cnt.add_scene()
    node_1 = scene.add_child(node_name='Node1')
    mesh_data = node_1.add_mesh(mesh)
    node_2 = node_1.add_child(child_name='Node2')
    node_2.translation = [0, 0, 5]
    node_2.add_mesh(mesh_data.key)

    gltf = GLTF(gltf_filepath)
    gltf.content = cnt
    gltf.export(embed_data=True)
