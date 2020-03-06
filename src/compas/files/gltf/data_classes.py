from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import itertools

from compas.files.gltf.constants import MODE_BY_VERTEX_COUNT
from compas.files.gltf.constants import VERTEX_COUNT_BY_MODE
from compas.files.gltf.helpers import get_weighted_mesh_vertices


class SamplerData(object):
    def __init__(self, input_, output, interpolation=None, extras=None):
        self.input = input_
        self.output = output
        self.interpolation = interpolation
        self.extras = extras


class AnimationData(object):
    def __init__(self, channels, samplers, name=None, extras=None):
        self.channels = channels
        self.samplers = samplers
        self.name = name
        self.extras = extras


class SkinData(object):
    def __init__(self, joints, inverse_bind_matrices=None, skeleton=None, name=None, extras=None):
        self.joints = joints
        self.inverse_bind_matrices = inverse_bind_matrices
        self.skeleton = skeleton
        self.name = name
        self.extras = extras


class ImageData(object):
    def __init__(self, image_data=None, uri=None, mime_type=None, media_type=None, name=None, extras=None):
        self.uri = uri
        self.mime_type = mime_type
        self.media_type = media_type
        self.name = name
        self.extras = extras

        self.data = image_data


class PrimitiveData(object):
    def __init__(self, attributes, indices=None, material=None, mode=None, targets=None, extras=None):
        self.attributes = attributes or {}
        self.indices = indices
        self.material = material
        self.mode = mode
        self.targets = targets
        self.extras = extras


class MeshData(object):
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
    vertices : list
        List of xyz-tuples representing the points of the mesh.
    faces : list
        List of tuples referencing the indices of :attr:`compas.files.MeshData.vertices`
        representing faces of the mesh.
    """
    def __init__(self, primitive_data_list, mesh_key, mesh_name=None, weights=None, extras=None):
        self.mesh_name = mesh_name
        self.weights = weights
        self.primitive_data_list = primitive_data_list
        self.extras = extras

        self.key = mesh_key

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
    def from_vertices_and_faces(cls, vertices, faces, mesh_name=None, extras=None):
        """Construct a :class:`compas.files.MeshData` object from lists of vertices and faces.
        Vertices can be given as either a list of xyz-tuples or -lists, in which case
        the faces reference vertices by index, or vertices can be given as a dictionary of
        key-value pairs where the values are xyz-tuples or -lists and the faces reference the keys.
        """
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

        return cls(mesh_name, None, [primitive], extras)

    @classmethod
    def from_mesh(cls, mesh):
        """Construct a :class:`compas.files.MeshData` object from a :class:`compas.datastructures.Mesh`.
        """
        vertices, faces = mesh.to_vertices_and_faces()
        return cls.from_vertices_and_faces(vertices, faces)
