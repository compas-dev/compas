from __future__ import print_function
from __future__ import absolute_import


__all__ = [
    'GLTF',
    'GLTFReader',
    'GLTFParser',
]

import json
from compas.geometry import multiply_matrices, transpose_matrix


class GLTF(object):
    """Read and write files in glTF format.

    See Also
    --------
    * https://github.com/KhronosGroup/glTF/blob/master/specification/2.0/figures/gltfOverview-2.0.0b.png

    """
    def __init__(self, filepath):
        self.reader = GLTFReader(filepath)
        self.parser = GLTFParser(self.reader)


class GLTFReader(object):
    """"Read the contents of a *glTF* file using the trimesh library.

    Parameters
    ----------
    filepath: str
        Path to the file.

    Attributes
    ----------
    scene : trimesh.Scene
        See https://trimsh.org/trimesh.html?highlight=load#trimesh.Scene

    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.scene = None
        self.read()

    def read(self):
        from trimesh import load
        self.scene = load(self.filepath)


class GLTFParser(object):
    """Parse the contents of the reader to objects digestible by compas.

    Parameters
    ----------
    reader : GLTFReader

    Attributes
    ----------
    faces_and_vertices_dict : dict
        Dictionary with mesh names as keys and dictionaries containing vertex and face lists as values.
    root : str
        Name of the root vertex of the scene.
    scene_data : dict
        Dictionary containing vertex and edge (meta)data.
    """
    def __init__(self, reader):
        self.reader = reader
        self.faces_and_vertices_dict = {}
        self.root = None
        self.scene_data = None
        self.parse()

    def parse(self):
        geometries = self.reader.scene.geometry

        for name, trimesh in geometries.items():
            self.faces_and_vertices_dict[name] = {
                'vertices': trimesh.vertices,
                'faces': trimesh.faces,
            }

        self.root = self.reader.scene.graph.base_frame
        edge_list = self.reader.scene.graph.to_edgelist()

        origin = [0, 0, 0]
        identity = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

        vertex_coordinate_data = {self.root: origin}
        vertex_data = {self.root: {'transform': identity}}
        edge_data = []

        while edge_list:
            # i suspect the output of to_edgelist() is a tree search, so this may not be necessary
            parent, child, attributes = edge_list.pop(0)
            if parent not in vertex_data:
                edge_list.append((parent, child, attributes))
                continue

            parent_transform = vertex_data[parent]['transform']
            matrix = attributes['matrix']
            child_transform = multiply_matrices(parent_transform, matrix)

            vertex_coordinate_data[child] = self._inhomogeneous_transformation(child_transform, origin)
            attributes['transform'] = child_transform
            vertex_data[child] = attributes
            edge_data.append((parent, child))

        self.scene_data = {
            'vertex_data': vertex_data,  # {child_name: {'matrix': matrix from parent to child, 'transform': matrix from origin to child, 'geometry': mesh name, 'time': timestamp}}
            'vertices': vertex_coordinate_data,  # {vertex_name: [x, y, z]]}
            'edges': edge_data,  # [(parent_name, child_name])
        }

    def _inhomogeneous_transformation(self, matrix, vector):
        return self._project_vector(multiply_matrices([self._embed_vector(vector)], transpose_matrix(matrix))[0])

    def _embed_vector(self, vector):
        return vector + [1.0]

    def _project_vector(self, vector):
        return vector[:3]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import os
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

    gltf = GLTF(filepath_gltf)

    print('hello')

    scene_tree = Network.from_vertices_and_edges(
        gltf.parser.scene_data['vertices'],
        gltf.parser.scene_data['edges']
    )
    scene_tree.plot()

    vertex_data = gltf.parser.scene_data['vertex_data']

    meshes_by_name = {
        name: Mesh.from_vertices_and_faces(data['vertices'], data['faces'])
        for name, data in gltf.parser.faces_and_vertices_dict.items()
    }
    meshes = []

    for vertex_name, attributes in vertex_data.items():
        if 'geometry' not in attributes:
            continue
        mesh_name = attributes['geometry']
        transform = attributes['transform']
        mesh = meshes_by_name[mesh_name]
        transformed_mesh = mesh_transformed(mesh, transform)
        transformed_mesh.name = mesh_name
        meshes.append(transformed_mesh)

    viewer = MultiMeshViewer()
    viewer.meshes = meshes
    viewer.show()
