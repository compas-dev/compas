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
import struct
from collections import defaultdict
from array import array
from collections import defaultdict

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

DEFAULT_ROOT_NAME = 'root'


class Primitive(object):
    def __init__(self, attributes, indices, material, mode, targets, extras):
        self.attributes = attributes  # dict of position, normal, tangent, etc
        self.indices = indices  # defines faces
        self.material = material  # int referencing something in the json
        self.mode = mode  # how to group the indices
        self.targets = targets  # morph targets
        self.extras = extras  # other stuff


class MeshData(object):
    """Object containing COMPAS consumable data for creating a mesh.

    Attributes
    ----------
    vertices : list
        List of the xyz-coordinates of the vertices of the mesh.
    faces : list of tuples
        List of the faces of the mesh represented by tuples of vertices referenced by index.
    mesh_name : str
        Name of the mesh, if any.
    vertex_data : list
        List of dictionaries containing vertex data, eg textures, if any.
    extras : object
        Application-specific data.
    """
    def __init__(self, faces=None, vertex_data=None, mesh_name=None, extras=None):
        self._faces = None

        self.vertices = []
        self.faces = faces or []
        self.mesh_name = mesh_name
        self.vertex_data = vertex_data or []
        self.extras = extras

    @property
    def vertices(self):
        return [vertex['POSITION'] for vertex in self.vertex_data]

    @vertices.setter
    def vertices(self, value):
        self.validate_vertices(value)
        self.vertex_data = [{'POSITION': position} for position in value]

    def validate_vertices(self, vertices):
        for vertex in vertices:
            if len(vertex) != 3:
                raise Exception('Invalid mesh.  Vertices are expected to be points in 3-space.')

    @property
    def faces(self):
        return self._faces

    @faces.setter
    def faces(self, value):
        self.validate_faces(value)
        self._faces = value

    def validate_faces(self, faces):
        if not faces:
            return
        if len(faces[0]) > 3:
            raise Exception('Invalid mesh. Expected mesh composed of points, lines xor triangles.')
        for face in faces:
            if len(face) != len(faces[0]):
                # This restriction could be removed by splitting into multiple primitives.
                raise NotImplementedError('Invalid mesh. Expected mesh composed of points, lines xor triangles.')

    @classmethod
    def from_mesh(cls, mesh):
        vertices, faces = mesh.to_vertices_and_faces()
        mesh_data = cls()
        mesh_data.vertices = vertices
        mesh_data.faces = faces
        return mesh_data


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
        self.mesh_index = None
        self.weights = None

        self.position = None
        self.transform = None
        self._mesh_data = None
        self.node_key = None  # should i depend on this attribute never changing?
        # i think this will solve my skins et al woes, but do i trust the user not to fuck with this?
        # prefix with an underscore and hope for the best?
        # i need to be careful as a developer not to use this outside of contexts
        # where the damn thing was loaded from a file, seems hairy

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
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        if not isinstance(value, list) or not value or not isinstance(value[0], list) or not value[0]:
            raise Exception('Invalid matrix.')
        if len(value) != 4 or len(value[0]) != 4:
            raise Exception('Invalid matrix.')
        if matrix_determinant(value) == 0:
            raise Exception('Invalid matrix. Expecting a matrix of the form TRS, '
                            'where T is a translation, R is a rotation and S is a scaling.')
        if value[3] != [0, 0, 0, 1]:
            raise Exception('Invalid matrix. Expecting a matrix of the form TRS, '
                            'where T is a translation, R is a rotation and S is a scaling.')
        self._matrix = value


