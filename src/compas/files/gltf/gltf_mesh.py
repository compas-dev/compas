import itertools
from collections.abc import Hashable
from collections.abc import Mapping
from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Any
from typing import Optional
from typing import Union
from typing import cast

from typing_extensions import Self

from compas.files.gltf.constants import VERTEX_COUNT_BY_MODE
from compas.files.gltf.data_classes import PrimitiveData
from compas.files.gltf.helpers import get_mode
from compas.files.gltf.helpers import get_unweighted_primitive_vertices
from compas.files.gltf.helpers import get_weighted_mesh_vertices

if TYPE_CHECKING:
    from compas.datastructures import Mesh

    from .gltf_document import GLTFDocument


class GLTFMesh:
    """Object containing mesh data in a format compatible with the glTF standard.

    Attributes
    ----------
    mesh_name : str
        String of the name of the mesh.
    weights : list
        List containing the weights to be applied to morph targets.
    primitive_data_list : list
        List of objects defining the geometry and material of the mesh.
    extras : object
    extensions : object
    context : GLTFDocument
        GLTF context in which the mesh exists.
    key : int
        Key of the mesh used in GLTFMesh.context.meshes.
    vertices : list
        List of xyz-tuples representing the points of the mesh.
    faces : list
        List of tuples referencing the indices of GLTFMesh.vertices
        representing faces of the mesh.

    """

    def __init__(
        self,
        primitive_data_list: list[PrimitiveData],
        context: "GLTFDocument",
        mesh_name: Optional[str] = None,
        weights: Optional[list[float]] = None,
        extras: Any = None,
        extensions: Any = None,
    ) -> None:
        self.mesh_name = mesh_name
        self.weights = weights
        self.primitive_data_list = primitive_data_list
        self.extras = extras
        self.extensions = extensions

        self._key = None
        self.context = context
        self._set_key()

    def _set_key(self) -> None:
        key = len(self.context.meshes)
        while key in self.context.meshes:
            key += 1
        self.context.meshes[key] = self
        self._key = key

    @property
    def key(self) -> int:
        assert self._key is not None
        return self._key

    @property
    def vertices(self) -> list[tuple[float, ...]]:
        if not self.weights:
            return get_unweighted_primitive_vertices(self.primitive_data_list)
        return get_weighted_mesh_vertices(self, self.weights)

    @property
    def faces(self) -> list[tuple[int, ...]]:
        faces = []
        shift = 0
        for primitive_data in self.primitive_data_list:
            indices = primitive_data.indices or range(len(primitive_data.attributes["POSITION"]))
            shifted_indices = self.shift_indices(indices, shift)
            group_size = VERTEX_COUNT_BY_MODE[primitive_data.mode]
            grouped_indices = self.group_indices(shifted_indices, group_size)
            faces.extend(grouped_indices)
            shift += len(primitive_data.attributes["POSITION"])
        return faces

    def shift_indices(self, indices: Sequence[int], shift: int) -> list[int]:
        """Shift every index by an offset.

        Parameters
        ----------
        indices
            Indices to shift.
        shift
            Offset added to every index.

        Returns
        -------
        list[int]
            Shifted indices.

        """
        return [index + shift for index in indices]

    def group_indices(self, indices: Sequence[int], group_size: int) -> list[tuple[int, ...]]:
        """Group a flat index sequence into fixed-size tuples.

        Parameters
        ----------
        indices
            Flat index sequence.
        group_size
            Number of indices per group.

        Returns
        -------
        list[tuple[int, ...]]
            Grouped indices.

        """
        it = [iter(indices)] * group_size
        return list(zip(*it))

    @classmethod
    def validate_faces(cls, faces: Sequence[Sequence[Hashable]]) -> None:
        """Validate that all index groups consistently represent points, lines, or triangles.

        Parameters
        ----------
        faces
            Point, line, or triangle index groups.

        Raises
        ------
        Exception
            If index groups have unsupported or inconsistent sizes.

        """
        if not faces:
            return
        if len(faces[0]) > 3:
            raise Exception("Invalid mesh. Expected mesh composed of points, lines xor triangles.")
        for face in faces:
            if len(face) != len(faces[0]):
                # This restriction could be removed by splitting into multiple primitives.
                raise NotImplementedError("Invalid mesh. Expected mesh composed of points, lines xor triangles.")

    @classmethod
    def validate_vertices(
        cls, vertices: Union[Sequence[Sequence[float]], Mapping[Hashable, Sequence[float]]]
    ) -> None:
        """Raise an exception if there are either too many vertices, or the vertices do not
        represent points in 3-space.

        Parameters
        ----------
        vertices
            Vertex coordinates by position or key.

        """
        if len(vertices) > 4294967295:
            # This restriction could be removed by splitting into multiple primitives.
            raise Exception("Invalid mesh.  Too many vertices.")
        if isinstance(vertices, Mapping):
            positions = list(vertices.values())
        else:
            positions = vertices
        for position in positions:
            if len(position) != 3:
                raise Exception("Invalid mesh.  Vertices are expected to be points in 3-space.")

    @classmethod
    def from_vertices_and_faces(
        cls,
        context: "GLTFDocument",
        vertices: Union[Sequence[Sequence[float]], Mapping[Hashable, Sequence[float]]],
        faces: Sequence[Sequence[Hashable]],
        mesh_name: Optional[str] = None,
        extras: Any = None,
    ) -> Self:
        """Construct a GLTFMesh object from lists of vertices and faces.
        Vertices can be given as either a list of xyz-tuples or -lists, in which case
        the faces reference vertices by index, or vertices can be given as a dictionary of
        key-value pairs where the values are xyz-tuples or -lists and the faces reference the keys.

        Parameters
        ----------
        context
            Destination document.
        vertices
            Vertex coordinates by position or key.
        faces
            Point, line, or triangle index groups.
        mesh_name
            Optional mesh name.
        extras
            Application-specific data.

        Returns
        -------
        GLTFMesh
            Created mesh data.

        """
        cls.validate_faces(faces)
        cls.validate_vertices(vertices)
        mode = get_mode(faces)
        if isinstance(vertices, Mapping):
            index_by_key = {}
            positions = []
            for key, position in vertices.items():
                positions.append(position)
                index_by_key[key] = len(positions) - 1
            face_list = [index_by_key[key] for key in itertools.chain(*faces)]
        else:
            positions = [list(position) for position in vertices]
            face_list = cast(list[int], list(itertools.chain(*faces)))

        primitive = PrimitiveData({"POSITION": cast(list[Any], positions)}, face_list, None, mode, None, None)

        return cls([primitive], context, mesh_name=mesh_name, extras=extras)

    @classmethod
    def from_mesh(cls, context: "GLTFDocument", mesh: "Mesh") -> Self:
        """Construct a GLTFMesh object from a compas mesh.

        Parameters
        ----------
        context
            Destination document.
        mesh
            Source mesh.

        Returns
        -------
        GLTFMesh
            Created mesh data.
        """
        vertices, faces = mesh.to_vertices_and_faces()
        texture_coordinates = mesh.vertices_attribute("texture_coordinate")
        vertex_normals = mesh.vertices_attribute("vertex_normal")
        vertex_colors = mesh.vertices_attribute("vertex_color")

        mesh_data = cls.from_vertices_and_faces(context, vertices, faces)
        pd = mesh_data.primitive_data_list[0]
        if texture_coordinates and texture_coordinates[0] is not None:
            pd.attributes["TEXCOORD_0"] = texture_coordinates
        if vertex_normals and vertex_normals[0] is not None:
            pd.attributes["NORMAL"] = vertex_normals
        if vertex_colors and vertex_colors[0] is not None:
            pd.attributes["COLOR_0"] = vertex_colors
        return mesh_data
