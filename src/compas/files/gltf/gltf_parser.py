from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from compas.files.gltf.constants import DEFAULT_ROOT_NAME
from compas.files.gltf.data_classes import MeshData
from compas.files.gltf.data_classes import PrimitiveData
from compas.files.gltf.gltf_node import GLTFNode
from compas.files.gltf.gltf_scene import GLTFScene
from compas.files.gltf.helpers import get_matrix_from_col_major_list
from compas.geometry import multiply_matrices
from compas.geometry import transform_points


class GLTFParser(object):
    """Parse the contents of the reader and create objects digestible by COMPAS.

    Parameters
    ----------
    reader : :class:`GLTFReader`

    Attributes
    ----------
    reader : :class:`GLTFReader`
    default_scene_index : int
        Index of the default scene.
    scenes : list of :class:`compas.files.GLTFScene`
        List of dictionaries containing the information of each scene.
    extras : object
    """
    def __init__(self, reader):
        self.reader = reader
        self.default_scene_index = None
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
            gltf_node.position = transform_points([scene_obj.nodes[DEFAULT_ROOT_NAME].position], gltf_node.transform)[0]
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

        return MeshData(primitive_data_list, mesh_name, weights, extras)

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
