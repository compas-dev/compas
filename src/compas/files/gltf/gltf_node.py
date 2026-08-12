from math import fabs
from typing import TYPE_CHECKING
from typing import Any
from typing import Iterable
from typing import Optional
from typing import Union
from typing import cast

from compas.files.gltf.gltf_children import GLTFChildren
from compas.geometry import identity_matrix
from compas.geometry import matrix_from_quaternion
from compas.geometry import matrix_from_scale_factors
from compas.geometry import matrix_from_translation
from compas.geometry import multiply_matrices

if TYPE_CHECKING:
    from compas.datastructures import Mesh

    from .gltf_document import GLTFDocument
    from .gltf_mesh import GLTFMesh


class GLTFNode:
    """Object representing the COMPAS consumable part of a glTF node.

    Attributes
    ----------
    name : str
        Name of the node.
    children : GLTFChildren
        Validated list of keys referencing GLTFNode.context.nodes.
    matrix : list of lists
        Matrix representing the displacement from node's parent to the node.
        Default value is the identity matrix.
        Cannot be set when any of translation, rotation or scale is set.
    translation : list[float]
        xyz-coordinates of the translation displacement of the node.
        Cannot be set when GLTFNode.matrix is set.
    rotation : list[float]
        Unit quaternion representing the rotational displacement of the node.
        Cannot be set when GLTFNode.matrix is set.
    scale : list[float]
        List of length 3 representing the scaling displacement of the node.
        Cannot be set when GLTFNode.matrix is set.
    mesh_key : int
        Key of the mesh within GLTFNode.context.meshes.
    weights : list[float]
        Weights used for computing morph targets in the attached mesh.
    position : tuple
        xyz-coordinates of the node, calculated from the matrix and tree structure.
    transform : list of lists
        Matrix representing the displacement from the root node to the node.
    key : int
        Key of the node used in GLTFNode.context.nodes.
    camera : int
        Key of the camera in GLTFNode.context.cameras.
    skin : int
        Key of the skin in GLTFNode.context.skins.
    extras : object
        Application-specific data.
    extensions : object
    context : GLTFDocument
        GLTF context in which the node exists.
    mesh_data : GLTFMesh
        GLTFMesh used by this node.
    vertices : list
        List of xyz-coordinates of the points of the mesh used by this node.
    faces : list
        List of tuples of indices of the vertices of the faces of the mesh used by this node.

    """

    def __init__(
        self,
        context: "GLTFDocument",
        name: Optional[str] = None,
        extras: Any = None,
        extensions: Any = None,
    ) -> None:
        self.name = name
        self._children = GLTFChildren(context, [])
        self._matrix = None
        self._translation = None
        self._rotation = None
        self._scale = None
        self._mesh_key = None
        self.weights: Optional[list[float]] = None

        self.position: Optional[list[float]] = None
        self.transform: Optional[list[list[float]]] = None
        self._key = None

        self._camera = None
        self._skin = None
        self.extras = extras
        self.extensions = extensions

        self.context = context
        self._set_key()

    def _set_key(self) -> None:
        key = len(self.context.nodes)
        while key in self.context.nodes:
            key += 1
        self.context.nodes[key] = self
        self._key = key

    @property
    def key(self) -> int:
        assert self._key is not None
        return self._key

    @property
    def children(self) -> GLTFChildren:
        return self._children

    @children.setter
    def children(self, value: Optional[Iterable[int]]) -> None:
        self._children = GLTFChildren(self.context, value or [])

    @property
    def mesh_key(self) -> Optional[int]:
        return self._mesh_key

    @mesh_key.setter
    def mesh_key(self, value: Optional[int]) -> None:
        if value is not None and value not in self.context.meshes:
            raise ValueError(f"Cannot find glTF mesh {value}.")
        self._mesh_key = value

    @property
    def camera(self) -> Optional[int]:
        return self._camera

    @camera.setter
    def camera(self, value: Optional[int]) -> None:
        if value is not None and value not in self.context.cameras:
            raise ValueError(f"Cannot find glTF camera {value}.")
        self._camera = value

    @property
    def skin(self) -> Optional[int]:
        return self._skin

    @skin.setter
    def skin(self, value: Optional[int]) -> None:
        if value is not None and value not in self.context.skins:
            raise ValueError(f"Cannot find glTF skin {value}.")
        self._skin = value

    @property
    def translation(self) -> Optional[list[float]]:
        return self._translation

    @translation.setter
    def translation(self, value: Optional[list[float]]) -> None:
        if value is None:
            self._translation = value
            return
        if self._matrix:
            raise ValueError("Cannot set translation when matrix is set.")
        if not isinstance(value, list) or len(value) != 3:
            raise ValueError("Invalid translation. Expected [x, y, z].")
        self._translation = value

    @property
    def rotation(self) -> Optional[list[float]]:
        return self._rotation

    @rotation.setter
    def rotation(self, value: Optional[list[float]]) -> None:
        if value is None:
            self._rotation = value
            return
        if self._matrix:
            raise ValueError("Cannot set rotation when matrix is set.")
        if not isinstance(value, list) or len(value) != 4 or fabs(sum([q**2 for q in value]) - 1) > 1e-03:
            raise ValueError("Invalid rotation. Expected a unit quaternion [x, y, z, w].")
        self._rotation = value

    @property
    def scale(self) -> Optional[list[float]]:
        return self._scale

    @scale.setter
    def scale(self, value: Optional[list[float]]) -> None:
        if value is None:
            self._scale = value
            return
        if self._matrix:
            raise ValueError("Cannot set scale when matrix is set.")
        if not isinstance(value, list) or len(value) != 3:
            raise ValueError("Invalid scale. Expected [x, y, z].")
        self._scale = value

    @property
    def matrix(self) -> Optional[list[list[float]]]:
        if not (self.translation or self.rotation or self.scale or self._matrix):
            return identity_matrix(4)
        return self._matrix

    @matrix.setter
    def matrix(self, value: Optional[list[list[float]]]) -> None:
        if value is None:
            self._matrix = value
            return
        if self.translation or self.rotation or self.scale:
            raise ValueError("Cannot set matrix when translation, rotation, or scale is set.")
        if not isinstance(value, list) or not value or not value[0] or not isinstance(value[0], list):
            raise ValueError("Invalid matrix. Expected a list of lists.")
        if len(value) != 4 or len(value[0]) != 4:
            raise ValueError("Invalid matrix. Expected a 4x4 matrix.")
        if value[3] != [0, 0, 0, 1]:
            raise ValueError(
                "Invalid matrix.  A matrix without shear or skew is expected.  It must be of the form TRS, where T is a translation, R is a rotation and S is a scaling."
            )
        self._matrix = value

    @property
    def mesh_data(self) -> "Optional[GLTFMesh]":
        if self.mesh_key is None:
            return None
        return self.context.meshes.get(self.mesh_key)

    @property
    def vertices(self):
        return self.context.get_node_vertices(self)

    @property
    def faces(self):
        return self.context.get_node_faces(self)

    def get_matrix_from_trs(self) -> list[list[float]]:
        """Compose the node's translation, rotation, and scale into a matrix.

        Returns
        -------
        list[list[float]]
            Composed transformation matrix.

        """
        matrix = cast(list[list[float]], identity_matrix(4))
        if self.translation:
            translation = matrix_from_translation(self.translation)
            matrix = multiply_matrices(matrix, translation)
        if self.rotation:
            rotation = matrix_from_quaternion(self.rotation)
            matrix = multiply_matrices(matrix, rotation)
        if self.scale:
            scale = matrix_from_scale_factors(self.scale)
            matrix = multiply_matrices(matrix, scale)
        return cast(list[list[float]], matrix)

    def add_child(self, child_name: Optional[str] = None, child_extras: Any = None) -> "GLTFNode":
        """Create and attach a child node.

        Parameters
        ----------
        child_name
            Optional child name.
        child_extras
            Application-specific child data.

        Returns
        -------
        GLTFNode
            Created child node.
        """
        return self.context.add_child_to_node(self, child_name, child_extras)

    def add_mesh(self, mesh: "Union[int, Mesh]") -> "GLTFMesh":
        """Attach an existing or converted mesh to this node.

        Parameters
        ----------
        mesh
            Existing mesh key or mesh to convert.

        Returns
        GLTFMesh
            Attached mesh data.

        """
        return self.context.add_mesh_to_node(self, mesh)
