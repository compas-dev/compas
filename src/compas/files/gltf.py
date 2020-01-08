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

COMPONENT_TYPE_SIZE_ENUM = {
    5120: 1,  # BYTE
    5121: 1,  # UNSIGNED_BYTE
    5122: 2,  # SHORT
    5123: 2,  # UNSIGNED_SHORT
    5125: 4,  # UNSIGNED_INT
    5126: 4,  # FLOAT
}

NUM_COMPONENTS_BY_TYPE_ENUM = {
    "SCALAR": 1,
    # "VEC2": 2,
    "VEC3": 3,
    # "VEC4": 4,
    # "MAT2": 4,
    # "MAT3": 9,
    # "MAT4": 16,
}


class GLTF(object):
    """Read files in glTF format.

    See Also
    --------
    * https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/figures/gltfOverview-2.0.0b.png

    """
    def __init__(self, filepath):
        self.reader = GLTFReader(filepath)
        self.parser = GLTFParser(self.reader)


class GLTFReader(object):
    """"Read the contents of a *glTF* or *glb* version 2 file using the json library .

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
        Note: Only scalar and 3 dimensional vector data are supported.
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.json = None
        self.data = []
        self.read()

    def read(self):
        if self.filepath:
            ext = self.get_file_extension()
            if ext == '.gltf':
                self.load_json_from_gltf()
            if ext == '.glb':
                self.load_json_from_glb()

        if self.json:
            for accessor in self.json.get('accessors', []):
                accessor_data = self.access_data(accessor)
                self.data.append(accessor_data)

    def get_file_extension(self):
        _, ext = os.path.splitext(self.filepath)
        if ext not in ['.gltf', '.glb']:
            raise Exception('Invalid  file extension.  glTF or glb expected.')
        return ext

    def load_json_from_gltf(self):
        with open(self.filepath, 'r') as f:
            self.json = json.load(f)
            version = self.json['asset']['version']
            self.check_version(version)

    def load_json_from_glb(self):
        with open(self.filepath, 'rb') as f:
            self.check_magic_number(f)
            version = self.read_byte(f, 4)
            self.check_version(version)
            self.check_chunk_type(f)

            chunk_length = self.read_byte(f, 12)
            f.seek(20)
            bytes_ = f.read(chunk_length)
            self.json = json.loads(bytes_)

    def check_version(self, version):
        if float(version) != 2.0:
            raise Exception('Invalid glTF version.  Version 2.0 expected.')

    def check_magic_number(self, f):
        magic = self.read_byte(f, 0)
        if magic != 0x46546C67:
            raise Exception('Invalid file type.')

    def check_chunk_type(self, f):
        chunk_type = self.read_byte(f, 16)
        if chunk_type != 0x4E4F534A:
            raise NotImplementedError

    def read_byte(self, f, origin, type_='I'):
        f.seek(origin)
        return struct.unpack(type_, f.read(4))[0]

    def access_data(self, accessor):
        count = accessor['count']
        component_type = accessor['componentType']
        type_ = accessor['type']
        accessor_offset = accessor.get('byteOffset', 0)

        try:
            num_components = NUM_COMPONENTS_BY_TYPE_ENUM[type_]
        except KeyError:
            return None

        if 'sparse' not in accessor and 'bufferView' not in accessor:
            raise Exception('Extensions are not supported.')

        data = self.get_generic_data(num_components, count)

        if 'bufferView' in accessor:
            buffer_view_index = accessor['bufferView']
            data = self.read_from_buffer_view(
                buffer_view_index,
                count,
                component_type,
                accessor_offset,
                num_components
            )

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

        return data

    def get_generic_data(self, num_components, count):
        return [(0, ) * num_components for _ in range(count)]

    def read_from_buffer_view(self, buffer_view_index, count, component_type, accessor_offset, num_components):
        data = []
        buffer_view = self.json['bufferViews'][buffer_view_index]
        buffer_view_offset = buffer_view.get('byteOffset', 0)

        offset = accessor_offset + buffer_view_offset

        expected_length = COMPONENT_TYPE_SIZE_ENUM[component_type] * num_components
        byte_stride = buffer_view.get('byteStride', expected_length)
        pad_length = byte_stride - expected_length

        format_ = '<' + COMPONENT_TYPE_ENUM[component_type] * num_components + 'x' * pad_length

        uri = self.get_uri(buffer_view)
        f = self.get_byte_stream(uri)

        f.seek(offset, 1)
        for _ in range(count):
            bytes_ = f.read(byte_stride)
            unpacked = struct.unpack(format_, bytes_)
            data.append(unpacked)
        f.close()

        if num_components == 1:
            data = [item[0] for item in data]  # unwrap integers from tuple

        return data

    def get_uri(self, buffer_view):
        buffer_index = buffer_view['buffer']
        return self.json['buffers'][buffer_index].get('uri', None)

    def get_byte_stream(self, uri):
        if not uri:
            f = open(self.filepath, 'rb')
            chunk_0_len = self.read_byte(f, 12)
            f.seek(12 + 8 + chunk_0_len + 8)  # header + chunk 0 header + chunk 0 + chunk 1 header
        elif self.is_data_uri(uri):
            string = self.get_data_uri_data(uri)
            f = base64.b64decode(string)
            f = io.BytesIO(f)
            f.seek(0)
        else:
            filepath = self.get_filepath(uri)
            f = open(filepath, 'rb')
            f.seek(0)
        return f

    def is_data_uri(self, uri):
        split_uri = uri.split(':')
        return split_uri[0] == 'data'

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
    default_scene : int
        index of the default scene
    scenes : list
        List of dictionaries containing the information of each scene.
        Dictionaries are of the following form:

        name : str
            Name of the scene.
        extras : dict
            Extra information about the scene.
        faces_and_vertices : dict
            Dictionary of dictionaries containing vertex and face lists.
        vertices : dict
            Dictionary with vertex names as keys and values of the form:
                {
                    'position' : <xyz coordinates>
                    'transform': <matrix representing the transformation from the origin to the vertex>
                    'matrix' : <matrix representing the transformation from the parent to the vertex>
                    'mesh_key' : <index of the mesh at this vertex, if any>
                    'mesh_name' : <name of the mesh, if any>
                    'extras' : <extra data associated to the node, if any>
                }
        edges : list
            List of tupled pairs of vertices representing edges.
    """
    def __init__(self, reader):
        self.reader = reader
        self.scenes = []
        self.default_scene = None
        self.parse()

    def parse(self):
        self.default_scene = self.get_default_scene()

        for scene in self.reader.json.get('scenes', []):
            scene_dict = self.get_initial_scene_dict(scene)
            root_children = scene.get('nodes', [])
            self.process_children('root', root_children, scene_dict)
            self.scenes.append(scene_dict)

    def get_default_scene(self):
        return self.reader.json.get('scene', None)

    def get_initial_scene_dict(self, scene):
        return {
            'name': scene.get('name', ''),
            'extras': scene.get('extras', {}),
            'faces_and_vertices': {},
            'vertices': {'root': {
                'position': [0, 0, 0],
                'transform': identity_matrix(4),
                'matrix': identity_matrix(4),
            }},
            'edges': [],
        }

    def process_children(self, parent_key, child_keys, scene_dict):
        for key in child_keys:
            scene_dict['edges'].append((parent_key, key))

            data = self.get_vertex_data(key, parent_key, scene_dict)

            transform = data['transform']
            position = self.inhomogeneous_transformation(transform, scene_dict['vertices']['root']['position'])
            data['position'] = position

            scene_dict['vertices'][key] = data

            descendents = self.reader.json['nodes'][key].get('children', [])
            self.process_children(key, descendents, scene_dict)

    def get_vertex_data(self, vertex_key, parent_key, scene_dict):
        node = self.reader.json['nodes'][vertex_key]
        matrix = self.get_matrix(node)
        transform = multiply_matrices(scene_dict['vertices'][parent_key]['transform'], matrix)
        mesh_data = self.get_mesh_data(node, scene_dict)
        extras = node.get('extras', {})

        data = {'matrix': matrix, 'transform': transform}
        data.update(mesh_data)
        data['extras'] = extras
        return data

    def get_matrix(self, node):
        if 'matrix' in node:
            return self.get_matrix_from_col_major_list(node['matrix'])
        return self.get_matrix_from_trs(node)

    def get_matrix_from_col_major_list(self, matrix_as_list):
        return [[matrix_as_list[i + j * 4] for j in range(4)] for i in range(4)]

    def get_matrix_from_trs(self, child_node):
        matrix = identity_matrix(4)
        if 'translation' in child_node:
            translation = matrix_from_translation(child_node['translation'])
            matrix = multiply_matrices(matrix, translation)
        if 'rotation' in child_node:
            rotation = matrix_from_quaternion(child_node['rotation'])
            matrix = multiply_matrices(matrix, rotation)
        if 'scale' in child_node:
            scale = matrix_from_scale_factors(child_node['scale'])
            matrix = multiply_matrices(matrix, scale)
        return matrix

    def get_mesh_data(self, node, scene_dict):
        mesh_data = {}
        if 'mesh' in node:
            mesh_key = node['mesh']
            mesh_data['mesh_key'] = mesh_key
            mesh = self.reader.json['meshes'][mesh_key]
            scene_dict['faces_and_vertices'][mesh_key] = self.get_faces_and_vertices(mesh, node)
            if 'name' in mesh:
                mesh_data['mesh_name'] = mesh['name']
        return mesh_data

    def inhomogeneous_transformation(self, matrix, vector):
        return self.project_vector(multiply_matrices([self.embed_vector(vector)], transpose_matrix(matrix))[0])

    def embed_vector(self, vector):
        return vector + [1.0]

    def project_vector(self, vector):
        return vector[:3]

    def get_faces_and_vertices(self, mesh, node):
        vertices = []
        faces = []
        primitives = mesh['primitives']
        shift = 0
        weights = self.get_weights(mesh, node)
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
        return {
                'vertices': vertices,
                'faces': faces,
            }

    def get_weights(self, mesh, node):
        weights = mesh.get('weights', None)
        weights = node.get('weights', weights)
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

    source_glb = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/GearboxAssy/glTF-Binary/GearboxAssy.glb'
    filepath_glb = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'GearboxAssy.glb')

    download_file_from_remote(source_glb, filepath_glb, overwrite=False)

    gltf = GLTF(filepath_glb)

    default_scene = gltf.parser.default_scene or 0
    vertex_data = gltf.parser.scenes[default_scene]['vertices']

    vertices = {name: data['position'] for name, data in vertex_data.items()}
    edges = gltf.parser.scenes[default_scene]['edges']

    scene_tree = Network.from_vertices_and_edges(vertices, edges)
    scene_tree.plot()

    meshes_by_key = {
        key: Mesh.from_vertices_and_faces(data['vertices'], data['faces'])
        for key, data in gltf.parser.scenes[default_scene]['faces_and_vertices'].items()
    }

    transformed_meshes = []

    for vertex_name, attributes in vertex_data.items():
        if 'mesh_key' not in attributes:
            continue
        mk = attributes['mesh_key']
        t = attributes['transform']
        m = meshes_by_key[mk]
        transformed_mesh = mesh_transformed(m, t)
        transformed_meshes.append(transformed_mesh)

    viewer = MultiMeshViewer()
    viewer.meshes = transformed_meshes
    viewer.show()
