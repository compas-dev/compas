from __future__ import print_function
from __future__ import absolute_import


__all__ = [
    'GLTF2',
    'GLTF2Reader',
    'GLTF2Parser',
]

import base64
import io
import json
import os
import struct

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


class GLTF2(object):
    """Read and write files in glTF format.

    See Also
    --------
    * https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/figures/gltfOverview-2.0.0b.png

    """
    def __init__(self, filepath):
        self.reader = GLTF2Reader(filepath)
        self.parser = GLTF2Parser(self.reader)


class GLTF2Reader(object):
    """"Read the contents of a *glTF* file using the json library.

    Parameters
    ----------
    filepath: str
        Path to the file.

    Attributes
    ----------
    filepath : str
        String containing the path to the glTF
    json : dict
        Dictionary object containing the contents of the glTF
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.json = None
        self.read()

    def read(self):
        if self.filepath:
            with open(self.filepath, 'r') as f:
                self.json = json.load(f)


class GLTF2Parser(object):
    """Parse the contents of the reader to read and parse the associated binary files to create objects digestible by compas.

    Parameters
    ----------
    reader : GLTFReader

    Attributes
    ----------
    reader : GLTF2Reader
    faces_and_vertices : list
        List of dictionaries containing vertex and face lists.
    root : str
        Name of the root vertex of the default scene.
    vertices : dict
        Dictionary of vertex name-xyz coordinate pairs.
    vertex_data : dict
        Dictionary with vertex names as keys and values of dictionaries of the form:
            {
                'transform': <matrix representing the transformation from the origin to the vertex>
                'matrix' : <matrix representing the transformation from the parent to the vertex>
                'mesh_key' : <index of the mesh at this vertex, if any>
                'mesh_name' : <name of the mesh, if any>
            }
    edges : list
        List of tupled pairs of vertices representing edges.
    """
    def __init__(self, reader):
        self.reader = reader
        self.faces_and_vertices = []
        self.root = 'world'
        self.vertices = {self.root: [0, 0, 0]}  # this contains much redundant information, so that a reasonable thing?
        self.vertex_data = {self.root: {
            'transform': identity_matrix(4),
            'matrix': identity_matrix(4),
        }}
        self.edges = []
        self.parse()

    def parse(self):
        self.extract_tree_data()

        meshes = self.reader.json['meshes']
        self.faces_and_vertices = [self.get_faces_and_vertices(mesh) for mesh in meshes]

    def extract_tree_data(self):
        default_scene_index = self.reader.json['scene']  # consider handling other scenes...
        root_children = self.reader.json['scenes'][default_scene_index]['nodes']

        self.process_children(self.root, root_children)

        nodes = self.reader.json['nodes']
        for node_key, node in enumerate(nodes):
            if 'children' in node:
                child_indices = node['children']
                self.process_children(node_key, child_indices)

    def process_children(self, parent_key, child_keys):
        for child_key in child_keys:
            self.edges.append((parent_key, child_key))

            data = self.get_vertex_data(child_key, parent_key)
            self.vertex_data[child_key] = data

            transform = data['transform']
            child_coord = self.inhomogeneous_transformation(transform, self.vertices[self.root])
            self.vertices[child_key] = child_coord

    def get_vertex_data(self, vertex_key, parent_key):
        node = self.reader.json['nodes'][vertex_key]
        matrix = self.get_matrix(node)
        transform = multiply_matrices(self.vertex_data[parent_key]['transform'], matrix)
        mesh_data = self.get_mesh_data(node)

        data = {'matrix': matrix, 'transform': transform}
        data.update(mesh_data)
        return data

    def get_matrix(self, node):
        if 'matrix' in node:
            matrix = self.get_matrix_from_col_major_list(node['matrix'])
        else:
            matrix = self.get_matrix_from_trs(node)
        return matrix

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

    def get_mesh_data(self, node):
        mesh_data = {}
        if 'mesh' in node:
            mesh_key = node['mesh']
            mesh_data['mesh_key'] = mesh_key

            mesh = self.reader.json['meshes'][mesh_key]
            if 'name' in mesh:
                mesh_data['mesh_name'] = mesh['name']
        return mesh_data

    def inhomogeneous_transformation(self, matrix, vector):
        return self.project_vector(multiply_matrices([self.embed_vector(vector)], transpose_matrix(matrix))[0])

    def embed_vector(self, vector):
        return vector + [1.0]

    def project_vector(self, vector):
        return vector[:3]

    def get_faces_and_vertices(self, mesh):
        vertices = []
        faces = []
        primitives = mesh['primitives']
        shift = 0
        for primitive in primitives:
            face_side_count = self.get_face_side_count(primitive)

            if 'attributes' not in primitive or 'POSITION' not in primitive['attributes']:
                continue
            position_accessor_index = primitive['attributes']['POSITION']
            primitive_vertices = self.access_data(position_accessor_index)
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
            indices = self.get_generic_indices(num_vertices)
        else:
            indices_accessor_index = primitive['indices']
            wrapped_indices = self.access_data(indices_accessor_index)
            indices = [item[0] for item in wrapped_indices]
        return indices

    def get_generic_indices(self, num_vertices):
        return list(range(num_vertices))

    def shift_indices(self, indices, shift):
        return [index + shift for index in indices]

    def group_indices(self, indices, group_size):
        it = [iter(indices)] * group_size
        return list(zip(*it))

    def access_data(self, accessor_index):
        data = []

        accessor = self.reader.json['accessors'][accessor_index]

        if 'sparse' in accessor:
            raise NotImplementedError

        buffer_view_index = accessor['bufferView']
        buffer_view = self.reader.json['bufferViews'][buffer_view_index]

        offset = accessor['byteOffset'] + buffer_view['byteOffset']
        count = accessor['count']
        component_type = accessor['componentType']
        type_ = accessor['type']

        try:
            num_components = NUM_COMPONENTS_BY_TYPE_ENUM[type_]
        except KeyError:
            raise NotImplementedError

        expected_length = COMPONENT_TYPE_SIZE_ENUM[component_type] * num_components
        byte_stride = buffer_view['byteStride'] if 'byteStride' in buffer_view else expected_length
        pad_length = byte_stride - expected_length

        format_ = '<' + COMPONENT_TYPE_ENUM[component_type] * num_components + 'x' * pad_length

        uri = self.get_uri(buffer_view)
        f = self.get_byte_stream(uri)

        f.seek(offset)
        for _ in range(count):
            bytes_ = f.read(byte_stride)
            unpacked = struct.unpack(format_, bytes_)
            data.append(unpacked)
        f.close()

        return data

    def get_uri(self, buffer_view):
        buffer_index = buffer_view['buffer']
        return self.reader.json['buffers'][buffer_index]['uri']

    def get_byte_stream(self, uri):
        if self.is_data_uri(uri):
            string = self.get_data_uri_data(uri)
            f = base64.b64decode(string)
            f = io.BytesIO(f)
        else:
            filepath = self.get_filepath(uri)
            f = open(filepath, 'rb')
        return f

    def is_data_uri(self, uri):
        split_uri = uri.split(':')
        return split_uri[0] == 'data'

    def get_data_uri_data(self, uri):
        split_uri = uri.split(',')
        return split_uri[-1]

    def get_filepath(self, uri):
        dir_path = os.path.dirname(self.reader.filepath)
        return os.path.join(dir_path, uri)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas

    from compas.datastructures import Mesh, Network, mesh_transformed
    from compas.utilities import download_file_from_remote
    from compas_viewers.multimeshviewer import MultiMeshViewer

    source_gltf = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/GearboxAssy/glTF/GearboxAssy.gltf'
    source_bin = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/GearboxAssy/glTF/GearboxAssy0.bin'
    filepath_gltf = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'GearboxAssy.gltf')
    filepath_bin = os.path.join(compas.APPDATA, 'data', 'gltfs', 'khronos', 'GearboxAssy0.bin')

    download_file_from_remote(source_gltf, filepath_gltf, overwrite=False)
    download_file_from_remote(source_bin, filepath_bin, overwrite=False)

    gltf = GLTF2(filepath_gltf)

    print('break')

    scene_tree = Network.from_vertices_and_edges(
        gltf.parser.vertices,
        gltf.parser.edges
    )
    scene_tree.plot()

    vertex_data = gltf.parser.vertex_data

    meshes = [
        Mesh.from_vertices_and_faces(data['vertices'], data['faces'])
        for data in gltf.parser.faces_and_vertices
    ]

    transformed_meshes = []

    for vertex_name, attributes in vertex_data.items():
        if 'mesh_key' not in attributes:
            continue
        mk = attributes['mesh_key']
        t = attributes['transform']
        m = meshes[mk]
        transformed_mesh = mesh_transformed(m, t)
        transformed_meshes.append(transformed_mesh)

    viewer = MultiMeshViewer()
    viewer.meshes = transformed_meshes
    viewer.show()