class GLTF(object):
    """Read files in glTF format.
    Caution: Cameras, materials and skins have limited support, and their data may be lost or corrupted.
    Animations, extensions and most other application specific data are completely unsupported,
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
            for attr in ['cameras', 'materials', 'skins', 'images', 'textures', 'samplers']
            if self._reader.json.get(attr)
        })
        # haven't added yet images, textures, samplers

        self.ancillaries['image_data'] = self._reader.image_data
        self.ancillaries['skin_data'] = self._reader.skin_data

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
        if not self._is_parsed:
            self._is_parsed = True
        return self._scenes

    def export(self):
        GLTFExporter(self.filepath, self.scenes, self.default_scene_index, self.extras, self.ancillaries)
        # export to already established filepath
        # must choose gtlf, gtlf-embedded, glb
        # for the first, will write bin to same filepath gtlf -> bin


class GLTFExporter(object):
    """
    """

    def __init__(self, filepath, scenes, default_scene_index=0, extras=None, ancillaries=None):
        self.filepath = filepath
        self.bin_filepath = self.get_bin_filepath()  # this is inflexible, maybe want multiple .bins
        self.scenes = scenes
        self.default_scene_index = default_scene_index
        self.extras = extras
        self.ancillaries = ancillaries or {}

        self._gltf_dict = None
        self._node_key_index_dict = {}
        self._buffer = b''  # should i make a buffer class? and this could be a list of those...

        self.export()

    def export(self):
        self.validate_scenes()  # or should this be wrapped up in the creation of the dict?
        self._gltf_dict = self.get_generic_gltf_dict()
        self.append_scenes()
        if self.ancillaries.get('cameras') and self.is_jsonable(self.ancillaries['cameras'], 'cameras list'):
            for index, camera in enumerate(self.ancillaries['cameras']):
                if not camera.get('type'):
                    raise Exception('Invalid camera at index {}.  Expecting "type" attribute.'.format(index))
            self._gltf_dict['cameras'] = self.ancillaries['cameras']  # trim unused cameras?, but then would have to reindex...
        if self.ancillaries.get('materials') and self.is_jsonable(self.ancillaries['materials'], 'materials list'):
            self._gltf_dict['materials'] = self.ancillaries['materials']
        if self.ancillaries.get('skins') and self.is_jsonable(self.ancillaries['skins'], 'skins list'):
            for index, skin in enumerate(self.ancillaries['skins']):
                if not skin.get('joints'):
                    raise Exception('Invalid skin at index {}.  Expecting "joints" attribute.'.format(index))
                skin['joints'] = [
                    self._node_key_index_dict.get(item)
                    for item in skin['joints']
                    if self._node_key_index_dict.get(item)
                ]  # this smells buggy.
                # gots to write some data here
            self._gltf_dict['skins'] = self.ancillaries['skins']  # beware the bufferView index, must be changed

        with open(self.filepath, 'w') as f:
            json.dump(self._gltf_dict, f)

    def is_jsonable(self, obj, obj_name):
        try:
            json.dumps(obj)
        except (TypeError, OverflowError):
            raise Exception('The {} is not a valid JSON object.'.format(obj_name))
        return True

    def validate_scenes(self):
        # i think much of this validation should actually be happening as the object is created and manipulated
        if self.default_scene_index is not None and not (
            isinstance(self.default_scene_index, int) and 0 <= self.default_scene_index < len(self.scenes)
        ):
            raise Exception('Invalid default scene index.')

        node_keys = set()

        for index, scene in enumerate(self.scenes):
            nodes = scene.nodes
            if not nodes.get(DEFAULT_ROOT_NAME):
                raise Exception('Cannot find root node for scene at index {}.'.format(index))

            for node_key in nodes.keys():
                if node_key == DEFAULT_ROOT_NAME:
                    continue
                if node_key in node_keys:
                    raise Exception('Node keys (except roots) must be unique across scenes.')
                node_keys.add(node_key)

            visited = {node_key: False for node_key in nodes}
            queue = [DEFAULT_ROOT_NAME]
            while queue:
                cur = queue.pop(0)
                if visited[cur]:
                    raise Exception('Scene at index {} is not a tree.'.format(index))
                visited[cur] = True
                queue.extend(nodes[cur].children)

            for node in nodes:
                # what is it i want to do here?
                # transform, matrix and location are tightly linked and should be checked as one walks through the tree
                pass

    def get_generic_gltf_dict(self):
        asset_dict = {
            'version': '2.0'
        }
        if self.extras is not None:
            asset_dict['extras'] = self.extras
        return {
            'asset': asset_dict
        }

    def append_scenes(self):
        if not self.scenes:
            return
        nodes = []
        scenes = []
        for gltf_scene in self.scenes:
            scene_dict = {}
            if gltf_scene.nodes[DEFAULT_ROOT_NAME].children:
                scene_dict['nodes'] = gltf_scene.children
            if gltf_scene.name:
                scene_dict['name'] = gltf_scene.name
            if gltf_scene.extras:
                scene_dict['extras'] = gltf_scene.extras
            scenes.append(scene_dict)

            descendents = {node_key: node for node_key, node in gltf_scene.nodes.items() if node_key != DEFAULT_ROOT_NAME}
            self._node_key_index_dict.update({node_key: index + len(nodes) for index, node_key in enumerate(descendents)})
            nodes += [None] * len(descendents)

            for node_key, node in descendents.items():
                node_dict = {}
                if node.name:
                    node_dict['name'] = node.name
                if node.children:
                    node_dict['children'] = [self._node_key_index_dict[key] for key in node.children]
                if node.matrix:
                    node_dict['matrix'] = self.matrix_to_col_major_order(node.matrix)
                if node.mesh_data:
                    node_dict['mesh'] = self.process_mesh_data(node.mesh_data)
                if node.camera:
                    node_dict['camera'] = node.camera
                if node.skin:
                    node_dict['skin'] = node.skin
                if node.extras:
                    node_dict['extras'] = node.extras

                nodes[self._node_key_index_dict[node_key]] = node_dict

        self._gltf_dict['scenes'] = scenes
        self._gltf_dict['nodes'] = nodes

    def matrix_to_col_major_order(self, matrix):
        return [matrix[i][j] for j in range(4) for i in range(4)]

    def process_mesh_data(self, mesh_data):
        mesh_dict = {}
        if mesh_data.mesh_name:
            mesh_dict['name'] = mesh_data.mesh_name
        if mesh_data.extras and self.is_jsonable(mesh_data.extras, 'mesh extras object'):
            mesh_dict['extras'] = mesh_data.extras
        mode = self.get_mode(mesh_data.faces)

        attributes = {}
        breaks = {0}
        for attr_data in mesh_data.additional_attributes.values():  # wrong
            def compare_neighbors(i):
                return isinstance(attr_data[i - 1], type(attr_data[i]))

            breaks |= set(filter(compare_neighbors, range(1, len(attr_data))))

        breaks = list(breaks).sort()

        indices = self.get_indices(mesh_data.faces)
        primitives = [self.get_primitive_dict(attributes, indices, mode)]
        mesh_dict['primitives'] = primitives

        self._gltf_dict.setdefault('meshes', []).append(mesh_dict)
        return len(self._gltf_dict['meshes']) - 1

    def get_indices(self, faces):
        data = [(item,) for item in itertools.chain(*faces)]
        accessor_index = self.get_accessor(data, COMPONENT_TYPE_UNSIGNED_INT, TYPE_SCALAR)
        return accessor_index

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
        size += (4 - size % 4) % 4  # ensure the bytes_ length is divisible by 4,  is this right, or should it be ==0%12 when vec3(float)?

        bytes_ = bytearray(size)

        for i, datum in enumerate(data):
            struct.pack_into(fmt, bytes_, i * component_len, *datum)

        buffer_view_index = self.get_buffer_view(bytes_)
        accessor_dict = {
            'bufferView': buffer_view_index,
            'count': count,
            'componentType': component_type,
            'type': type_,
        }
        if include_bounds:
            minimum = tuple(map(min, zip(*data)))
            maximum = tuple(map(min, zip(*data)))
            accessor_dict['min'] = minimum
            accessor_dict['max'] = maximum

        self._gltf_dict.setdefault('accessors', []).append(accessor_dict)

        return len(self._gltf_dict['accessors']) - 1

    def get_buffer_view(self, bytes_):
        byte_offset = self.update_buffer(bytes_)
        buffer_view_dict = {
            'buffer': 0,
            'bufferLength': len(bytes_),
            'byteOffset': byte_offset,
        }

        self._gltf_dict.setdefault('bufferViews', []).append(buffer_view_dict)

        return len(self._gltf_dict['bufferViews']) - 1

    def update_buffer(self, bytes_):
        if not self._gltf_dict.get('buffers'):
            buffer = {
                'uri': self.bin_filepath,
                'byteLength': 0
            }
            buffers = [buffer]
            self._gltf_dict['buffers'] = buffers
        byte_offset = self._gltf_dict['buffers'][0]['byteLength']  # len(self._buffer) ? what is more compatible with glb creation?
        self._gltf_dict['buffers'][0]['byteLength'] += len(bytes_)
        self._buffer += bytes_
        return byte_offset

    def get_bin_filepath(self):
        base = os.path.splitext(self.filepath)[0]
        return base + '.bin'

    def get_mode(self, faces):
        vertex_count = len(faces[0])
        if vertex_count in MODE_BY_VERTEX_COUNT:
            return MODE_BY_VERTEX_COUNT[vertex_count]
        raise Exception('Meshes must be composed of triangles, lines or points.')

    def get_primitive_dict(self, attributes, indices, mode):
        primitive_dict = {
            'attributes': attributes,
            'indices': indices,
        }
        if mode:
            primitive_dict['mode'] = mode
        return primitive_dict


class GLTFReader(object):
    """"Read the contents of a *glTF* or *glb* version 2 file using the json library.
    Uses ideas from Khronos Group glTF-Blender-IO.
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
        self.image_data = []  # image-image_data having corresponding indices, will have to amend indices
        self.skin_data = []  # same

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
                image_data = self.get_attr_data(image, 'bufferView')
                self.image_data.append(image_data)

            for skin in self.json.get('skins', []):
                skin_data = self.get_attr_data(skin, 'inverseBindMatrices')
                self.skin_data.append(skin_data)

        self.release_buffers()

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
            gltf_node.matrix = self.get_matrix(node)
            gltf_node.weights = node.get('weights')
            gltf_node.mesh_index = node.get('mesh')
            gltf_node.camera = node.get('camera')
            gltf_node.skin = node.get('skin')
            gltf_node.extras = node.get('extras')

            gltf_node.transform = multiply_matrices(scene_obj.nodes[parent_key].transform, gltf_node.matrix)
            gltf_node.position = self.inhomogeneous_transformation(gltf_node.transform, scene_obj.nodes[DEFAULT_ROOT_NAME].position)
            gltf_node.node_key = key

            if gltf_node.mesh_index is not None:
                gltf_node.mesh_data = self.get_mesh_data(gltf_node)

            scene_obj.nodes[key] = gltf_node

            self.process_children(key, scene_obj)

    def get_matrix(self, node):
        if 'matrix' in node:
            return self.get_matrix_from_col_major_list(node['matrix'])
        return self.get_matrix_from_trs(node)

    def get_matrix_from_col_major_list(self, matrix_as_list):
        return [[matrix_as_list[i + j * 4] for j in range(4)] for i in range(4)]

    def get_matrix_from_trs(self, node):
        matrix = identity_matrix(4)
        if 'translation' in node:
            translation = matrix_from_translation(node['translation'])
            matrix = multiply_matrices(matrix, translation)
        if 'rotation' in node:
            rotation = matrix_from_quaternion(node['rotation'])
            matrix = multiply_matrices(matrix, rotation)
        if 'scale' in node:
            scale = matrix_from_scale_factors(node['scale'])
            matrix = multiply_matrices(matrix, scale)
        return matrix

    def inhomogeneous_transformation(self, matrix, vector):
        return self.project_vector(multiply_matrices([self.embed_vector(vector)], transpose_matrix(matrix))[0])

    def embed_vector(self, vector):
        return vector + [1.0]

    def project_vector(self, vector):
        return vector[:3]

    def get_mesh_data(self, gltf_node):
        vertex_data = []
        faces = []
        mesh = self.reader.json['meshes'][gltf_node.mesh_index]
        mesh_name = mesh.get('name')
        extras = mesh.get('extras')
        primitives = mesh['primitives']
        shift = 0
        weights = self.get_weights(mesh, gltf_node)
        for primitive_index, primitive in enumerate(primitives):
            if 'POSITION' not in primitive['attributes']:
                continue

            attributes = defaultdict(list)
            face_side_count = self.get_face_side_count(primitive)

            for attr, attr_accessor_index in primitive['attributes'].items():
                primitive_attr = self.reader.data[attr_accessor_index]
                if weights and primitive.get('targets') and attr in primitive['targets'][0]:
                    targets = primitive['targets']
                    target_data = [self.reader.data[target[attr]] for target in targets]

                    apply_morph_targets = self.get_morph_function(weights)

                    primitive_attr = list(map(apply_morph_targets, primitive_attr, *target_data))

                attributes[attr] += primitive_attr

            indices = self.get_indices(primitive, len(attributes['POSITION']))
            shifted_indices = self.shift_indices(indices, shift)
            primitive_faces = self.group_indices(shifted_indices, face_side_count)
            faces.extend(primitive_faces)

            shift += len(attributes['POSITION'])
            for data in attributes.values():
                if len(data) != shift:
                    data += [None] * (shift - len(data))

            for i in range(len(attributes['POSITION'])):
                vertex = {'PRIMITIVE': primitive_index}
                for attr, data in attributes.items():
                    vertex[attr] = data[i]
                vertex_data.append(vertex)
        return MeshData(faces, vertex_data, mesh_name, extras)

    def get_weights(self, mesh, gltf_node):
        weights = mesh.get('weights', None)
        weights = gltf_node.weights or weights
        return weights

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
            # revisit this, necessary because morph targets can apply to normal vectors which are 4d, but you shouldn't mess with the w component

        return apply_morph_target

    def get_face_side_count(self, primitive):
        if 'mode' not in primitive or primitive['mode'] == 4:
            return 3
        if primitive['mode'] == 1:
            return 2
        if primitive['mode'] == 0:
            return 1
        raise NotImplementedError

    def get_indices(self, primitive, num_vertices):
        if 'indices' not in primitive:
            return self.get_generic_indices(num_vertices)
        indices_accessor_index = primitive['indices']
        return self.reader.data[indices_accessor_index]

    def get_generic_indices(self, num_vertices):
        return list(range(num_vertices))

    def shift_indices(self, indices, shift):
        return [index + shift for index in indices]

    def group_indices(self, indices, group_size):
        it = [iter(indices)] * group_size
        return list(zip(*it))


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

    source_glb = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/GearboxAssy/glTF/GearboxAssy.gltf'
    filepath_glb = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'GearboxAssy.gltf')

    # source_glb = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/SimpleMorph/glTF-Embedded/SimpleMorph.gltf'
    # filepath_glb = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'SimpleMorph.gltf')

    download_file_from_remote(source_glb, filepath_glb, overwrite=False)

    gltf = GLTF(filepath_glb)

    default_scene_index = gltf.parser.default_scene_index or 0
    nodes = gltf.parser.scenes[default_scene_index].nodes

    vrts = {name: gltf_node.position for name, gltf_node in nodes.items()}
    edges = [
        (node.node_key, child)
        for node in gltf.parser.scenes[default_scene_index].nodes.values()
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
