from __future__ import print_function
from __future__ import division
from __future__ import absolute_import


class SamplerData(object):
    def __init__(
        self,
        mag_filter=None,
        min_filter=None,
        wrap_s=None,
        wrap_t=None,
        name=None,
        extras=None,
        extensions=None,
    ):
        self.mag_filter = mag_filter
        self.min_filter = min_filter
        self.wrap_s = wrap_s
        self.wrap_t = wrap_t
        self.name = name
        self.extras = extras
        self.extensions = extensions

    def get_dict(self):
        sampler_dict = {}
        if self.mag_filter is not None:
            sampler_dict['magFilter'] = self.mag_filter
        if self.min_filter is not None:
            sampler_dict['minFilter'] = self.min_filter
        if self.wrap_s is not None:
            sampler_dict['wrapS'] = self.wrap_s
        if self.wrap_t is not None:
            sampler_dict['wrapT'] = self.wrap_t
        if self.name is not None:
            sampler_dict['name'] = self.name
        if self.extras is not None:
            sampler_dict['extras'] = self.extras
        if self.extensions is not None:
            sampler_dict['extensions'] = self.extensions
        return sampler_dict


class TextureData(object):
    def __init__(self, sampler=None, source=None, name=None, extras=None, extensions=None):
        self.sampler = sampler
        self.source = source
        self.name = name
        self.extras = extras
        self.extensions = extensions

    def get_dict(self, sampler_index_by_key, image_index_by_key):
        texture_dict = {}
        if self.sampler is not None:
            texture_dict['sampler'] = sampler_index_by_key[self.sampler]
        if self.source is not None:
            texture_dict['source'] = image_index_by_key[self.source]
        if self.name is not None:
            texture_dict['name'] = self.name
        if self.extras is not None:
            texture_dict['extras'] = self.extras
        if self.extensions is not None:
            texture_dict['extensions'] = self.extensions
        return texture_dict


class TextureInfoData(object):
    def __init__(self, index, tex_coord=None, extras=None, extensions=None):
        self.index = index
        self.tex_coord = tex_coord
        self.extras = extras
        self.extensions = extensions

    def get_dict(self, texture_index_by_key):
        texture_info_dict = {'index': texture_index_by_key[self.index]}
        if self.tex_coord is not None:
            texture_info_dict['texCoord'] = self.tex_coord
        if self.extras is not None:
            texture_info_dict['extras'] = self.extras
        if self.extensions is not None:
            texture_info_dict['extensions'] = self.extensions
        return texture_info_dict


class OcclusionTextureInfoData(TextureInfoData):
    def __init__(self, index, tex_coord=None, extras=None, extensions=None, strength=None):
        super(OcclusionTextureInfoData).__init__(index, tex_coord, extras, extensions)
        self.strength = strength

    def get_dict(self, texture_index_by_key):
        texture_info_dict = super(OcclusionTextureInfoData).get_dict(texture_index_by_key)
        if self.strength is not None:
            texture_info_dict['strength'] = self.strength
        return texture_info_dict


class NormalTextureInfoData(TextureInfoData):
    def __init__(self, index, tex_coord=None, extras=None, extensions=None, scale=None):
        super(NormalTextureInfoData).__init__(index, tex_coord, extras, extensions)
        self.scale = scale

    def get_dict(self, texture_index_by_key):
        texture_info_dict = super(NormalTextureInfoData).get_dict(texture_index_by_key)
        if self.scale is not None:
            texture_info_dict['scale'] = self.scale
        return texture_info_dict


class PBRMetallicRoughnessData(object):
    def __init__(
        self,
        base_color_factor=None,
        base_color_texture=None,  # TextureInfoData
        metallic_factor=None,
        roughness_factor=None,
        metallic_roughness_texture=None,  # TextureInfoData
        extras=None,
        extensions=None,
    ):
        self.base_color_factor = base_color_factor
        self.base_color_texture = base_color_texture
        self.metallic_factor = metallic_factor
        self.roughness_factor = roughness_factor
        self.metallic_roughness_texture = metallic_roughness_texture
        self.extras = extras
        self.extensions = extensions

    def get_dict(self, texture_index_by_key):
        roughness_dict = {}
        if self.base_color_factor is not None:
            roughness_dict['baseColorFactor'] = self.base_color_factor
        if self.base_color_texture is not None:
            roughness_dict['baseColorTexture'] = self.base_color_texture.get_dict(texture_index_by_key)
        if self.metallic_factor is not None:
            roughness_dict['metallicFactor'] = self.metallic_factor
        if self.metallic_roughness_texture is not None:
            roughness_dict['metallicRoughnessTexture'] = self.metallic_roughness_texture.get_dict(texture_index_by_key)
        if self.extras is not None:
            roughness_dict['extras'] = self.extras
        if self.extensions is not None:
            roughness_dict['extensions'] = self.extensions
        return roughness_dict


