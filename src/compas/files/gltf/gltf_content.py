from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.files.gltf.data_classes import TextureInfoData
from compas.files.gltf.gltf_mesh import GLTFMesh
from compas.files.gltf.gltf_node import GLTFNode
from compas.files.gltf.gltf_scene import GLTFScene
from compas.files.gltf.helpers import get_weighted_mesh_vertices
from compas.geometry import multiply_matrices
from compas.geometry import transform_points


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
        self.extensions_used = None

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
                raise Exception("Nodes do not form a rooted forest.")
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
            animation.samplers_dict = {key: animation.samplers_dict[key] for key in animation.samplers_dict if key in visited_sampler_keys}
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
        def check_extensions_texture_recursively(item):
            # get the extensions that are in the attributes
            for a in dir(item):
                if not a.startswith("__") and not callable(getattr(item, a)):
                    # ipy does not like this one: if isinstance(getattr(item, a), TextureInfoData):
                    if getattr(getattr(item, a), "IS_TEXTURE_INFO_DATA", False):
                        texture_visit_log[getattr(item, a).index] = True
                    # ipy does not like this one: elif isinstance(getattr(item, a), BaseGLTFDataClass):
                    elif getattr(getattr(item, a), "IS_BASE_GLTF_DATA", False):
                        check_extensions_texture_recursively(getattr(item, a))
            if item.extensions is not None:
                for _, e in item.extensions.items():
                    check_extensions_texture_recursively(e)

        for material in self.materials.values():
            check_extensions_texture_recursively(material)

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
                    child.transform = multiply_matrices(cur.transform, child.matrix or child.get_matrix_from_trs())
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

    def get_node_by_name(self, name):
        """Returns the node with a specific name.

        Parameters
        ----------
        name : str
            The name of the node

        Returns
        -------
        node : :class:`compas.files.GLTFNode` or `None`
        """
        for key in self.nodes:
            if self.nodes[key].name == name:
                return self.nodes[key]
        return None

    @classmethod
    def _get_next_available_key(cls, adict):
        key = len(adict)
        while key in adict:
            key += 1
        return key

    def add_material(self, material):
        """Adds a material to the content.

        Parameters
        ----------
        material : :class:`compas.files.data_classes.MaterialData`
            The material to add

        Returns
        -------
        int
        """
        key = self._get_next_available_key(self.materials)
        self.materials[key] = material
        return key

    def add_texture(self, texture):
        """Adds a texture to the content.

        Parameters
        ----------
        texture : :class:`compas.files.data_classes.TextureData`
            The texture to add

        Returns
        -------
        int
        """
        key = self._get_next_available_key(self.textures)
        self.textures[key] = texture
        return key

    def add_image(self, image):
        """Adds an image to the content.

        Parameters
        ----------
        image : :class:`compas.files.data_classes.ImageData`
            The image to add

        Returns
        -------
        int
        """
        key = self._get_next_available_key(self.images)
        self.images[key] = image
        return key

    def get_material_index_by_name(self, name):
        """Returns the index of the material.

        Parameters
        ----------
        name : str
            The name of the material

        Returns
        -------
        int or None
        """
        for key, material in self.materials.items():
            if material.name == name:
                return key
        return None

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
            raise Exception("Cannot find scene.")
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
        positions_dict = {"root": [0, 0, 0]}
        edges_list = []

        def visit(node, key):
            for child_key in node.children:
                positions_dict[child_key] = self.nodes[child_key].position
                edges_list.append((key, child_key))
                visit(self.nodes[child_key], child_key)

        visit(scene, "root")

        return positions_dict, edges_list


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    import os
    import urllib

    import compas
    from compas.datastructures import Mesh
    from compas.files.gltf.data_classes import ImageData
    from compas.files.gltf.data_classes import MaterialData
    from compas.files.gltf.data_classes import MineType
    from compas.files.gltf.data_classes import PBRMetallicRoughnessData
    from compas.files.gltf.data_classes import TextureData
    from compas.files.gltf.extensions import KHR_materials_pbrSpecularGlossiness
    from compas.files.gltf.extensions import KHR_Texture_Transform
    from compas.files.gltf.gltf import GLTF
    from compas.geometry import Box
    from compas.geometry import Frame
    from compas.utilities import download_file_from_remote

    dirname = os.path.join(compas.APPDATA, "data", "gltfs")
    gltf_filepath = os.path.join(dirname, "compas.gltf")

    image_uri = "compas_icon_white.png"
    image_file = os.path.join(dirname, image_uri)
    try:
        download_file_from_remote("https://compas.dev/images/compas_icon_white.png", image_file)
    except urllib.error.HTTPError:
        pass

    cnt = GLTFContent()
    scene = cnt.add_scene()

    # image's uri should be the relative path to the image from the filepath given at the time of export,
    # so if the image will sit in the same directory as the resultant gltf, the uri is just the name of the file.
    # it's the exporter's job to manage how things are stored in the buffer, and it would only store image data
    # in the buffer if it is exporting as glb. otherwise the uri will just stay the relative path to the image
    # and the gltf only makes sense when bundled with these external files.
    image_data = ImageData(
        name=image_uri,
        mime_type=MineType.PNG,
        uri=image_file,
    )
    image_idx = cnt.add_image(image_data)
    # TextureData.source takes the key of the ImageData that it should use as 'source'
    texture = TextureData(source=image_idx)
    texture_idx = cnt.add_texture(texture)

    texture = TextureData(source=image_idx)
    texture_idx2 = cnt.add_texture(texture)

    material = MaterialData()
    material.name = "Texture"
    material.pbr_metallic_roughness = PBRMetallicRoughnessData()
    material.pbr_metallic_roughness.metallic_factor = 0.0
    material.pbr_metallic_roughness.base_color_texture = TextureInfoData(index=texture_idx)
    material_key = cnt.add_material(material)

    # add extension
    pbr_specular_glossiness = KHR_materials_pbrSpecularGlossiness()
    pbr_specular_glossiness.diffuse_factor = [
        0.980392158,
        0.980392158,
        0.980392158,
        1.0,
    ]
    pbr_specular_glossiness.specular_factor = [0.0, 0.0, 0.0]
    pbr_specular_glossiness.glossiness_factor = 0.0
    texture_transform = KHR_Texture_Transform()
    texture_transform.rotation = 0.0
    texture_transform.scale = [2.0, 2.0]
    # same here, TextureInfoData uses the key of the TextureData
    pbr_specular_glossiness.diffuse_texture = TextureInfoData(texture_idx2)
    pbr_specular_glossiness.diffuse_texture.add_extension(texture_transform)
    material.add_extension(pbr_specular_glossiness)

    # add box
    box = Box(Frame.worldXY(), 1, 1, 1)
    mesh = Mesh.from_shape(box)
    mesh.quads_to_triangles()

    node = scene.add_child()
    mesh_data = node.add_mesh(mesh)
    normals = [mesh.vertex_normal(k) for k in mesh.vertices()]

    texcoord_0 = [(0, 0) for _ in mesh.vertices()]

    """
    for fkey in mesh.faces():
        vkeys = mesh.face_vertices(fkey)
        plane = mesh.face_plane(fkey)
        frame = Frame.from_plane(plane)
        coords = mesh.face_coordinates(fkey)
        for vkey, xyz in zip(vkeys, coords):
            u, v, _ = frame.to_local_coordinates(Point(*xyz))
            texcoord_0[vkey] = (u, v)  # not ideal, gets overwritten
    """

    # here is the tricky part... for this material to be valid and applied to this mesh,
    # each of the primitives must have within the attribute `attributes` a key of the form `TEXCOORD_{some integer}`.
    # the value of this thing should be a list of pairs of floats representing the UV texture coordinates for each vertex.
    # if `{some integer}` is 0 then there's nothing else to do.  but if a primitive has multiple `TEXTCOORD_{some integer}`s,
    # then the various `TextureInfoData.tex_coord` associated to this material have to be updated with the appropriate `{some integer}`.

    # would work better if each vertex could have 4 different texture coordinates
    texcoord_0 = [
        (0.0, 1.0),
        (0.0, 0.0),
        (1.0, 0.0),
        (1.0, 1.0),
        (0.0, 0.0),
        (1.0, 0.0),
        (1.0, 1.0),
        (0.0, 1.0),
    ]

    pd = node.mesh_data.primitive_data_list[0]
    pd.material = material_key
    pd.attributes["TEXCOORD_0"] = texcoord_0
    pd.attributes["NORMAL"] = normals

    gltf = GLTF(gltf_filepath)
    gltf.content = cnt
    gltf.export(embed_data=False)
