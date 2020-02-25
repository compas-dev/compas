from __future__ import print_function
from __future__ import absolute_import


__all__ = [
    'GLTF',
    'GLTFReader',
    'GLTFParser',
]

import base64
import itertools
import json
import math
import os
import re
import struct

from compas.geometry import identity_matrix
from compas.geometry import matrix_determinant
from compas.geometry import matrix_from_quaternion
from compas.geometry import matrix_from_scale_factors
from compas.geometry import matrix_from_translation
from compas.geometry import multiply_matrices
from compas.geometry import transpose_matrix

COMPONENT_TYPE_BYTE = 5120
COMPONENT_TYPE_UNSIGNED_BYTE = 5121
COMPONENT_TYPE_SHORT = 5122
COMPONENT_TYPE_UNSIGNED_SHORT = 5123
COMPONENT_TYPE_UNSIGNED_INT = 5125
COMPONENT_TYPE_FLOAT = 5126

TYPE_SCALAR = 'SCALAR'
TYPE_VEC2 = 'VEC2'
TYPE_VEC3 = 'VEC3'
TYPE_VEC4 = 'VEC4'
TYPE_MAT2 = 'MAT2'
TYPE_MAT3 = 'MAT3'
TYPE_MAT4 = 'MAT4'

COMPONENT_TYPE_ENUM = {
    COMPONENT_TYPE_BYTE: 'b',
    COMPONENT_TYPE_UNSIGNED_BYTE: 'B',
    COMPONENT_TYPE_SHORT: 'h',
    COMPONENT_TYPE_UNSIGNED_SHORT: 'H',
    COMPONENT_TYPE_UNSIGNED_INT: 'I',
    COMPONENT_TYPE_FLOAT: 'f',
}

NUM_COMPONENTS_BY_TYPE_ENUM = {
    TYPE_SCALAR: 1,
    TYPE_VEC2: 2,
    TYPE_VEC3: 3,
    TYPE_VEC4: 4,
    TYPE_MAT2: 4,
    TYPE_MAT3: 9,
    TYPE_MAT4: 16,
}

NUM_BYTES_BY_COMPONENT_TYPE = {
    COMPONENT_TYPE_BYTE: 1,
    COMPONENT_TYPE_UNSIGNED_BYTE: 1,
    COMPONENT_TYPE_SHORT: 2,
    COMPONENT_TYPE_UNSIGNED_SHORT: 2,
    COMPONENT_TYPE_UNSIGNED_INT: 4,
    COMPONENT_TYPE_FLOAT: 4,
}

MODE_BY_VERTEX_COUNT = {
    3: None,
    2: 1,
    1: 0,
}

VERTEX_COUNT_BY_MODE = {
    0: 1,
    1: 2,
    4: 3,
    None: 3,
}

DEFAULT_ROOT_NAME = 'root'


def get_matrix_from_col_major_list(matrix_as_list):
    return [[matrix_as_list[i + j * 4] for j in range(4)] for i in range(4)]


def inhomogeneous_transformation(matrix, vector):
    return project_vector(multiply_matrices([embed_vector(vector)], transpose_matrix(matrix))[0])


def embed_vector(vector):
    return vector + [1.0]


def project_vector(vector):
    return vector[:3]


class SamplerData(object):
    def __init__(self, input_, output, interpolation='LINEAR', extras=None):
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
    def __init__(self, image_data=None, uri=None, mime_type=None, media_type = None, name=None, extras=None):
        self.uri = uri
        self.mime_type = mime_type
        self.media_type = media_type
        self.name = name
        self.extras = extras

        self.data = image_data


class PrimitiveData(object):
    def __init__(self, attributes, indices, material, mode, targets, extras):
        self.attributes = attributes or {}
        self.indices = indices
        self.material = material
        self.mode = mode
        self.targets = targets
        self.extras = extras


class MeshData(object):  # expose this
    def __init__(self, mesh_name, weights, primitive_data_list, extras):
        self.mesh_name = mesh_name
        self.weights = weights
        self.primitive_data_list = primitive_data_list
        self.extras = extras

    @property
    def vertices(self):
        if not self.weights:
            return list(itertools.chain(*[primitive.attributes['POSITION'] for primitive in self.primitive_data_list]))

        vertices = []
        for primitive_data in self.primitive_data_list:
            position_target_data = [target['POSITION'] for target in primitive_data.targets]
            apply_morph_targets = self.get_morph_function(self.weights)
            vertices += list(map(apply_morph_targets, primitive_data.attributes['POSITION'], *position_target_data))
        return vertices

    def get_morph_function(self, weights):
        # Returns a function which computes for a fixed list w of scalar weights the linear combination
        #                               vertex + sum_i(w[i] * targets[i])
        # where vertex and targets[i] are vectors.

        def apply_weight(weight, target_coordinate):
            return weight * target_coordinate

        def weighted_sum(vertex_coordinate, *targets_coordinate):
            return vertex_coordinate + math.fsum(map(apply_weight, weights, targets_coordinate))

        def apply_morph_target(vertex, *targets):
            return tuple(map(weighted_sum, vertex, *targets)) + ((vertex[-1],) if len(vertex) == 4 else ())

        return apply_morph_target

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
            raise Exception('Invalid mesh.  Too many vertices.')
        positions = list(vertices.values()) if isinstance(vertices, dict) else vertices
        for position in positions:
            if len(position) != 3:
                raise Exception('Invalid mesh.  Vertices are expected to be points in 3-space.')

    @classmethod
    def from_vertices_and_faces(cls, vertices, faces, mesh_name=None, extras=None):
        cls.validate_faces(faces)
        cls.validate_vertices(vertices)
        mode = cls.get_mode(faces)
        if isinstance(vertices, dict):
            index_by_key = {}
            positions = []
            for key, position in vertices.items():
                positions.append(position)
                index_by_key[key] = len(positions) - 1
            face_list = [index_by_key[key] for key in itertools.chain(faces)]
        else:
            positions = vertices
            face_list = list(itertools.chain(faces))

        primitive = PrimitiveData({'POSITION': positions}, face_list, None, mode, None, None)

        return cls(mesh_name, None, [primitive], extras)

    @classmethod
    def from_mesh(cls, mesh):
        vertices, faces = mesh.to_vertices_and_faces()
        return cls.from_vertices_and_faces(vertices, faces)