class MaterialData(object):
    def __init__(
        self,
        name=None,
        extras=None,
        pbr_metallic_roughness=None,  # PBRMetallicRoughnessData
        normal_texture=None,  # NormalTextureInfoData
        occlusion_texture=None,  # OcclusionTextureInfoData
        emissive_texture=None,  # TextureInfoData
        emissive_factor=None,
        alpha_mode=None,
        alpha_cutoff=None,
        double_sided=None,
        extensions=None,
    ):
        self.name = name
        self.extras = extras
        self.pbr_metallic_roughness = pbr_metallic_roughness
        self.normal_texture = normal_texture
        self.occlusion_texture = occlusion_texture
        self.emissive_texture = emissive_texture
        self.emissive_factor = emissive_factor
        self.alpha_mode = alpha_mode
        self.alpha_cutoff = alpha_cutoff
        self.double_sided = double_sided
        self.extensions = extensions

    def get_dict(self, texture_index_by_key):
        material_dict = {}
        if self.name is not None:
            material_dict['name'] = self.name
        if self.extras is not None:
            material_dict['extras'] = self.extras
        if self.pbr_metallic_roughness is not None:
            material_dict['pbrMetallicRoughness'] = self.pbr_metallic_roughness.get_dict(texture_index_by_key)
        if self.normal_texture is not None:
            material_dict['normalTexture'] = self.normal_texture.get_dict(texture_index_by_key)
        if self.occlusion_texture is not None:
            material_dict['materialTexture'] = self.occlusion_texture.get_dict(texture_index_by_key)
        if self.emissive_texture is not None:
            material_dict['emissiveTexture'] = self.emissive_texture.get_dict(texture_index_by_key)
        if self.emissive_factor is not None:
            material_dict['emissiveFactor'] = self.emissive_factor
        if self.alpha_mode is not None:
            material_dict['alphaMode'] = self.alpha_mode
        if self.alpha_cutoff is not None:
            material_dict['alphaFactor'] = self.alpha_cutoff
        if self.double_sided is not None:
            material_dict['doubleSided'] = self.double_sided
        if self.extensions is not None:
            material_dict['extensions'] = self.extensions
        return material_dict


class CameraData(object):
    def __init__(self, type_, orthographic=None, perspective=None, name=None, extras=None, extensions=None):
        self.type = type_
        self.orthographic = orthographic
        self.perspective = perspective
        self.name = name
        self.extras = extras
        self.extensions = extensions

    def get_dict(self):
        camera_dict = {'type': self.type}
        if self.orthographic is not None:
            camera_dict['orthographic'] = self.orthographic
        if self.perspective is not None:
            camera_dict['perspective'] = self.perspective
        if self.name is not None:
            camera_dict['name'] = self.name
        if self.extras is not None:
            camera_dict['extras'] = self.extras
        if self.extensions is not None:
            camera_dict['extensions'] = self.extensions
        return camera_dict


class AnimationSamplerData(object):
    def __init__(self, input_, output, interpolation=None, extras=None, extensions=None):
        self.input = input_
        self.output = output
        self.interpolation = interpolation
        self.extras = extras
        self.extensions = extensions

    def get_dict(self, input_accessor, output_accessor):
        sampler_dict = {
            'input': input_accessor,
            'output': output_accessor,
        }
        if self.interpolation is not None:
            sampler_dict['interpolation'] = self.interpolation
        if self.extras is not None:
            sampler_dict['extras'] = self.extras
        if self.extensions is not None:
            sampler_dict['extensions'] = self.extensions
        return sampler_dict


class TargetData(object):
    def __init__(self, path, node=None, extras=None, extensions=None):
        self.path = path
        self.node = node
        self.extras = extras
        self.extensions = extensions

    def get_dict(self, node_index_by_key):
        target_dict = {
            'path': self.path
        }
        if self.node is not None:
            target_dict['node'] = node_index_by_key[self.node]
        if self.extras is not None:
            target_dict['extras'] = self.extras
        if self.extensions is not None:
            target_dict['extensions'] = self.extensions
        return target_dict


