from copy import deepcopy
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from typing import Union
from typing import cast

from compas.files.gltf.data_classes import AnimationData
from compas.files.gltf.data_classes import CameraData
from compas.files.gltf.data_classes import ImageData
from compas.files.gltf.data_classes import MaterialData
from compas.files.gltf.data_classes import SamplerData
from compas.files.gltf.data_classes import SkinData
from compas.files.gltf.data_classes import TextureData
from compas.files.gltf.data_classes import TextureInfoData
from compas.files.gltf.gltf_mesh import GLTFMesh
from compas.files.gltf.gltf_node import GLTFNode
from compas.files.gltf.gltf_scene import GLTFScene
from compas.files.gltf.helpers import get_weighted_mesh_vertices
from compas.geometry import multiply_matrices
from compas.geometry import transform_points

if TYPE_CHECKING:
    from compas.datastructures import Mesh


class GLTFDocument:
    """Semantic content and scene-editing model of a glTF document.

    Attributes
    ----------
    scenes : dict
        Dictionary containing (int, GLTFScene) pairs.
    default_scene_key : int or None
        Key of the scene to be displayed on loading the glTF.
    nodes : dict
        Dictionary containing (int, GLTFNode) pairs.
    meshes : dict
        Dictionary containing (int, GLTFMesh) pairs.
    cameras : dict
        Dictionary containing (int, CameraData) pairs.
    animations : dict
        Dictionary containing (int, AnimationData) pairs.
    skins : dict
        Dictionary containing (int, SkinData) pairs.
    materials : dict
        Dictionary containing (int, MaterialData) pairs.
    textures : dict
        Dictionary containing (int, TextureData) pairs.
    samplers : dict
        Dictionary containing (int, SamplerData) pairs.
    images : dict
        Dictionary containing (int, ImageData) pairs.
    extras : object
    extensions : object

    """

    def __init__(self) -> None:
        self.scenes: dict[int, GLTFScene] = {}
        self.default_scene_key: Optional[int] = None
        self.nodes: dict[int, GLTFNode] = {}
        self.meshes: dict[int, GLTFMesh] = {}
        self.cameras: dict[int, CameraData] = {}
        self.animations: dict[int, AnimationData] = {}
        self.skins: dict[int, SkinData] = {}
        self.materials: dict[int, MaterialData] = {}
        self.textures: dict[int, TextureData] = {}
        self.samplers: dict[int, SamplerData] = {}
        self.images: dict[int, ImageData] = {}
        self.extras: Any = None
        self.extensions: Any = None
        self.extensions_used: Optional[list[str]] = None
        self.extensions_required: Optional[list[str]] = None
        self.asset: dict[str, Any] = {"version": "2.0"}
        self.unknown: dict[str, Any] = {}

    @property
    def default_or_first_scene(self) -> GLTFScene:
        key = self.default_scene_key or 0
        return self.scenes[key]

    def check_if_forest(self) -> None:
        """Verify that the nodes form a disjoint union of rooted trees.

        Raises
        ------
        ValueError
            If a node has multiple parents or the hierarchy contains a cycle.

        """
        parent_counts = {key: 0 for key in self.nodes}
        for node in self.nodes.values():
            for child_key in node.children:
                parent_counts[child_key] += 1
        if any(count > 1 for count in parent_counts.values()):
            raise ValueError("A glTF node cannot have multiple parents.")

        states = {key: 0 for key in self.nodes}

        def visit(key):
            if states[key] == 1:
                raise ValueError("glTF node hierarchy contains a cycle.")
            if states[key] == 2:
                return
            states[key] = 1
            for child_key in self.nodes[key].children:
                visit(child_key)
            states[key] = 2

        for node_key in self.nodes:
            visit(node_key)

    def validate(self) -> None:
        """Validate references and scene-graph structure.

        """
        if self.asset.get("version") != "2.0":
            raise ValueError("glTF asset version 2.0 is required.")
        used = set(self.extensions_used or [])
        required = set(self.extensions_required or [])
        if not required.issubset(used):
            raise ValueError("Required glTF extensions must also appear in extensionsUsed.")
        if self.default_scene_key is not None and self.default_scene_key not in self.scenes:
            raise ValueError(f"Cannot find default glTF scene {self.default_scene_key}.")
        for scene in self.scenes.values():
            for key in scene.children:
                if key not in self.nodes:
                    raise ValueError(f"Cannot find glTF scene node {key}.")
        for node in self.nodes.values():
            for key in node.children:
                if key not in self.nodes:
                    raise ValueError(f"Cannot find child glTF node {key}.")
            if node.mesh_key is not None and node.mesh_key not in self.meshes:
                raise ValueError(f"Cannot find glTF mesh {node.mesh_key}.")
            if node.camera is not None and node.camera not in self.cameras:
                raise ValueError(f"Cannot find glTF camera {node.camera}.")
            if node.skin is not None and node.skin not in self.skins:
                raise ValueError(f"Cannot find glTF skin {node.skin}.")
        for mesh in self.meshes.values():
            for primitive in mesh.primitive_data_list:
                if "POSITION" not in primitive.attributes:
                    raise ValueError("glTF mesh primitives require a POSITION attribute.")
                if primitive.mode not in (None, 0, 1, 2, 3, 4, 5, 6):
                    raise ValueError(f"Unsupported glTF primitive mode {primitive.mode}.")
                vertex_count = len(primitive.attributes["POSITION"])
                if vertex_count == 0:
                    raise ValueError("glTF POSITION attributes cannot be empty.")
                if primitive.indices is not None and any(index < 0 or index >= vertex_count for index in primitive.indices):
                    raise ValueError("glTF primitive index is outside its POSITION accessor.")
                if primitive.material is not None and primitive.material not in self.materials:
                    raise ValueError(f"Cannot find glTF material {primitive.material}.")
        for sampler in self.samplers.values():
            if sampler.mag_filter is not None and sampler.mag_filter not in (9728, 9729):
                raise ValueError(f"Invalid glTF magnification filter {sampler.mag_filter}.")
            if sampler.min_filter is not None and sampler.min_filter not in (9728, 9729, 9984, 9985, 9986, 9987):
                raise ValueError(f"Invalid glTF minification filter {sampler.min_filter}.")
            if sampler.wrap_s is not None and sampler.wrap_s not in (33071, 33648, 10497):
                raise ValueError(f"Invalid glTF wrap mode {sampler.wrap_s}.")
            if sampler.wrap_t is not None and sampler.wrap_t not in (33071, 33648, 10497):
                raise ValueError(f"Invalid glTF wrap mode {sampler.wrap_t}.")
        for texture in self.textures.values():
            if texture.sampler is not None and texture.sampler not in self.samplers:
                raise ValueError(f"Cannot find glTF sampler {texture.sampler}.")
            if texture.source is not None and texture.source not in self.images:
                raise ValueError(f"Cannot find glTF image {texture.source}.")
        for material in self.materials.values():
            if material.alpha_mode is not None and material.alpha_mode not in ("OPAQUE", "MASK", "BLEND"):
                raise ValueError(f"Invalid glTF alpha mode {material.alpha_mode!r}.")
            for item in material.iter_data():
                if isinstance(item, TextureInfoData) and item.index not in self.textures:
                    raise ValueError(f"Cannot find glTF texture {item.index}.")
        for animation in self.animations.values():
            for channel in animation.channels:
                if channel.sampler not in animation.samplers_dict:
                    raise ValueError(f"Cannot find glTF animation sampler {channel.sampler}.")
                if channel.target.node is not None and channel.target.node not in self.nodes:
                    raise ValueError(f"Cannot find glTF animation target node {channel.target.node}.")
                if channel.target.path not in ("translation", "rotation", "scale", "weights", "pointer"):
                    raise ValueError(f"Invalid glTF animation target path {channel.target.path!r}.")
            for sampler in animation.samplers_dict.values():
                if sampler.interpolation not in (None, "LINEAR", "STEP", "CUBICSPLINE"):
                    raise ValueError(f"Invalid glTF animation interpolation {sampler.interpolation!r}.")
        for skin in self.skins.values():
            if not skin.joints:
                raise ValueError("glTF skins require at least one joint.")
            for joint in skin.joints:
                if joint not in self.nodes:
                    raise ValueError(f"Cannot find glTF skin joint {joint}.")
            if skin.skeleton is not None and skin.skeleton not in self.nodes:
                raise ValueError(f"Cannot find glTF skin skeleton {skin.skeleton}.")
            if skin.inverse_bind_matrices is not None and len(skin.inverse_bind_matrices) != len(skin.joints):
                raise ValueError("glTF inverse bind matrix count must match the number of joints.")
        for camera in self.cameras.values():
            if camera.type not in ("perspective", "orthographic"):
                raise ValueError(f"Invalid glTF camera type {camera.type!r}.")
            if camera.type == "perspective" and camera.perspective is None:
                raise ValueError("Perspective glTF cameras require perspective properties.")
            if camera.type == "orthographic" and camera.orthographic is None:
                raise ValueError("Orthographic glTF cameras require orthographic properties.")
        self.check_if_forest()

    def without_orphans(self) -> "GLTFDocument":
        """Return an independent document with unreachable data removed.

        Returns
        -------
        GLTFDocument
            Cleaned document copy.

        """
        content = deepcopy(self)
        content.remove_orphans()
        return content

    def remove_orphans(self) -> None:
        """Remove unreachable objects.

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
        for animation_key, animation in list(self.animations.items()):
            animation.channels = [
                channel
                for channel in animation.channels
                if channel.target.node is None or node_visit_log[channel.target.node]
            ]
            visited_sampler_keys = {channel.sampler for channel in animation.channels}
            animation.samplers_dict = {key: animation.samplers_dict[key] for key in animation.samplers_dict if key in visited_sampler_keys}
            if not animation.samplers_dict:
                del self.animations[animation_key]

        # remove skins referencing no existing nodes
        for key, skin_data in list(self.skins.items()):
            skin_data.joints = [joint_key for joint_key in skin_data.joints if node_visit_log[joint_key]]
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
            for item in material.iter_data():
                if isinstance(item, TextureInfoData):
                    texture_visit_log[item.index] = True

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

    def _remove_unvisited(self, log: dict[int, bool], dictionary: dict[int, Any]) -> None:
        for key, visited in log.items():
            if not visited:
                del dictionary[key]

    def update_node_transforms_and_positions(self) -> None:
        """Update transforms and positions throughout all scenes.

        """
        for scene in self.scenes.values():
            self.update_scene_transforms_and_positions(scene)

    def update_scene_transforms_and_positions(self, scene: GLTFScene) -> None:
        """Update transforms and positions throughout a scene tree.

        Parameters
        ----------
        scene
            Scene to update.

        """
        origin = [0, 0, 0]
        for node_key in scene.children:
            node = self.nodes[node_key]
            node.transform = node.matrix or node.get_matrix_from_trs()
            node.position = cast(list[float], transform_points([origin], node.transform)[0])
            queue = [node_key]
            while queue:
                cur_key = queue.pop(0)
                cur = self.nodes[cur_key]
                for child_key in cur.children:
                    child = self.nodes[child_key]
                    child.transform = cast(
                        list[list[float]],
                        multiply_matrices(cur.transform, child.matrix or child.get_matrix_from_trs()),
                    )
                    child.position = cast(list[float], transform_points([origin], child.transform)[0])
                    queue.append(child_key)

    def get_node_faces(self, node: GLTFNode) -> Optional[list[tuple[int, ...]]]:
        """Return the faces of the mesh attached to a node.

        Parameters
        ----------
        node
            Node containing the mesh.

        Returns
        -------
        list[tuple[int, ...]] | None
            Mesh faces, if the node references a mesh.
        """
        if node.mesh_key is None:
            return None
        mesh_data = self.meshes.get(node.mesh_key)
        if mesh_data is None:
            return None
        return mesh_data.faces

    def get_node_vertices(self, node: GLTFNode) -> Optional[list[tuple[float, ...]]]:
        """Return the vertices of the mesh attached to a node.

        Parameters
        ----------
        node
            Node containing the mesh.

        Returns
        -------
        list[tuple[float, ...]] | None
            Mesh vertices, with node morph weights applied when present.
        """
        if node.mesh_key is None:
            return None
        mesh_data = self.meshes.get(node.mesh_key)
        if mesh_data is None:
            return None
        if node.weights is None:
            return mesh_data.vertices
        return get_weighted_mesh_vertices(mesh_data, node.weights)

    def get_node_by_name(self, name: str) -> Optional[GLTFNode]:
        """Return the node with a specific name.

        Parameters
        ----------
        name
            Name to match.

        Returns
        -------
        GLTFNode | None
            Matching node, if found.
        """
        for key in self.nodes:
            if self.nodes[key].name == name:
                return self.nodes[key]
        return None

    @classmethod
    def _get_next_available_key(cls, adict: dict[int, Any]) -> int:
        key = len(adict)
        while key in adict:
            key += 1
        return key

    def add_material(self, material: MaterialData) -> int:
        """Add a material to the document.

        Parameters
        ----------
        material
            Material to add.

        Returns
        -------
        int
            Assigned material key.
        """
        key = self._get_next_available_key(self.materials)
        self.materials[key] = material
        return key

    def add_texture(self, texture: TextureData) -> int:
        """Add a texture to the document.

        Parameters
        ----------
        texture
            Texture to add.

        Returns
        -------
        int
            Assigned texture key.
        """
        key = self._get_next_available_key(self.textures)
        self.textures[key] = texture
        return key

    def add_image(self, image: ImageData) -> int:
        """Add an image to the document.

        Parameters
        ----------
        image
            Image to add.

        Returns
        -------
        int
            Assigned image key.
        """
        key = self._get_next_available_key(self.images)
        self.images[key] = image
        return key

    def get_material_index_by_name(self, name: str) -> Optional[int]:
        """Return the key of a material with a specific name.

        Parameters
        ----------
        name
            Name to match.

        Returns
        -------
        int | None
            Matching material key, if found.
        """
        for key, material in self.materials.items():
            if material.name == name:
                return key
        return None

    def add_scene(self, name: Optional[str] = None, extras: Any = None) -> GLTFScene:
        """Add a scene to the document.

        Parameters
        ----------
        name
            Optional scene name.
        extras
            Application-specific scene data.

        Returns
        -------
        GLTFScene
        """
        return GLTFScene(self, name=name, extras=extras)

    def add_node_to_scene(
        self, scene: GLTFScene, node_name: Optional[str] = None, node_extras: Any = None
    ) -> GLTFNode:
        """Create a node and add it as a scene root.

        Parameters
        ----------
        scene
            Parent scene.
        node_name
            Optional node name.
        node_extras
            Application-specific node data.

        Returns
        -------
        GLTFNode
        """
        if scene not in self.scenes.values():
            raise ValueError("Cannot find glTF scene.")
        node = GLTFNode(self, node_name, node_extras)
        scene.children.append(node.key)
        return node

    def add_child_to_node(
        self, parent_node: GLTFNode, child_name: Optional[str] = None, child_extras: Any = None
    ) -> GLTFNode:
        """Create a node and add it as a child of another node.

        Parameters
        ----------
        parent_node
            Parent node.
        child_name
            Optional child name.
        child_extras
            Application-specific child data.

        Returns
        -------
        GLTFNode
        """
        child_node = GLTFNode(self, child_name, child_extras)
        parent_node.children.append(child_node.key)
        return child_node

    def add_mesh(self, mesh: "Mesh") -> GLTFMesh:
        """Convert a COMPAS mesh and add it to the document.

        Parameters
        ----------
        mesh
            Mesh to add.

        Returns
        -------
        GLTFMesh
        """
        return GLTFMesh.from_mesh(self, mesh)

    def add_mesh_to_node(self, node: GLTFNode, mesh: "Union[int, Mesh]") -> GLTFMesh:
        """Attach an existing or converted mesh to a node.

        Parameters
        ----------
        node
            Destination node.
        mesh
            Existing mesh key or mesh to add.

        Returns
        -------
        GLTFMesh
        """
        if isinstance(mesh, int):
            mesh_data = self.meshes[mesh]
        else:
            mesh_data = self.add_mesh(mesh)
        node.mesh_key = mesh_data.key
        return mesh_data

    def get_nodes_from_scene(self, scene: GLTFScene) -> dict[int, GLTFNode]:
        """Return the nodes reachable from a scene.

        Parameters
        ----------
        scene
            Scene to traverse.

        Returns
        -------
        dict[int, GLTFNode]
            Nodes keyed by document key.
        """
        node_dict = {}

        def visit(key):
            node_dict[key] = self.nodes[key]
            for child in self.nodes[key].children:
                visit(child)

        for child_key in scene.children:
            visit(child_key)

        return node_dict

    def get_scene_positions_and_edges(self, scene: GLTFScene):
        """Return node positions and hierarchy edges for a scene.

        Parameters
        ----------
        scene
            Scene to inspect.

        Returns
        -------
        tuple[dict[Any, Any], list[tuple[Any, int]]]
            Node positions and hierarchy edges.
        """
        positions_dict: dict[Any, Any] = {"root": [0, 0, 0]}
        edges_list: list[tuple[Any, int]] = []

        def visit(node, key):
            for child_key in node.children:
                positions_dict[child_key] = self.nodes[child_key].position
                edges_list.append((key, child_key))
                visit(self.nodes[child_key], child_key)

        visit(scene, "root")

        return positions_dict, edges_list