class GLTFScene(object):
    """Object representing the base of a scene.

    Attributes
    ----------
    name : str
        Name of the scene, if any.
    nodes : dict
        Dictionary of (node_key, :class:`GLTFNode`) pairs.
        Node representing the root must be named ``DEFAULT_ROOT_NAME``.
    extras : object
        Application-specific data.
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
        root_node.position = [0, 0, 0]
        root_node.transform = identity_matrix(4)
        root_node.matrix = identity_matrix(4)
        root_node.children = []
        return root_node

    def update_node_transforms_and_positions(self):
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
                child.position = inhomogeneous_transformation(child.transform, self.nodes[DEFAULT_ROOT_NAME].position)
                queue.append(child_key)

    def is_tree(self):
        visited = {node_key: False for node_key in nodes}
        queue = [DEFAULT_ROOT_NAME]
        while queue:
            cur = queue.pop(0)
            if visited[cur]:
                raise Exception('Scene {} is not a tree.'.format(self.name))
            visited[cur] = True
            queue.extend(nodes[cur].children)
        return True


class GLTFNode(object):
    """Object representing the COMPAS consumable part of a glTF node.

    Attributes
    ----------
    name : str
        Name of the node, if any.
    children : list
        Child nodes referenced by node_key.
    matrix : list of lists
        Matrix representing the displacement from node's parent to the node.
    mesh_index : int
        Index of the associated mesh within the JSON, if any.
    weights : list of ints
        Weights used for computing morph targets in the attached mesh, if any.
    position : tuple
        xyz-coordinates of the node, calculated from the matrix.
    transform : list of lists
        Matrix representing the displacement from the root node to the node.
    mesh_data : :class:`MeshData`
        Contains mesh data, if any.
    node_key : int or str
        Key of the node used in :attr:`GLTFScene.nodes`.
    camera : int--only referencing the information in the JSON?
    skin : int--only referencing the information in the JSON?
    extras : object
        Application-specific data.
    """
    def __init__(self):
        self.name = None
        self.children = []
        self._matrix = None
        self._translation = None
        self._rotation = None
        self._scale = None
        self.mesh_index = None
        self.weights = None

        self.position = None
        self.transform = None
        self._mesh_data = None
        self.node_key = None  # think this over

        self.camera = None
        self.skin = None
        self.extras = None

    @property
    def mesh_data(self):
        return self._mesh_data

    @mesh_data.setter
    def mesh_data(self, value):
        if not value.faces or not value.vertices:
            raise Exception('Invalid mesh at node {}.  Meshes are expected '
                            'to have vertices and faces.'.format(self.node_key))
        self._mesh_data = value

    @property
    def translation(self):
        return self._translation

    @translation.setter
    def translation(self, value):
        if value is None:
            self._translation = value
            return
        if self._matrix:
            raise Exception('Cannot set translation when matrix is set.')
        if not isinstance(value, list) or len(value) != 3:
            raise Exception('Invalid translation. Translations are expected to be of the form [x, y, z].')
        self._translation = value

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        if value is None:
            self._rotation = value
            return
        if self._matrix:
            raise Exception('Cannot set rotation when matrix is set.')
        if not isinstance(value, list) or len(value) != 4 or sum([q**2 for q in value]) != 1:
            raise Exception('Invalid rotation.  Rotations are expected to be given as '
                            'unit quaternions of the form [q1, q2, q3, q4]')
        self._rotation = value

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        if value is None:
            self._scale = value
            return
        if self._matrix:
            raise Exception('Cannot set scale when matrix is set.')
        if not isinstance(value, list) or len(value) != 3:
            raise Exception('Invalid scale.  Scales are expected to be of the form [s1, s2, s3]')
        self._scale = value

    @property
    def matrix(self):
        if not self.translation and not self.rotation and not self.scale and not self._matrix:
            return identity_matrix(4)
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        if value is None:
            self._matrix = value
            return
        if self.translation or self.rotation or self.scale:
            raise Exception('Cannot set matrix when translation, rotation or scale is set.')
        if not isinstance(value, list) or not value or not value[0] or not isinstance(value[0], list):
            raise Exception('Invalid matrix. A list of lists is expected.')
        if len(value) != 4 or len(value[0]) != 4:
            raise Exception('Invalid matrix. A 4x4 matrix is expected.')
        if value[3] != [0, 0, 0, 1]:
            raise Exception('Invalid matrix.  A matrix without shear or skew is expected.  It must be of '
                            'the form TRS, where T is a translation, R is a rotation and S is a scaling.')
        self._matrix = value

    def get_matrix_from_trs(self):
        matrix = identity_matrix(4)
        if self.translation:
            translation = matrix_from_translation(self.translation)
            matrix = multiply_matrices(matrix, translation)
        if self.rotation:
            rotation = matrix_from_quaternion(self.rotation)
            matrix = multiply_matrices(matrix, rotation)
        if self.scale:
            scale = matrix_from_scale_factors(self.scale)
            matrix = multiply_matrices(matrix, scale)
        return matrix


class GLTF(object):
    """Read files in glTF format.
    Caution: Cameras, materials and skins have limited support, and their data may be lost or corrupted.
    Extensions and most other application specific data are completely unsupported,
    and their data will be lost upon import.
    See Also
    --------
    * https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/figures/gltfOverview-2.0.0b.png

    """
    def __init__(self, filepath=None):
        self.filepath = filepath
        self._scenes = []
        self.default_scene_index = None
        self.extras = None
        # in the Exporter I don't want to call the reader
        self.ancillaries = {}

        self._is_parsed = False
        self._reader = None
        self._parser = None

    def read(self):
        self._reader = GLTFReader(self.filepath)
        self._parser = GLTFParser(self._reader)
        self._is_parsed = True

        self._scenes = self._parser.scenes
        self.default_scene_index = self._parser.default_scene_index
        self.extras = self._parser.extras
        self.ancillaries.update({
            attr: self._reader.json.get(attr)
            for attr in ['cameras', 'materials', 'textures', 'samplers']
            if self._reader.json.get(attr)
        })
        self.ancillaries.update({
            'images': self._reader.image_data,
            'skins': self._reader.skin_data,
            'animations': self._reader.animation_data,
        })

    @property
    def reader(self):
        if not self._is_parsed:
            self.read()
        return self._reader

    @property
    def parser(self):
        if not self._is_parsed:
            self.read()
        return self._parser

    @property
    def scenes(self):
        return self._scenes

    @scenes.setter
    def scenes(self, value):
        if not self._is_parsed:
            self._is_parsed = True
        self._scenes = value

    def export(self, embed_data=False):
        GLTFExporter(self.filepath, self.scenes, embed_data, self.default_scene_index, self.extras, self.ancillaries)


class GLTFExporter(object):
    """
    """

    def __init__(self, filepath, scenes, embed_data, default_scene_index=0, extras=None, ancillaries=None):
        self.gltf_filepath = filepath
        self.dirname = None
        self.filename = None
        self.ext = None

        self.embed_data = embed_data
        self.scenes = scenes
        self.default_scene_index = default_scene_index
        self.extras = extras
        self.ancillaries = ancillaries or {}

        self._gltf_dict = None
        self._node_key_index_dict = {}
        self._buffer = b''  # should i make a buffer class? and this could be a list of those...

        self.set_path_attributes()
        self.export()

    def export(self):
        self.validate_scenes()
        self._gltf_dict = self.get_generic_gltf_dict()
        self.add_scenes()
        self.add_ancillaries()
        self.add_buffer()

        gltf_json = json.dumps(self._gltf_dict)

        # how does ironpython deal with writing these things???
        if self.ext == '.gltf':
            with open(self.gltf_filepath, 'w') as f:
                f.write(gltf_json)
                # write newline?
            if not self.embed_data and len(self._buffer) > 0:
                with open(self.get_bin_path(), 'wb') as f:
                    f.write(self._buffer)

        if self.ext == '.glb':
            with open(self.gltf_filepath, 'wb') as f:
                gltf_data = gltf_json.encode()

                length_gltf = len(gltf_data)
                spaces_gltf = (4 - (length_gltf & 3)) & 3
                length_gltf += spaces_gltf

                length_bin = len(self._buffer)
                zeros_bin = (4 - (length_bin & 3)) & 3
                length_bin += zeros_bin

                length = 12 + 8 + length_gltf
                if length_bin > 0:
                    length += 8 + length_bin

                f.write('glTF'.encode('ascii'))  # little endian because 1 byte per character
                f.write(struct.pack('<I', 2))
                f.write(struct.pack('<I', length))

                f.write(struct.pack('<I', length_gltf))
                f.write('JSON'.encode('ascii'))
                f.write(gltf_data)
                for i in range(0, spaces_gltf):
                    f.write(' '.encode())

                if length_bin > 0:
                    f.write(struct.pack('<I', length_bin))
                    f.write('BIN\0'.encode())
                    f.write(self._buffer)
                    for i in range(0, zeros_bin):
                        f.write('\0'.encode())

    def add_buffer(self):
        buffer = {'byteLength': len(self._buffer)}
        if self.embed_data:
            buffer['uri'] = 'data:application/octet-stream,base64;' + base64.b64encode(self._buffer).decode('ascii')
        elif self.ext == '.gltf':
            buffer['uri'] = self.get_bin_filename()
        self._gltf_dict['buffers'] = [buffer]

    def add_ancillaries(self):
        for attr in ['cameras', 'materials', 'textures', 'samplers']:
            if not self.ancillaries.get(attr):
                continue
            if self.is_jsonable(self.ancillaries[attr], '{} list'.format(attr)):
                if attr == 'cameras':
                    self.validate_cameras()
                self._gltf_dict[attr] = self.ancillaries[attr]

        images_list = []
        for image_data in self.ancillaries['images']:
            image_dict = {}
            if image_data.name:
                image_dict['name'] = image_data.name
            if image_data.extras:
                image_dict['extras'] = image_data.extras

            if image_data.mime_type:
                image_dict['mimeType'] = image_data.mime_type
            if image_data.uri:
                image_dict['uri'] = image_data.uri

            if image_data.data and self.embed_data:
                image_dict['uri'] = ('data:' +
                                     (image_data.media_type if image_data.media_type else '') +
                                     ';base64,' +
                                     base64.b64encode(image_data.data))

            if image_data.data and not self.embed_data:
                image_dict['bufferView'] = self.get_buffer_view(image_data.data)

            images_list.append(image_dict)
        if images_list:
            self._gltf_dict['images'] = images_list

        skins_list = []
        for skin_data in self.ancillaries['skins']:
            skin_dict = {'joints': [
                self._node_key_index_dict.get(item)
                for item in skin_data.joints
                if self._node_key_index_dict.get(item)
            ]}
            if skin_data.skeleton:
                skin_dict['skeleton'] = skin_data.skeleton
            if skin_data.name:
                skin_dict['name'] = skin_data.name
            if skin_data.extras:
                skin_dict['extras'] = skin_data.extras
            if skin_data.inverse_bind_matrices:
                skin_dict['inverseBindMatrices'] = self.get_accessor(skin_data.inverse_bind_matrices, COMPONENT_TYPE_FLOAT, TYPE_MAT4)

            skins_list.append(skin_dict)
        if skins_list:
            self._gltf_dict['skins'] = skins_list

        animations_list = []
        for animation_data in self.ancillaries['animations']:
            animation_dict = {'channels': animation_data.channels}
            samplers = []
            for sampler_data in animation_data.samplers:
                input_accessor = self.get_accessor(sampler_data.input, COMPONENT_TYPE_FLOAT, TYPE_SCALAR, include_bounds=True)
                type_ = TYPE_VEC3
                if isinstance(sampler_data.output[0], int):
                    type_ = TYPE_SCALAR
                elif len(sampler_data.output[0]) == 4:
                    type_ = TYPE_VEC4
                output_accessor = self.get_accessor(sampler_data.output, COMPONENT_TYPE_FLOAT, type_)
                sampler_dict = {
                    'input': input_accessor,
                    'output': output_accessor,
                }
                if sampler_data.interpolation:
                    sampler_dict['interpolation'] = sampler_data.interpolation
                if sampler_data.extras:
                    sampler_dict['extras'] = sampler_data.extras
                samplers.append(sampler_dict)
            animation_dict['samplers'] = samplers
            if animation_data.name:
                animation_dict['name'] = animation_data.name
            if animation_data.extras:
                animation_dict['extras'] = animation_data.extras
            animations_list.append(animation_dict)
        if animations_list:
            self._gltf_dict['animations'] = animations_list

    def validate_cameras(self):
        for index, camera in enumerate(self.ancillaries['cameras']):
            if not camera.get('type'):
                raise Exception('Invalid camera at index {}.  Expecting "type" attribute.'.format(index))

    def is_jsonable(self, obj, obj_name):
        try:
            json.dumps(obj)
        except (TypeError, OverflowError):
            raise Exception('The {} is not a valid JSON object.'.format(obj_name))
        return True

    def validate_scenes(self):
        if self.default_scene_index is not None and not (
            isinstance(self.default_scene_index, int) and 0 <= self.default_scene_index < len(self.scenes)
        ):
            raise Exception('Invalid default scene index.')

        node_keys = set()

        for index, scene in enumerate(self.scenes):
            nodes = scene.nodes
            if not nodes.get(DEFAULT_ROOT_NAME):
                raise Exception('Cannot find root node for scene at index {}.  '
                                'Root node is distinguished by having {} as the node_key'.format(index, DEFAULT_ROOT_NAME))

            for node_key in nodes.keys():
                if node_key == DEFAULT_ROOT_NAME:
                    continue
                if node_key in node_keys:
                    raise Exception('Node keys (except roots) must be unique across scenes.')
                node_keys.add(node_key)  # or i could uniqueify them here....

            scene.is_tree()

    def get_generic_gltf_dict(self):
        asset_dict = {'version': '2.0'}
        if self.extras:
            asset_dict['extras'] = self.extras
        return {'asset': asset_dict}

    def add_scenes(self):
        if not self.scenes:
            return
        nodes = []
        scenes = []
        for gltf_scene in self.scenes:
            descendents = {node_key: node for node_key, node in gltf_scene.nodes.items() if node_key != DEFAULT_ROOT_NAME}
            self._node_key_index_dict.update({node_key: index + len(nodes) for index, node_key in enumerate(descendents)})
            nodes += [None] * len(descendents)

            for node_key, node in descendents.items():
                node_dict = {}
                if node.name:
                    node_dict['name'] = node.name
                if node.children:
                    node_dict['children'] = [self._node_key_index_dict[key] for key in node.children]
                if node.matrix and node.matrix != identity_matrix(4):
                    node_dict['matrix'] = self.matrix_to_col_major_order(node.matrix)
                else:
                    if node.translation:
                        node_dict['translation'] = node.translation
                    if node.rotation:
                        node_dict['rotation'] = node.rotation
                    if node.scale:
                        node_dict['scale'] = node.scale
                if node.mesh_data:
                    node_dict['mesh'] = self.process_mesh_data(node.mesh_data)
                if node.camera is not None:
                    # validate that camera exists?
                    node_dict['camera'] = node.camera
                if node.skin is not None:
                    # validate that skin exists?
                    node_dict['skin'] = node.skin
                if node.extras:
                    node_dict['extras'] = node.extras

                nodes[self._node_key_index_dict[node_key]] = node_dict

            scene_dict = {}
            if gltf_scene.nodes[DEFAULT_ROOT_NAME].children:
                scene_dict['nodes'] = [self._node_key_index_dict[key] for key in gltf_scene.nodes[DEFAULT_ROOT_NAME].children]
            if gltf_scene.name:
                scene_dict['name'] = gltf_scene.name
            if gltf_scene.extras:
                scene_dict['extras'] = gltf_scene.extras
            scenes.append(scene_dict)

        self._gltf_dict['scenes'] = scenes
        self._gltf_dict['nodes'] = nodes

    def matrix_to_col_major_order(self, matrix):
        return [matrix[i][j] for j in range(4) for i in range(4)]

    def process_mesh_data(self, mesh_data):
        mesh_dict = {}
        if mesh_data.mesh_name:
            mesh_dict['name'] = mesh_data.mesh_name
        if mesh_data.weights:
            mesh_dict['weights'] = mesh_data.weights
        if mesh_data.extras and self.is_jsonable(mesh_data.extras, 'mesh extras object'):
            mesh_dict['extras'] = mesh_data.extras

        primitives = []
        for primitive_data in mesh_data.primitive_data_list:
            primitive = {'indices': self.get_accessor(primitive_data.indices, COMPONENT_TYPE_UNSIGNED_INT, TYPE_SCALAR)}  # indices are wrapped? or no?
            if primitive_data.material is not None:
                # validate that material exists
                primitive['material'] = primitive_data.material
            if primitive_data.mode is not None:
                primitive['mode'] = primitive_data.mode
            if primitive_data.extras:
                primitive['extras'] = primitive_data.extras
            attributes = {}
            for attr in primitive_data.attributes:
                component_type = COMPONENT_TYPE_UNSIGNED_INT if attr.startswith('JOINT') else COMPONENT_TYPE_FLOAT
                type_ = TYPE_VEC3
                if len(primitive_data.attributes[attr][0]) == 4:
                    type_ = TYPE_VEC4
                if len(primitive_data.attributes[attr][0]) == 2:
                    type_ = TYPE_VEC2
                attributes[attr] = self.get_accessor(primitive_data.attributes[attr], component_type, type_, True)
            if attributes:
                primitive['attributes'] = attributes

            targets = {}
            for attr in primitive_data.targets:
                component_type = COMPONENT_TYPE_FLOAT
                type_ = TYPE_VEC3
                targets[attr] = self.get_accessor(primitive_data.attributes[attr], component_type, type_, True)
            if targets:
                primitive['targets'] = targets

            primitives.append(primitive)

        mesh_dict['primitives'] = primitives

        self._gltf_dict.setdefault('meshes', []).append(mesh_dict)
        return len(self._gltf_dict['meshes']) - 1

    def get_accessor(self, data, component_type, type_, include_bounds=False):
        count = len(data)

        fmt_char = COMPONENT_TYPE_ENUM[component_type]
        fmt = '<' + fmt_char * NUM_COMPONENTS_BY_TYPE_ENUM[type_]

        component_size = struct.calcsize('<' + fmt_char)
        if component_type == 'MAT2' and component_size == 1:
            fmt = '<FFxxFFxx'.replace('F', fmt_char)
        elif component_type == 'MAT3' and component_size == 1:
            fmt = '<FFFxFFFxFFFx'.replace('F', fmt_char)
        elif component_type == 'MAT3' and component_size == 2:
            fmt = '<FFFxxFFFxxFFFxx'.replace('F', fmt_char)

        component_len = struct.calcsize(fmt)

        size = count * component_len
        size += (4 - size % 4) % 4  # ensure bytes_ length is divisible by 4

        bytes_ = bytearray(size)

        for i, datum in enumerate(data):
            if isinstance(datum, int) or isinstance(datum, float):  # should i just wrap (or leave wrapped) the scalars?  if type_ == TYPE_SCALAR?
                datum = (datum, )  # this is horrible
            struct.pack_into(fmt, bytes_, (i * component_len), *datum)

        buffer_view_index = self.get_buffer_view(bytes_)
        accessor_dict = {
            'bufferView': buffer_view_index,
            'count': count,
            'componentType': component_type,
            'type': type_,
        }
        if include_bounds:
            try:
                _ = [e for e in data[0]]
                minimum = tuple(map(min, zip(*data)))
                maximum = tuple(map(max, zip(*data)))
            except TypeError:
                minimum = (min(data),)
                maximum = (max(data),)
            accessor_dict['min'] = minimum
            accessor_dict['max'] = maximum

        self._gltf_dict.setdefault('accessors', []).append(accessor_dict)

        return len(self._gltf_dict['accessors']) - 1

    def get_buffer_view(self, bytes_):
        byte_offset = self.update_buffer(bytes_)
        buffer_view_dict = {
            'buffer': 0,
            'byteLength': len(bytes_),
            'byteOffset': byte_offset,
        }

        self._gltf_dict.setdefault('bufferViews', []).append(buffer_view_dict)

        return len(self._gltf_dict['bufferViews']) - 1

    def update_buffer(self, bytes_):
        byte_offset = len(self._buffer)
        self._buffer += bytes_
        return byte_offset

    def get_bin_path(self):
        return os.path.join(self.dirname, self.filename + '.bin')
        return self.dirname +  '.bin'

    def get_bin_filename(self):
        return self.filename + '.bin'

    def set_path_attributes(self):
        dirname, basename = os.path.split(self.gltf_filepath)
        root, ext = os.path.splitext(basename)
        self.dirname = dirname
        self.filename = root
        self.ext = ext.lower()


class GLTFReader(object):
    """"Read the contents of a *glTF* or *glb* version 2 file using the json library.
    Uses ideas from Khronos Group's glTF-Blender-IO.
    Caution: Extensions are not supported and their data may be lost.
    Caution: Data for materials, textures, animations, images, skins and cameras are saved,
        but are not processed or used.

    Parameters
    ----------
    filepath: str
        Path to the file.
        Binary files containing the mesh data are assumed to be in the same directory.

    Attributes
    ----------
    filepath : str
        String containing the path to the glTF.
    json : dict
        Dictionary object containing the contents of the glTF.
    data : list
        List of lists containing data read from binary files.
    image_data : list
        List containing binary image data.
    """
    def __init__(self, filepath):
        self.filepath = filepath

        self.json = None
        self.data = []
        self.image_data = []
        self.skin_data = []
        self.animation_data = []

        self._content = None
        self._glb_buffer = None
        self._buffers = {}

        self.read()

    def read(self):
        with open(self.filepath, 'rb') as f:
            self._content = memoryview(f.read())

        is_glb = self._content[:4] == b'glTF'

        if not is_glb:
            content = self._content.tobytes().decode('utf-8')
            self.json = json.loads(content)
        else:
            self.load_from_glb()

        self.release_buffer(self._content)
        self._content = None

        self.check_version()

        if self.json:
            for accessor in self.json.get('accessors', []):
                accessor_data = self.access_data(accessor)
                self.data.append(accessor_data)

            for image in self.json.get('images', []):
                image_data = ImageData()
                image_data.name = image.get('name')
                image_data.mime_type = image.get('mimeType')
                image_data.extras = image.get('extras')

                if 'bufferView' in image:
                    image_data.data = self.get_attr_data(image, 'bufferView')
                if 'uri' in image:
                    if self.is_data_uri(image['uri']):
                        image_data.data = base64.b64decode(self.get_data_uri_data(image['uri']))
                        image_data.media_type = self.get_media_type(image['uri'])
                    else:
                        image_data.uri = image['uri']
                self.image_data.append(image_data)

            # do these belong here? i think yes for utility
            for skin in self.json.get('skins', []):
                skin_data = SkinData(skin['joints'])
                if 'inverseBindMatrices' in skin:
                    skin_data.inverse_bind_matrices = self.data[skin['inverseBindMatrices']]
                skin_data.skeleton = skin.get('skeleton')
                skin_data.name = skin.get('name')
                skin_data.extras = skin.get('extras')
                self.skin_data.append(skin_data)

            for animation in self.json.get('animations', []):
                sampler_data_list = []
                for sampler in animation['samplers']:
                    input_ = self.data[sampler['input']]
                    output = self.data[sampler['output']]
                    sampler_data = SamplerData(input_, output, sampler.get('interpolation'), sampler.get('extras'))
                    sampler_data_list.append(sampler_data)
                animation_data = AnimationData(animation.get('channels'), sampler_data_list, animation.get('name'), animation.get('extras'))
                self.animation_data.append(animation_data)

        self.release_buffers()

    def get_media_type(self, string):
        pattern = 'data:([\w/]+)(?<![;,])'
        result = re.search(pattern, string)
        return result.group(1)

    def load_from_glb(self):
        header = struct.unpack_from('<4sII', self._content)
        file_size = header[2]

        if file_size != len(self._content):
            raise Exception('Bad glTF.  File size does not match.')

        offset = 12

        # load json
        type_, _length, json_bytes, offset = self.load_chunk(offset)
        if type_ != b'JSON':
            raise Exception('Bad glTF.  First chunk not in JSON format')
        json_str = json_bytes.tobytes().decode('utf-8')
        self.json = json.loads(json_str)

        # load binary buffer
        if offset < len(self._content):
            type_, _length, bytes_, offset = self.load_chunk(offset)
            if type_ == b'BIN\0':
                self._glb_buffer = bytes_

    def load_chunk(self, offset):
        chunk_header = struct.unpack_from('<I4s', self._content, offset)
        length = chunk_header[0]
        type_ = chunk_header[1]
        data = self._content[offset + 8: offset + 8 + length]

        return type_, length, data, offset + 8 + length

    def check_version(self):
        version = self.json['asset']['version']
        if version != '2.0':
            raise Exception('Invalid glTF version.  Version 2.0 expected.')

    def get_attr_data(self, obj, attr):
        if attr not in obj:
            return None
        buffer_view_index = obj[attr]
        buffer_view = self.json['bufferViews'][buffer_view_index]
        buffer = self.get_buffer(buffer_view['buffer'])
        offset = buffer_view.get('byteOffset', 0)
        length = buffer_view['byteLength']
        return buffer[offset: offset + length].tobytes()

    def access_data(self, accessor):
        count = accessor['count']
        component_type = accessor['componentType']
        type_ = accessor['type']
        accessor_offset = accessor.get('byteOffset', 0)
        num_components = NUM_COMPONENTS_BY_TYPE_ENUM[type_]

        # This situation indicates use of an extension.
        if 'sparse' not in accessor and 'bufferView' not in accessor:
            return None

        if 'bufferView' in accessor:
            buffer_view_index = accessor['bufferView']
            data = self.read_from_buffer_view(
                buffer_view_index,
                count,
                component_type,
                accessor_offset,
                num_components
            )
        else:
            data = self.get_generic_data(num_components, count)

        if 'sparse' in accessor:
            sparse_data = accessor['sparse']
            sparse_count = sparse_data['count']

            sparse_indices_data = sparse_data['indices']
            sparse_indices_buffer_view_index = sparse_indices_data['bufferView']
            sparse_indices_component_type = sparse_indices_data['componentType']
            sparse_indices = self.read_from_buffer_view(
                sparse_indices_buffer_view_index,
                sparse_count,
                sparse_indices_component_type,
                accessor_offset,
                NUM_COMPONENTS_BY_TYPE_ENUM['SCALAR']
            )

            sparse_values_data = sparse_data['values']
            sparse_values_buffer_view_index = sparse_values_data['bufferView']
            sparse_values = self.read_from_buffer_view(
                sparse_values_buffer_view_index,
                sparse_count,
                component_type,
                accessor_offset,
                num_components
            )

            for index, data_index in enumerate(sparse_indices):
                data[data_index] = sparse_values[index]

            if accessor.get('normalized', False):
                for index, tuple_ in enumerate(data):
                    new_tuple = ()
                    for i in tuple_:
                        if component_type == COMPONENT_TYPE_BYTE:
                            new_tuple += (max(float(i / 127.0), -1.0),)
                        elif component_type == COMPONENT_TYPE_UNSIGNED_BYTE:
                            new_tuple += (float(i / 255.0),)
                        elif component_type == COMPONENT_TYPE_SHORT:
                            new_tuple += (max(float(i / 32767.0), -1.0),)
                        elif component_type == COMPONENT_TYPE_UNSIGNED_SHORT:
                            new_tuple += (i / 65535.0,)
                        else:
                            new_tuple += (float(i),)
                    data[index] = new_tuple

        return data

    def get_generic_data(self, num_components, count):
        return [(0, ) * num_components for _ in range(count)]

    def read_from_buffer_view(self, buffer_view_index, count, component_type, accessor_offset, num_components):
        buffer_view = self.json['bufferViews'][buffer_view_index]

        buffer_view_offset = buffer_view.get('byteOffset', 0)
        offset = accessor_offset + buffer_view_offset

        format_char = COMPONENT_TYPE_ENUM[component_type]
        format_ = '<' + format_char * num_components

        expected_length = struct.calcsize(format_)

        component_size = struct.calcsize('<' + format_char)
        if component_type == 'MAT2' and component_size == 1:
            format_ = '<FFxxFF'.replace('F', format_char)
            expected_length = 8
        elif component_type == 'MAT3' and component_size == 1:
            format_ = '<FFFxFFFxFFF'.replace('F', format_char)
            expected_length = 12
        elif component_type == 'MAT3' and component_size == 2:
            format_ = '<FFFxxFFFxxFFF'.replace('F', format_char)
            expected_length = 24

        byte_stride = buffer_view.get('byteStride', expected_length)

        unpack_from = struct.Struct(format_).unpack_from

        buffer_index = buffer_view['buffer']
        buffer = self.get_buffer(buffer_index)

        data = [
            unpack_from(buffer[i: i + byte_stride].tobytes())
            for i in range(offset, offset + count * byte_stride, byte_stride)
        ]

        if num_components == 1:
            data = [item[0] for item in data]  # unwrap scalars from tuple

        return data

    def get_buffer(self, buffer_index):
        if buffer_index in self._buffers:
            return self._buffers[buffer_index]

        uri = self.json['buffers'][buffer_index].get('uri', None)

        if not uri:
            buffer = self._glb_buffer
        elif self.is_data_uri(uri):
            string = self.get_data_uri_data(uri)
            buffer = memoryview(base64.b64decode(string))
        else:
            filepath = self.get_filepath(uri)
            with open(filepath, 'rb') as f:
                buffer = memoryview(f.read())

        self._buffers[buffer_index] = buffer

        return buffer

    def release_buffer(self, buffer):
        try:
            buffer.release()
        except AttributeError:
            pass

    def release_buffers(self):
        self.release_buffer(self._glb_buffer)
        self._glb_buffer = None
        for i in range(len(self._buffers)):
            self.release_buffer(self._buffers[i])
        self._buffers = {}

    def is_data_uri(self, uri):
        return uri.startswith('data:')

    def get_data_uri_data(self, uri):
        split_uri = uri.split(',')
        return split_uri[-1]

    def get_filepath(self, uri):
        dir_path = os.path.dirname(self.filepath)
        return os.path.join(dir_path, uri)


class GLTFParser(object):
    """Parse the contents of the reader to read and parse the associated binary files
    and create objects digestible by COMPAS.

    Parameters
    ----------
    reader : :class:`GLTFReader`

    Attributes
    ----------
    reader : :class:`GLTFReader`
    default_scene_index : int
        Index of the default scene.
    scenes : list of :class:`GLTFScene`
        List of dictionaries containing the information of each scene.
    """
    def __init__(self, reader):
        self.reader = reader
        self.default_scene_index = None  # maybe check that there is a scene before setting this to 0
        self.scenes = []
        self.extras = None

        self.parse()

    def parse(self):
        self.default_scene_index = self.get_default_scene()
        self.extras = self.get_extras()

        for scene in self.reader.json.get('scenes', []):
            scene_obj = self.get_initial_scene(scene)
            self.process_children('root', scene_obj)
            self.scenes.append(scene_obj)

    def get_extras(self):
        return self.reader.json.get('extras')

    def get_default_scene(self):
        return self.reader.json.get('scene')

    def get_initial_scene(self, scene):
        scene_obj = GLTFScene()
        scene_obj.name = scene.get('name')
        scene_obj.extras = scene.get('extras')
        scene_obj.nodes[DEFAULT_ROOT_NAME].children = scene.get('nodes', [])

        return scene_obj

    def process_children(self, parent_key, scene_obj):
        child_keys = scene_obj.nodes[parent_key].children
        for key in child_keys:
            gltf_node = GLTFNode()

            node = self.reader.json['nodes'][key]

            gltf_node.name = node.get('name')
            gltf_node.children = node.get('children', [])
            gltf_node.translation = node.get('translation')
            gltf_node.rotation = node.get('rotation')
            gltf_node.scale = node.get('scale')
            gltf_node.matrix = self.get_matrix(node)
            gltf_node.weights = node.get('weights')
            gltf_node.mesh_index = node.get('mesh')
            gltf_node.camera = node.get('camera')
            gltf_node.skin = node.get('skin')
            gltf_node.extras = node.get('extras')

            gltf_node.transform = multiply_matrices(
                scene_obj.nodes[parent_key].transform,
                gltf_node.matrix or gltf_node.get_matrix_from_trs()
            )
            gltf_node.position = inhomogeneous_transformation(gltf_node.transform, scene_obj.nodes[DEFAULT_ROOT_NAME].position)
            gltf_node.node_key = key

            if gltf_node.mesh_index is not None:
                gltf_node.mesh_data = self.get_mesh_data(gltf_node)

            scene_obj.nodes[key] = gltf_node

            self.process_children(key, scene_obj)

    def get_matrix(self, node):
        if 'matrix' in node:
            return get_matrix_from_col_major_list(node['matrix'])
        return None

    def get_mesh_data(self, gltf_node):
        mesh = self.reader.json['meshes'][gltf_node.mesh_index]
        mesh_name = mesh.get('name')
        extras = mesh.get('extras')
        primitives = mesh['primitives']
        weights = self.get_weights(mesh, gltf_node)

        primitive_data_list = []

        for primitive in primitives:
            if 'POSITION' not in primitive['attributes']:
                continue

            attributes = {}
            for attr, attr_accessor_index in primitive['attributes'].items():
                attributes[attr] = self.reader.data[attr_accessor_index]

            indices = self.get_indices(primitive, len(attributes['POSITION']))

            target_list = []
            for target in primitive.get('targets', []):
                target_data = {attr: self.reader.data[accessor_index] for attr, accessor_index in target.items()}
                target_list.append(target_data)

            primitive_data_list.append(PrimitiveData(
                attributes,
                indices,
                primitive.get('material'),
                primitive.get('mode'),
                target_list,
                primitive.get('extras'),
            ))

        return MeshData(mesh_name, weights, primitive_data_list, extras)

    def get_weights(self, mesh, gltf_node):
        weights = mesh.get('weights', None)
        weights = gltf_node.weights or weights
        return weights

    def get_indices(self, primitive, num_vertices):
        if 'indices' not in primitive:
            return self.get_generic_indices(num_vertices)
        indices_accessor_index = primitive['indices']
        return self.reader.data[indices_accessor_index]

    def get_generic_indices(self, num_vertices):
        return list(range(num_vertices))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas

    from compas.datastructures import Mesh, Network, mesh_transformed
    from compas.utilities import download_file_from_remote
    from compas_viewers.multimeshviewer import MultiMeshViewer

    # source_glb = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/BoxInterleaved/glTF-Binary/BoxInterleaved.glb'
    # filepath_glb = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'BoxInterleaved.glb')

    # source_glb = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/GearboxAssy/glTF/GearboxAssy.gltf'
    # filepath_glb = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'GearboxAssy.gltf')

    # source_glb = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/SimpleMorph/glTF-Embedded/SimpleMorph.gltf'
    # filepath_glb = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'SimpleMorph.gltf')

    # source_glb = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Duck/glTF-Embedded/Duck.gltf'
    # filepath_glb = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'Duck.gltf')

    # source_glb = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/MorphPrimitivesTest/glTF-Binary/MorphPrimitivesTest.glb'
    # filepath_glb = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'MorphPrimitivesTest.glb')

    source_glb = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/SimpleMeshes/glTF/SimpleMeshes.gltf'
    source_bin = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/SimpleMeshes/glTF/triangle.bin'
    filepath_glb = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'SimpleMeshes.gltf')
    filepath_bin = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'triangle.bin')

    download_file_from_remote(source_bin, filepath_bin, overwrite=False)

    gltf = GLTF(filepath_glb)
    gltf.read()

    default_scene_index = gltf.default_scene_index or 0
    nodes = gltf.scenes[default_scene_index].nodes

    vrts = {name: gltf_node.position for name, gltf_node in nodes.items()}
    edges = [
        (node.node_key, child)
        for node in gltf.scenes[default_scene_index].nodes.values()
        for child in node.children
    ]

    scene_tree = Network.from_vertices_and_edges(vrts, edges)
    scene_tree.plot()

    transformed_meshes = []

    for vertex_name, gltf_node in nodes.items():
        if gltf_node.mesh_data is None:
            continue
        t = gltf_node.transform
        m = Mesh.from_vertices_and_faces(gltf_node.mesh_data.vertices, gltf_node.mesh_data.faces)
        transformed_mesh = mesh_transformed(m, t)
        transformed_meshes.append(transformed_mesh)

    viewer = MultiMeshViewer()
    viewer.meshes = transformed_meshes
    viewer.show()
