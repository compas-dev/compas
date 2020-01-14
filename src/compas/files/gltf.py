from __future__ import print_function
from __future__ import absolute_import


__all__ = [
    'GLTF',
    'GLTFReader',
    'GLTFParser',
]

import base64
import io
import json
import os
import struct
from math import fsum

from compas.geometry import identity_matrix
from compas.geometry import matrix_from_quaternion
from compas.geometry import matrix_from_scale_factors
from compas.geometry import matrix_from_translation
from compas.geometry import multiply_matrices
from compas.geometry import transpose_matrix

COMPONENT_TYPE_ENUM = {
    5120: 'b',  # BYTE
    5121: 'B',  # UNSIGNED_BYTE
    5122: 'h',  # SHORT
    5123: 'H',  # UNSIGNED_SHORT
    5125: 'I',  # UNSIGNED_INT
    5126: 'f',  # FLOAT
}

NUM_COMPONENTS_BY_TYPE_ENUM = {
    "SCALAR": 1,
    "VEC2": 2,
    "VEC3": 3,
    "VEC4": 4,
    "MAT2": 4,
    "MAT3": 9,
    "MAT4": 16,
}

DEFAULT_ROOT_NAME = 'root'


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
    """
    def __init__(self, faces, vertices, mesh_name):
        self.vertices = vertices
        self.faces = faces
        self.mesh_name = mesh_name
        # self.material = ??


class GLTFScene(object):
    """Object representing a root node of a scene.

    Attributes
    ----------
    name : str
        Name of the scene, if any.
    edges : list
        List of 2-tuples referencing nodes by key.
    nodes : dict
        Dictionary of (node_key, GLTFNode) pairs.
    """
    def __init__(self):
        self.name = None
        self.edges = []
        self.nodes = {}


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
    mesh_index : int or str double check this
        Index of the associated mesh within the JSON.
    weights : list of ints
        Weights used for computing morph targets in the attached mesh, if any.

    position : tuple
        xyz-coordinates of the node, calculated from the matrix.
    transform : list of lists
        Matrix representing the displacement from the root node to the node.
    mesh_data : MeshData
        Contains mesh data, if any.
    node_key : int
        Key of the node used in GLTFScene.nodes.
    """
    def __init__(self):
        self.name = None
        self.children = []
        self.matrix = None
        self.mesh_index = None
        self.weights = None

        self.position = None
        self.transform = None
        self.mesh_data = None
        self.node_key = None


class GLTF(object):
    """Read files in glTF format.

    See Also
    --------
    * https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/figures/gltfOverview-2.0.0b.png

    """
    def __init__(self, filepath):
        self.filepath = filepath

        self._is_parsed = False
        self._reader = None
        self._parser = None

    def read(self):
        self._reader = GLTFReader(self.filepath)
        self._parser = GLTFParser(self._reader)
        self._is_parsed = True

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


