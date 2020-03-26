from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import itertools

from compas.files.gltf.constants import MODE_BY_VERTEX_COUNT
from compas.files.gltf.constants import VERTEX_COUNT_BY_MODE
from compas.files.gltf.data_classes import PrimitiveData
from compas.files.gltf.helpers import get_weighted_mesh_vertices


class GLTFMesh(object):
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
    context : GLTFContent
        GLTF context in which the mesh exists.
    key : int
        Key of the mesh used in :attr:`compas.files.GLTFMesh.context.meshes`.
    vertices : list
        List of xyz-tuples representing the points of the mesh.
    faces : list
        List of tuples referencing the indices of :attr:`compas.files.MeshData.vertices`
        representing faces of the mesh.

    Methods
    -------
    shift_indices(list indices, int shift)
        Given a list of indices, returns a list of indices, all shifted by `shift`.
    group_indices(list indices, int group_size)
        Returns a list of the elements of `indices` grouped into tuples of size `group_size`.
    get_mode(list faces)
        Returns the glTF mode of a list of faces.
    validate_faces(list faces)
        Raises an exception if not all faces in `faces` are defining either all triangles, lines
        or points.
    validate_vertices(list vertices)
        Raise an exception if there are either too many vertices, or the vertices do not
        represent points in 3-space.
    from_vertices_and_faces(GLTFContent context, list vertices, list faces, str mesh_name, object extras)
        Construct a :class:`compas.files.GLTFMesh` object from lists of vertices and faces.
        Vertices can be given as either a list of xyz-tuples or -lists, in which case
        the faces reference vertices by index, or vertices can be given as a dictionary of
        key-value pairs where the values are xyz-tuples or -lists and the faces reference the keys.
    from_mesh(Mesh mesh)
        Construct a :class:`compas.files.MeshData` object from a :class:`compas.datastructures.Mesh`.
    to_dict(list primitives)
        Returns a JSONable dictionary object in accordance with glTF specifications.
    from_dict(dict mesh, GLTFContent context, list primitive_data_list)
        Creates a :class:`compas.files.GLTFMesh` from a glTF node dictionary
        and inserts it in the provided context.
    """
    def __init__(self, primitive_data_list, context, mesh_name=None, weights=None, extras=None, extensions=None):
        self.mesh_name = mesh_name
        self.weights = weights
        self.primitive_data_list = primitive_data_list
        self.extras = extras
        self.extensions = extensions

        self._key = None
        self.context = context
        self._set_key()

    def _set_key(self):
        key = len(self.context.meshes)
        while key in self.context.meshes:
            key += 1
        self.context.meshes[key] = self
        self._key = key

    @property
    def key(self):
        return self._key

    @property
    def vertices(self):
        if not self.weights:
            return list(itertools.chain(*[primitive.attributes['POSITION'] for primitive in self.primitive_data_list]))
        return get_weighted_mesh_vertices(self, self.weights)

    @property
    def faces(self):
        faces = []
        shift = 0
        for primitive_data in self.primitive_data_list:
            shifted_indices = self.shift_indices(primitive_data.indices, shift)
            group_size = VERTEX_COUNT_BY_MODE[primitive_data.mode]
            grouped_indices = self.group_indices(shifted_indices, group_size)
            faces.extend(grouped_indices)
            shift += len(primitive_data.attributes['POSITION'])
        return faces

    def shift_indices(self, indices, shift):
        return [index + shift for index in indices]

    def group_indices(self, indices, group_size):
        it = [iter(indices)] * group_size
        return list(zip(*it))

    @classmethod
    def get_mode(cls, faces):
        vertex_count = len(faces[0])
        if vertex_count in MODE_BY_VERTEX_COUNT:
            return MODE_BY_VERTEX_COUNT[vertex_count]
        raise Exception('Meshes must be composed of triangles, lines or points.')

    @classmethod
    def validate_faces(cls, faces):
        if not faces:
            return
        if len(faces[0]) > 3:
            raise Exception('Invalid mesh. Expected mesh composed of points, lines xor triangles.')
        for face in faces:
            if len(face) != len(faces[0]):
                # This restriction could be removed by splitting into multiple primitives.
                raise NotImplementedError('Invalid mesh. Expected mesh composed of points, lines xor triangles.')

    @classmethod
    def validate_vertices(cls, vertices):
        if len(vertices) > 4294967295:
            # This restriction could be removed by splitting into multiple primitives.
            raise Exception('Invalid mesh.  Too many vertices.')
        positions = list(vertices.values()) if isinstance(vertices, dict) else vertices
        for position in positions:
            if len(position) != 3:
                raise Exception('Invalid mesh.  Vertices are expected to be points in 3-space.')

    @classmethod
    def from_vertices_and_faces(cls, context, vertices, faces, mesh_name=None, extras=None):
        cls.validate_faces(faces)
        cls.validate_vertices(vertices)
        mode = cls.get_mode(faces)
        if isinstance(vertices, dict):
            index_by_key = {}
            positions = []
            for key, position in vertices.items():
                positions.append(position)
                index_by_key[key] = len(positions) - 1
            face_list = [index_by_key[key] for key in itertools.chain(*faces)]
        else:
            positions = vertices
            face_list = list(itertools.chain(*faces))

        primitive = PrimitiveData({'POSITION': positions}, face_list, None, mode, None, None)

        return cls([primitive], context, mesh_name=mesh_name, extras=extras)

    @classmethod
    def from_mesh(cls, context, mesh):
        vertices, faces = mesh.to_vertices_and_faces()
        return cls.from_vertices_and_faces(context, vertices, faces)

    def to_dict(self, primitives):
        mesh_dict = {'primitives': primitives}
        if self.mesh_name is not None:
            mesh_dict['name'] = self.mesh_name
        if self.weights is not None:
            mesh_dict['weights'] = self.weights
        if self.extras is not None:
            mesh_dict['extras'] = self.extras
        if self.extensions is not None:
            mesh_dict['extensions'] = self.extensions
        return mesh_dict

    @classmethod
    def from_dict(cls, mesh, context, primitive_data_list):
        if mesh is None:
            return None
        return cls(
            primitive_data_list=primitive_data_list,
            context=context,
            mesh_name=mesh.get('name'),
            weights=mesh.get('weights'),
            extras=mesh.get('extras'),
            extensions=mesh.get('extensions'),
        )