class ChannelData(object):
    def __init__(self, sampler, target, extras=None, extensions=None):
        self.sampler = sampler
        self.target = target
        self.extras = extras
        self.extensions = extensions

    def get_dict(self, node_index_by_key, sampler_index_by_key):
        channel_dict = {
            'sampler': sampler_index_by_key[self.sampler],
            'target': self.target.get_dict(node_index_by_key),
        }
        if self.extras is not None:
            channel_dict['extras'] = self.extras
        if self.extensions is not None:
            channel_dict['extensions'] = self.extensions
        return channel_dict


class AnimationData(object):
    def __init__(self, channels, samplers_dict, name=None, extras=None, extensions=None):
        self.channels = channels
        self.samplers_dict = samplers_dict
        self.name = name
        self.extras = extras
        self.extensions = extensions

        self._sampler_index_by_key = None

    def get_dict(self, samplers_list, node_index_by_key):
        channels = [
            channel_data.get_dict(node_index_by_key, self._sampler_index_by_key)
            for channel_data in self.channels
        ]
        animation_dict = {
            'channels': channels,
            'samplers': samplers_list,
        }
        if self.name is not None:
            animation_dict['name'] = self.name
        if self.extras is not None:
            animation_dict['extras'] = self.extras
        if self.extensions is not None:
            animation_dict['extensions'] = self.extensions
        return animation_dict

    def get_sampler_index_by_key(self):
        self._sampler_index_by_key = {key: index for index, key in enumerate(self.samplers_dict)}
        return self._sampler_index_by_key


class SkinData(object):
    def __init__(self, joints, inverse_bind_matrices=None, skeleton=None, name=None, extras=None, extensions=None):
        self.joints = joints
        self.inverse_bind_matrices = inverse_bind_matrices
        self.skeleton = skeleton
        self.name = name
        self.extras = extras
        self.extensions = extensions

    def get_dict(self, node_index_by_key, accessor_index):
        skin_dict = {'joints': [
            node_index_by_key.get(item)
            for item in self.joints
            if node_index_by_key.get(item)
        ]}
        if self.skeleton is not None:
            skin_dict['skeleton'] = self.skeleton
        if self.name is not None:
            skin_dict['name'] = self.name
        if self.extras is not None:
            skin_dict['extras'] = self.extras
        if self.inverse_bind_matrices is not None:
            skin_dict['inverseBindMatrices'] = accessor_index
        if self.extensions is not None:
            skin_dict['extensions'] = self.extensions
        return skin_dict


class ImageData(object):
    def __init__(self, image_data=None, uri=None, mime_type=None, name=None, extras=None, extensions=None):
        self.uri = uri
        self.mime_type = mime_type
        self.name = name
        self.extras = extras
        self.extensions = extensions

        self.data = image_data

    def get_dict(self, uri, buffer_view):
        image_dict = {}
        if self.name is not None:
            image_dict['name'] = self.name
        if self.extras is not None:
            image_dict['extras'] = self.extras
        if self.mime_type is not None:
            image_dict['mimeType'] = self.mime_type
        if self.uri is not None:
            image_dict['uri'] = self.uri
        if uri is not None:
            image_dict['uri'] = uri
        if buffer_view is not None:
            image_dict['bufferView'] = buffer_view
        if self.extensions is not None:
            image_dict['extensions'] = self.extensions
        return image_dict


class PrimitiveData(object):
    def __init__(self, attributes, indices=None, material=None, mode=None, targets=None, extras=None, extensions=None):
        self.attributes = attributes or {}
        self.indices = indices
        self.material = material
        self.mode = mode
        self.targets = targets
        self.extras = extras
        self.extensions = extensions

    def get_dict(self, indices_accessor, attributes_dict, targets_dict, material_index_by_key):
        primitive_dict = {'indices': indices_accessor}
        if self.material is not None:
            primitive_dict['material'] = material_index_by_key[self.material]
        if self.mode is not None:
            primitive_dict['mode'] = self.mode
        if self.extras is not None:
            primitive_dict['extras'] = self.extras
        if attributes_dict:
            primitive_dict['attributes'] = attributes_dict
        if targets_dict:
            primitive_dict['targets'] = targets_dict
        if self.extensions is not None:
            primitive_dict['extensions'] = self.extensions
        return primitive_dict
