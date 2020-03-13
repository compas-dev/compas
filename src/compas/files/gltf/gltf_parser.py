from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

from compas.files.gltf.data_classes import AnimationData
from compas.files.gltf.data_classes import AnimationSamplerData
from compas.files.gltf.data_classes import CameraData
from compas.files.gltf.data_classes import ChannelData
from compas.files.gltf.data_classes import MaterialData
from compas.files.gltf.data_classes import NormalTextureInfoData
from compas.files.gltf.data_classes import OcclusionTextureInfoData
from compas.files.gltf.data_classes import PBRMetallicRoughnessData
from compas.files.gltf.data_classes import PrimitiveData
from compas.files.gltf.data_classes import SamplerData
from compas.files.gltf.data_classes import SkinData
from compas.files.gltf.data_classes import TargetData
from compas.files.gltf.data_classes import TextureData
from compas.files.gltf.data_classes import TextureInfoData
from compas.files.gltf.gltf_content import GLTFContent
from compas.files.gltf.gltf_mesh import GLTFMesh
from compas.files.gltf.gltf_node import GLTFNode
from compas.files.gltf.gltf_scene import GLTFScene
from compas.files.gltf.helpers import get_matrix_from_col_major_list


class GLTFParser(object):
    """Parse the contents of the reader into a :class:`compas.files.GLTFContent` object.

    Parameters
    ----------
    reader : :class:`compas.files.GLTFReader`

    Attributes
    ----------
    reader : :class:`compas.files.GLTFReader`
    content : :class:`compas.files.GLTFContent`
    """
    def __init__(self, reader):
        self.reader = reader
        self.content = GLTFContent()

        self.parse()

    def parse(self):
        self.content.default_scene_key = self.get_default_scene()
        self.content.extras = self.get_extras()
        self.content.extensions = self.get_extensions()

        self.content.images = {key: image_data for key, image_data in enumerate(self.reader.image_data)}
        self.content.samplers = {key: self.get_sampler_data(sampler) for key, sampler in enumerate(self.reader.json.get('samplers', []))}
        self.content.textures = {key: self.get_texture_data(texture) for key, texture in enumerate(self.reader.json.get('textures', []))}
        self.content.materials = {key: self.get_material_data(material) for key, material in enumerate(self.reader.json.get('materials', []))}
        self.content.cameras = {key: self.get_camera_data(camera) for key, camera in enumerate(self.reader.json.get('cameras', []))}
        for mesh in self.reader.json.get('meshes', []):
            self.add_gltf_mesh(mesh)
        for node in self.reader.json.get('nodes', []):
            self.add_gltf_node(node)
        for scene in self.reader.json.get('scenes', []):
            self.add_gltf_scene(scene)
        self.content.animations = {key: self.get_animation_data(animation) for key, animation in enumerate(self.reader.json.get('animations', []))}
        self.content.skins = {key: self.get_skin_data(skin) for key, skin in enumerate(self.reader.json.get('skins', []))}
        self.content.update_node_transforms_and_positions()

    def get_sampler_data(self, sampler):
        sampler_data = SamplerData()
        sampler_data.mag_filter = sampler.get('magFilter')
        sampler_data.min_filter = sampler.get('minFilter')
        sampler_data.wrap_s = sampler.get('wrapS')
        sampler_data.wrap_t = sampler.get('wrapT')
        sampler_data.name = sampler.get('name')
        sampler_data.extras = sampler.get('extras')
        return sampler_data

    def get_texture_data(self, texture):
        texture_data = TextureData()
        texture_data.sampler = texture.get('sampler')
        texture_data.source = texture.get('source')
        texture_data.name = texture.get('name')
        texture_data.extras = texture.get('extras')
        return texture_data

    def get_material_data(self, material):
        material_data = MaterialData()
        material_data.name = material.get('name')
        material_data.extras = material.get('extras')
        material_data.pbr_metallic_roughness = self.get_pbr_metallic_roughness_info_data(material.get('pbrMetallicRoughness'))
        material_data.normal_texture = self.get_normal_texture_info_data(material.get('normalTexture'))
        material_data.occlusion_texture = self.get_occlusion_texture_info_data(material.get('occlusionTexture'))
        material_data.emissive_texture = self.get_texture_info_data(material.get('emissiveTexture'))
        material_data.emissive_factor = material.get('emissiveFactor')
        material_data.alpha_mode = material.get('alphaMode')
        material_data.alpha_cutoff = material.get('alphaCutoff')
        material_data.double_sided = material.get('doubleSided')
        return material_data

    def get_pbr_metallic_roughness_info_data(self, texture_info):
        if not texture_info:
            return None
        roughness_data = PBRMetallicRoughnessData()
        roughness_data.base_color_factor = texture_info.get('baseColorFactor')
        roughness_data.base_color_texture = self.get_texture_info_data(texture_info.get('baseColorTexture'))
        roughness_data.metallic_factor = texture_info.get('metallicFactor')
        roughness_data.roughness_factor = texture_info.get('roughnessFactor')
        roughness_data.metallic_roughness_texture = self.get_texture_info_data(texture_info.get('metallicRoughnessTexture'))
        roughness_data.extras = texture_info.get('extras')
        return roughness_data

    def get_texture_info_data(self, texture_info):
        if not texture_info:
            return None
        texture_info_data = TextureInfoData(texture_info['index'])
        texture_info_data.tex_coord = texture_info.get('texCoord')
        texture_info_data.extras = texture_info.get('extras')
        return texture_info_data

    def get_occlusion_texture_info_data(self, texture_info):
        if not texture_info:
            return None
        texture_info_data = OcclusionTextureInfoData(texture_info['index'])
        texture_info_data.tex_coord = texture_info.get('texCoord')
        texture_info_data.extras = texture_info.get('extras')
        texture_info_data.strength = texture_info.get('strength')
        return texture_info_data

    def get_normal_texture_info_data(self, texture_info):
        if not texture_info:
            return None
        texture_info_data = NormalTextureInfoData(texture_info['index'])
        texture_info_data.tex_coord = texture_info.get('texCoord')
        texture_info_data.extras = texture_info.get('extras')
        texture_info_data.scale = texture_info.get('scale')
        return texture_info_data

    def get_skin_data(self, skin):
        skin_data = SkinData(skin['joints'])
        if 'inverseBindMatrices' in skin:
            skin_data.inverse_bind_matrices = self.reader.data[skin['inverseBindMatrices']]
        skin_data.skeleton = skin.get('skeleton')
        skin_data.name = skin.get('name')
        skin_data.extras = skin.get('extras')
        return skin_data

    def get_animation_data(self, animation):
        sampler_data_dict = {}
        for index, sampler in enumerate(animation['samplers']):
            input_ = self.reader.data[sampler['input']]
            output = self.reader.data[sampler['output']]
            sampler_data = AnimationSamplerData(input_, output, sampler.get('interpolation'), sampler.get('extras'))
            sampler_data_dict[index] = sampler_data
        channel_data_list = []
        for channel in animation['channels']:
            target_data = TargetData(channel['target']['path'])
            target_data.node = channel['target'].get('node')
            target_data.extras = channel['target'].get('extras')
            channel_data = ChannelData(channel['sampler'], target_data)
            channel_data_list.append(channel_data)
        return AnimationData(channel_data_list, sampler_data_dict, animation.get('name'), animation.get('extras'))

    def get_extras(self):
        return self.reader.json.get('extras')

    def get_default_scene(self):
        return self.reader.json.get('scene')

    def get_extensions(self):
        return self.reader.json.get('extensions')

    def get_camera_data(self, camera):
        camera_data = CameraData(camera['type'])
        camera_data.orthographic = camera.get('orthographic')
        camera_data.perspective = camera.get('perspective')
        camera_data.name = camera.get('name')
        camera_data.extras = camera.get('extras')
        return camera_data

    def add_gltf_scene(self, scene):
        scene_obj = GLTFScene(self.content)
        scene_obj.name = scene.get('name')
        scene_obj.extras = scene.get('extras')
        scene_obj.children = scene.get('nodes', [])

    def add_gltf_node(self, node):
        gltf_node = GLTFNode(self.content)
        gltf_node.name = node.get('name')
        # Accessing protected attribute to bypass validation:
        # Nodes may reference children that haven't yet been added to the GLTFContent
        gltf_node.children._value = node.get('children', [])
        gltf_node.translation = node.get('translation')
        gltf_node.rotation = node.get('rotation')
        gltf_node.scale = node.get('scale')
        gltf_node.matrix = self.get_matrix(node)
        gltf_node.weights = node.get('weights')
        gltf_node.mesh_key = node.get('mesh')
        gltf_node.camera = node.get('camera')
        gltf_node.skin = node.get('skin')
        gltf_node.extras = node.get('extras')

    def get_matrix(self, node):
        if 'matrix' in node:
            return get_matrix_from_col_major_list(node['matrix'])
        return None

    def add_gltf_mesh(self, mesh):
        mesh_name = mesh.get('name')
        extras = mesh.get('extras')
        primitives = mesh['primitives']
        weights = mesh.get('weights')

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
        GLTFMesh(primitive_data_list, self.content, mesh_name, weights, extras)

    def get_indices(self, primitive, num_vertices):
        if 'indices' not in primitive:
            return self.get_generic_indices(num_vertices)
        indices_accessor_index = primitive['indices']
        return self.reader.data[indices_accessor_index]

    def get_generic_indices(self, num_vertices):
        return list(range(num_vertices))