class GLTFReader(object):
    """"Read the contents of a *glTF* or *glb* version 2 file using the json library.
    Uses ideas from Khrono's Group glTF-Blender-IO.
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
            self._content = None
            self.json = json.loads(content)

        else:
            self.load_from_glb()
            self._content = None

        self.check_version()

        if self.json:
            for accessor in self.json.get('accessors', []):
                accessor_data = self.access_data(accessor)
                self.data.append(accessor_data)

            for image in self.json.get('images', []):
                image_data = self.get_image_data(image)
                self.image_data.append(image_data)

    def get_image_data(self, image):
        if 'bufferView' not in image:
            return None
        buffer_view_index = image['bufferView']
        buffer_view = self.json['buffersViews'][buffer_view_index]
        buffer = self.get_buffer(buffer_view['buffer'])
        offset = buffer_view.get('byteOffset', 0)
        length_ = buffer_view['byteLength']
        return buffer[offset: offset + length_]

    def load_from_glb(self):
        header = struct.unpack_from('<4sII', self._content)
        file_size = header[2]

        if file_size != len(self._content):
            raise Exception('Bad glTF.  File size does not match.')

        offset = 12

        # load json
        type_, length_, json_bytes, offset = self.load_chunk(offset)
        if type_ != b'JSON':
            raise Exception('Bad glTF.  First chunk not in JSON format')
        json_str = json_bytes.tobytes().decode('utf-8')
        self.json = json.loads(json_str)

        # load binary buffer
        if offset < len(self._content):
            type_, length_, bytes_, offset = self.load_chunk(offset)
            if type_ == b'BIN\0':
                self._glb_buffer = bytes_

    def load_chunk(self, offset):
        chunk_header = struct.unpack_from('<I4s', self._content, offset)
        length_ = chunk_header[0]
        type_ = chunk_header[1]
        data = self._content[offset + 8: offset + 8 + length_]

        return type_, length_, data, offset + 8 + length_

    def check_version(self):
        version = self.json['asset']['version']
        if float(version) != 2.0:
            raise Exception('Invalid glTF version.  Version 2.0 expected.')

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
                        if component_type == 5120:
                            new_tuple += (max(float(i / 127.0), -1.0),)
                        elif component_type == 5121:
                            new_tuple += (float(i / 255.0),)
                        elif component_type == 5122:
                            new_tuple += (max(float(i / 32767.0), -1.0),)
                        elif component_type == 5123:
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
            unpack_from(buffer, i)
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
    and create objects digestible by compas.

    Parameters
    ----------
    reader : GLTFReader

    Attributes
    ----------
    reader : GLTF2Reader
    default_scene_index : int
        index of the default scene
    scenes : list of GLTFScenes
        List of dictionaries containing the information of each scene.
    """
    def __init__(self, reader):
        self.reader = reader
        self.default_scene_index = None
        self.scenes = []

        self.parse()

    def parse(self):
        self.default_scene_index = self.get_default_scene()

        for scene in self.reader.json.get('scenes', []):
            scene_obj = self.get_initial_scene(scene)
            self.process_children('root', scene_obj)
            self.scenes.append(scene_obj)

    def get_default_scene(self):
        return self.reader.json.get('scene')

    def get_initial_scene(self, scene):
        scene_obj = GLTFScene()
        scene_obj.name = scene.get('name')

        root_node = self.get_default_root_node(scene)
        scene_obj.nodes[root_node.name] = root_node

        return scene_obj

    def get_default_root_node(self, scene):
        root_node = GLTFNode()

        root_node.name = DEFAULT_ROOT_NAME
        root_node.position = [0, 0, 0]
        root_node.transform = identity_matrix(4)
        root_node.matrix = identity_matrix(4)
        root_node.children = scene.get('nodes', [])

        return root_node

    def process_children(self, parent_key, scene_obj):
        child_keys = scene_obj.nodes[parent_key].children
        for key in child_keys:
            scene_obj.edges.append((parent_key, key))

            gltf_node = GLTFNode()

            node = self.reader.json['nodes'][key]

            gltf_node.name = node.get('name')
            gltf_node.children = node.get('children', [])
            gltf_node.matrix = self.get_matrix(node)
            gltf_node.weights = node.get('weights')
            gltf_node.mesh_index = node.get('mesh')

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
        faces = []
        vertices = []
        mesh = self.reader.json['meshes'][gltf_node.mesh_index]
        mesh_name = mesh.get('name')
        primitives = mesh['primitives']
        shift = 0
        weights = self.get_weights(mesh, gltf_node)
        for primitive in primitives:

            face_side_count = self.get_face_side_count(primitive)

            if 'POSITION' not in primitive['attributes']:
                continue
            position_accessor_index = primitive['attributes']['POSITION']
            primitive_vertices = self.reader.data[position_accessor_index]
            if weights and 'targets' in primitive and primitive['targets'] and 'POSITION' in primitive['targets'][0]:
                targets = primitive['targets']
                target_data = [self.reader.data[target['POSITION']] for target in targets]

                apply_morph_targets = self.get_morph_function(weights)

                primitive_vertices = list(map(apply_morph_targets, primitive_vertices, *target_data))

            vertices.extend(primitive_vertices)

            indices = self.get_indices(primitive, len(primitive_vertices))
            shifted_indices = self.shift_indices(indices, shift)
            primitive_faces = self.group_indices(shifted_indices, face_side_count)
            faces.extend(primitive_faces)

            shift += len(primitive_vertices)
        return MeshData(faces, vertices, mesh_name)

    def get_weights(self, mesh, gltf_node):
        weights = mesh.get('weights', None)
        weights = gltf_node.weights or weights
        return weights

    def get_morph_function(self, w):
        # Returns a function which computes for a fixed list w of scalar weights the linear combination
        #                               vertex + sum_i(w[i] * targets[i])
        # where vertex and targets[i] are vectors.
        def apply_morph_target(vertex, *targets):
            return tuple(map(lambda v, *t: v + fsum(map(lambda a, b: a * b, w, t)), vertex, *targets))
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

    source_glb = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/BoxInterleaved/glTF-Binary/BoxInterleaved.glb'
    filepath_glb = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'BoxInterleaved.glb')

    download_file_from_remote(source_glb, filepath_glb, overwrite=False)
    
    gltf = GLTF(filepath_glb)

    default_scene_index = gltf.parser.default_scene_index or 0
    vertex_data = gltf.parser.scenes[default_scene_index].nodes

    vertices = {name: gltf_node.position for name, gltf_node in vertex_data.items()}
    edges = gltf.parser.scenes[default_scene_index].edges

    scene_tree = Network.from_vertices_and_edges(vertices, edges)
    scene_tree.plot()

    transformed_meshes = []

    for vertex_name, gltf_node in vertex_data.items():
        if gltf_node.mesh_data is None:
            continue
        t = gltf_node.transform
        m = Mesh.from_vertices_and_faces(gltf_node.mesh_data.vertices, gltf_node.mesh_data.faces)
        transformed_mesh = mesh_transformed(m, t)
        transformed_meshes.append(transformed_mesh)

    viewer = MultiMeshViewer()
    viewer.meshes = transformed_meshes
    viewer.show()
