import base64
import os
import struct
from typing import Any

from compas.files.gltf.constants import COMPONENT_TYPE_ENUM
from compas.files.gltf.constants import COMPONENT_TYPE_FLOAT
from compas.files.gltf.constants import COMPONENT_TYPE_UNSIGNED_INT
from compas.files.gltf.constants import COMPONENT_TYPE_UNSIGNED_SHORT
from compas.files.gltf.constants import NUM_COMPONENTS_BY_TYPE_ENUM
from compas.files.gltf.constants import TYPE_MAT4
from compas.files.gltf.constants import TYPE_SCALAR
from compas.files.gltf.constants import TYPE_VEC2
from compas.files.gltf.constants import TYPE_VEC3
from compas.files.gltf.constants import TYPE_VEC4
from compas.files.gltf.data_classes import BaseGLTFDataClass
from compas.files.gltf.data_classes import CameraData
from compas.files.gltf.data_classes import ImageData
from compas.files.gltf.data_classes import MaterialData
from compas.files.gltf.data_classes import NormalTextureInfoData
from compas.files.gltf.data_classes import OcclusionTextureInfoData
from compas.files.gltf.data_classes import PBRMetallicRoughnessData
from compas.files.gltf.data_classes import SamplerData
from compas.files.gltf.data_classes import TextureData

from .gltf_document import GLTFDocument
from .gltf_payload import GLTFPayload
from .gltf_types import GLTFFormat


class GLTFEncoder:
    """Encode a semantic glTF document without writing targets."""

    def __init__(
        self,
        format: GLTFFormat = "gltf",
        embed_data: bool = False,
        filename: str = "model",
    ) -> None:
        if format not in ("gltf", "glb"):
            raise ValueError(f"Unsupported glTF format: {format}")
        self._filename = filename
        self._format: GLTFFormat = format
        self._embed_data = embed_data
        self._content: GLTFDocument
        self._gltf_dict = {}
        self._mesh_index_by_key = {}
        self._node_index_by_key = {}
        self._scene_index_by_key = {}
        self._camera_index_by_key = {}
        self._skin_index_by_key = {}
        self._material_index_by_key = {}
        self._texture_index_by_key = {}
        self._sampler_index_by_key = {}
        self._image_index_by_key = {}
        self._buffer = b""

    def encode(self, content: GLTFDocument) -> GLTFPayload:
        """Encode a document into a target-independent payload.

        Returns
        -------
        GLTFPayload
            JSON data, binary data, and adjacent resources.

        """
        content.validate()
        self._content = content.without_orphans()

        self._set_initial_gltf_dict()
        self._mesh_index_by_key = self._get_index_by_key(self._content.meshes)
        self._node_index_by_key = self._get_index_by_key(self._content.nodes)
        self._scene_index_by_key = self._get_index_by_key(self._content.scenes)
        self._camera_index_by_key = self._get_index_by_key(self._content.cameras)
        self._skin_index_by_key = self._get_index_by_key(self._content.skins)
        self._material_index_by_key = self._get_index_by_key(self._content.materials)
        self._texture_index_by_key = self._get_index_by_key(self._content.textures)
        self._sampler_index_by_key = self._get_index_by_key(self._content.samplers)
        self._image_index_by_key = self._get_index_by_key(self._content.images)
        self._buffer = b""

        self._add_meshes()
        self._add_nodes()
        self._add_scenes()
        self._add_cameras()
        self._add_skins()
        self._add_materials()
        self._add_textures()
        self._add_samplers()
        self._add_images()
        self._add_animations()
        self._add_buffer()
        self._add_extensions()

        format = self._format
        resources = {}
        if format == "gltf" and not self._embed_data and self._buffer:
            resources[f"{self._filename}.bin"] = self._buffer
        if format == "gltf" and not self._embed_data:
            for image in self._content.images.values():
                if image.uri and image.data is not None:
                    resources[os.path.basename(image.uri)] = image.data
        return GLTFPayload(format, self._gltf_dict, self._buffer, resources)

    def _get_index_by_key(self, d):
        return {key: index for index, key in enumerate(d)}

    def _add_extensions_recursively(self, item):
        if not isinstance(item, BaseGLTFDataClass):
            return
        keys = item.extension_keys()
        if not keys:
            return
        if self._content.extensions_used is None:
            self._content.extensions_used = []
        extensions_used = self._content.extensions_used
        assert extensions_used is not None
        for key in sorted(keys):
            if key not in extensions_used:
                extensions_used.append(key)

    def _add_images(self):
        if not self._content.images:
            return
        images_list: list[Any] = [None] * len(self._content.images)
        for key, image_data in self._content.images.items():
            if image_data.uri:
                basename = os.path.basename(image_data.uri)
            else:
                basename = None
            if self._embed_data:
                uri = self._construct_image_data_uri(image_data)
                buffer_view = None
            elif self._format == "glb":
                uri = None
                buffer_view = self._construct_buffer_view(image_data.data)
            elif basename:
                uri = basename
                buffer_view = None
            else:
                uri = None
                buffer_view = self._construct_buffer_view(image_data.data)
            images_list[self._image_index_by_key[key]] = self._image_json(image_data, uri, buffer_view)
            self._add_extensions_recursively(image_data)
        self._gltf_dict["images"] = images_list

    def _construct_image_data_uri(self, image_data):
        if image_data.data is None:
            return None
        return "data:" + (image_data.mime_type if image_data.mime_type else "") + ";base64," + base64.b64encode(image_data.data).decode("ascii")

    def _add_extensions(self):
        if self._content.extensions_used:
            self._gltf_dict["extensionsUsed"] = self._content.extensions_used
        if self._content.extensions_required:
            self._gltf_dict["extensionsRequired"] = self._content.extensions_required

    def _add_samplers(self):
        if not self._content.samplers:
            return
        samplers_list: list[Any] = [None] * len(self._content.samplers)
        for key, sampler_data in self._content.samplers.items():
            samplers_list[self._sampler_index_by_key[key]] = self._sampler_json(sampler_data)
        self._gltf_dict["samplers"] = samplers_list

    def _add_textures(self):
        if not self._content.textures:
            return
        textures_list: list[Any] = [None] * len(self._content.textures)
        for key, texture_data in self._content.textures.items():
            textures_list[self._texture_index_by_key[key]] = self._texture_json(texture_data)
            self._add_extensions_recursively(texture_data)
        self._gltf_dict["textures"] = textures_list

    def _add_materials(self):
        if not self._content.materials:
            return
        materials_list: list[Any] = [None] * len(self._content.materials)
        for key, material_data in self._content.materials.items():
            materials_list[self._material_index_by_key[key]] = self._material_json(material_data)
            self._add_extensions_recursively(material_data)
        self._gltf_dict["materials"] = materials_list

    def _add_skins(self):
        if not self._content.skins:
            return
        skins_list: list[Any] = [None] * len(self._content.skins)
        for key, skin_data in self._content.skins.items():
            accessor_index = self._construct_accessor(skin_data.inverse_bind_matrices, COMPONENT_TYPE_FLOAT, TYPE_MAT4)
            skins_list[self._skin_index_by_key[key]] = self._skin_json(skin_data, accessor_index)
            self._add_extensions_recursively(skin_data)
        self._gltf_dict["skins"] = skins_list

    def _add_cameras(self):
        if not self._content.cameras:
            return
        camera_list: list[Any] = [None] * len(self._content.cameras)
        for key, camera_data in self._content.cameras.items():
            camera_list[self._camera_index_by_key[key]] = self._camera_json(camera_data)
            self._add_extensions_recursively(camera_data)
        self._gltf_dict["cameras"] = camera_list

    def _add_meshes(self):
        if not self._content.meshes:
            return
        mesh_list: list[Any] = [None] * len(self._content.meshes)
        for key, mesh_data in self._content.meshes.items():
            primitives = self._construct_primitives(mesh_data)
            mesh_list[self._mesh_index_by_key[key]] = self._mesh_json(mesh_data, primitives)
            self._add_extensions_recursively(mesh_data)
        self._gltf_dict["meshes"] = mesh_list

    def _add_buffer(self):
        if not self._buffer:
            return
        buffer: dict[str, Any] = {"byteLength": len(self._buffer)}
        if self._embed_data:
            buffer["uri"] = "data:application/octet-stream;base64," + base64.b64encode(self._buffer).decode("ascii")
        elif self._format == "gltf":
            buffer["uri"] = f"{self._filename}.bin"
        self._gltf_dict["buffers"] = [buffer]

    def _add_animations(self):
        if not self._content.animations:
            return None
        animation_list = []
        for animation_data in self._content.animations.values():
            samplers_list = self._construct_animation_samplers_list(animation_data)
            animation_list.append(self._animation_json(animation_data, samplers_list))
            self._add_extensions_recursively(animation_data)
        self._gltf_dict["animations"] = animation_list

    def _construct_animation_samplers_list(self, animation_data):
        sampler_index_by_key = animation_data.get_sampler_index_by_key()
        samplers_list: list[Any] = [None] * len(sampler_index_by_key)
        for key, sampler_data in animation_data.samplers_dict.items():
            input_accessor = self._construct_accessor(
                sampler_data.input,
                COMPONENT_TYPE_FLOAT,
                TYPE_SCALAR,
                include_bounds=True,
            )
            type_ = TYPE_VEC3
            if isinstance(sampler_data.output[0], int) or isinstance(sampler_data.output[0], float):
                type_ = TYPE_SCALAR
            elif len(sampler_data.output[0]) == 4:
                type_ = TYPE_VEC4
            output_accessor = self._construct_accessor(sampler_data.output, COMPONENT_TYPE_FLOAT, type_)
            samplers_list[sampler_index_by_key[key]] = self._animation_sampler_json(sampler_data, input_accessor, output_accessor)
        return samplers_list

    def _set_initial_gltf_dict(self):
        gltf_dict = dict(self._content.unknown)
        gltf_dict["asset"] = dict(self._content.asset)
        if self._content.extras:
            gltf_dict["extras"] = self._content.extras
        if self._content.extensions:
            gltf_dict["extensions"] = self._content.extensions
        self._gltf_dict = gltf_dict

    def _add_scenes(self):
        if not self._content.scenes:
            return
        if self._content.default_scene_key is not None:
            self._gltf_dict["scene"] = self._scene_index_by_key[self._content.default_scene_key]
        else:
            self._gltf_dict["scene"] = list(self._content.scenes.values())[0].key
        scene_list: list[Any] = [None] * len(self._content.scenes.values())
        for key, scene in self._content.scenes.items():
            scene_list[self._scene_index_by_key[key]] = self._scene_json(scene)
        self._gltf_dict["scenes"] = scene_list

    def _add_nodes(self):
        if not self._content.nodes:
            return
        node_list: list[Any] = [None] * len(self._content.nodes)
        for key, node in self._content.nodes.items():
            node_list[self._node_index_by_key[key]] = self._node_json(node)
        self._gltf_dict["nodes"] = node_list

    def _construct_primitives(self, mesh_data):
        primitives = []
        for primitive_data in mesh_data.primitive_data_list:
            component_type = COMPONENT_TYPE_UNSIGNED_SHORT
            if primitive_data.indices and max(primitive_data.indices) > 65535:
                component_type = COMPONENT_TYPE_UNSIGNED_INT
            indices_accessor = self._construct_accessor(primitive_data.indices, component_type, TYPE_SCALAR)

            attributes = {}
            for attr in primitive_data.attributes:
                component_type = COMPONENT_TYPE_UNSIGNED_INT if attr.startswith("JOINT") else COMPONENT_TYPE_FLOAT
                type_ = TYPE_VEC3
                if len(primitive_data.attributes[attr][0]) == 4:
                    type_ = TYPE_VEC4
                if len(primitive_data.attributes[attr][0]) == 2:
                    type_ = TYPE_VEC2
                attributes[attr] = self._construct_accessor(primitive_data.attributes[attr], component_type, type_, True)

            targets = []
            for target in primitive_data.targets or []:
                target_dict = {}
                for attr in target:
                    component_type = COMPONENT_TYPE_FLOAT
                    type_ = TYPE_VEC3
                    target_dict[attr] = self._construct_accessor(target[attr], component_type, type_, True)
                targets.append(target_dict)

            primitive_dict = self._primitive_json(primitive_data, indices_accessor, attributes, targets)

            primitives.append(primitive_dict)
        return primitives

    def _construct_accessor(self, data, component_type, type_, include_bounds=False):
        if data is None:
            return None
        count = len(data)

        fmt_char = COMPONENT_TYPE_ENUM[component_type]
        fmt = "<" + fmt_char * NUM_COMPONENTS_BY_TYPE_ENUM[type_]

        component_size = struct.calcsize("<" + fmt_char)
        if type_ == "MAT2" and component_size == 1:
            fmt = "<FFxxFFxx".replace("F", fmt_char)
        elif type_ == "MAT3" and component_size == 1:
            fmt = "<FFFxFFFxFFFx".replace("F", fmt_char)
        elif type_ == "MAT3" and component_size == 2:
            fmt = "<FFFxxFFFxxFFFxx".replace("F", fmt_char)

        component_len = struct.calcsize(fmt)

        size = count * component_len
        bytes_ = bytearray(size)

        for i, datum in enumerate(data):
            if isinstance(datum, int) or isinstance(datum, float):
                struct.pack_into(fmt, bytes_, (i * component_len), datum)
            else:
                struct.pack_into(fmt, bytes_, (i * component_len), *datum)

        buffer_view_index = self._construct_buffer_view(bytes_)
        accessor_dict = {
            "bufferView": buffer_view_index,
            "count": count,
            "componentType": component_type,
            "type": type_,
        }
        if include_bounds:
            try:
                # Here we check if `data` contains tuples,
                # and compute min/max per coordinate.
                _ = [e for e in data[0]]
                minimum = tuple(map(min, zip(*data)))
                maximum = tuple(map(max, zip(*data)))
            except TypeError:
                # Here, `data` must contain primitives and not tuples,
                # so min and max are more simply computed.
                minimum = (min(data),)
                maximum = (max(data),)
            accessor_dict["min"] = minimum
            accessor_dict["max"] = maximum

        self._gltf_dict.setdefault("accessors", []).append(accessor_dict)

        return len(self._gltf_dict["accessors"]) - 1

    def _construct_buffer_view(self, bytes_):
        if not bytes_:
            return None
        byte_offset = self._update_buffer(bytes_)
        buffer_view_dict = {
            "buffer": 0,
            "byteLength": len(bytes_),
            "byteOffset": byte_offset,
        }

        self._gltf_dict.setdefault("bufferViews", []).append(buffer_view_dict)

        return len(self._gltf_dict["bufferViews"]) - 1

    def _update_buffer(self, bytes_):
        padding = -len(self._buffer) % 4
        if padding:
            self._buffer += b"\0" * padding
        byte_offset = len(self._buffer)
        self._buffer += bytes_
        return byte_offset

    def _extensions_json(self, extensions):
        if not extensions:
            return None
        return {key: self._extension_json(value) if isinstance(value, BaseGLTFDataClass) else value for key, value in extensions.items()}

    def _common_json(self, item):
        result = {}
        if item.extras is not None:
            result["extras"] = item.extras
        extensions = self._extensions_json(item.extensions)
        if extensions is not None:
            result["extensions"] = extensions
        return result

    def _texture_info_json(self, item):
        result: dict[str, Any] = {"index": self._texture_index_by_key[item.index]}
        if item.tex_coord is not None:
            result["texCoord"] = item.tex_coord
        if isinstance(item, NormalTextureInfoData) and item.scale is not None:
            result["scale"] = item.scale
        if isinstance(item, OcclusionTextureInfoData) and item.strength is not None:
            result["strength"] = item.strength
        result.update(self._common_json(item))
        return result

    def _sampler_json(self, item: SamplerData):
        result = self._common_json(item)
        for attr, key in (("mag_filter", "magFilter"), ("min_filter", "minFilter"), ("wrap_s", "wrapS"), ("wrap_t", "wrapT"), ("name", "name")):
            value = getattr(item, attr)
            if value is not None:
                result[key] = value
        return result

    def _texture_json(self, item: TextureData):
        result = self._common_json(item)
        if item.sampler is not None:
            result["sampler"] = self._sampler_index_by_key[item.sampler]
        if item.source is not None:
            result["source"] = self._image_index_by_key[item.source]
        if item.name is not None:
            result["name"] = item.name
        return result

    def _pbr_json(self, item: PBRMetallicRoughnessData):
        result = self._common_json(item)
        for attr, key in (("base_color_factor", "baseColorFactor"), ("metallic_factor", "metallicFactor"), ("roughness_factor", "roughnessFactor")):
            value = getattr(item, attr)
            if value is not None:
                result[key] = value
        if item.base_color_texture is not None:
            result["baseColorTexture"] = self._texture_info_json(item.base_color_texture)
        if item.metallic_roughness_texture is not None:
            result["metallicRoughnessTexture"] = self._texture_info_json(item.metallic_roughness_texture)
        return result

    def _material_json(self, item: MaterialData):
        result = self._common_json(item)
        if item.name is not None:
            result["name"] = item.name
        if item.pbr_metallic_roughness is not None:
            result["pbrMetallicRoughness"] = self._pbr_json(item.pbr_metallic_roughness)
        for attr, key in (("normal_texture", "normalTexture"), ("occlusion_texture", "occlusionTexture"), ("emissive_texture", "emissiveTexture")):
            value = getattr(item, attr)
            if value is not None:
                result[key] = self._texture_info_json(value)
        for attr, key in (("emissive_factor", "emissiveFactor"), ("alpha_mode", "alphaMode"), ("alpha_cutoff", "alphaCutoff"), ("double_sided", "doubleSided")):
            value = getattr(item, attr)
            if value is not None:
                result[key] = value
        return result

    def _camera_json(self, item: CameraData):
        result = self._common_json(item)
        result["type"] = item.type
        for attr in ("orthographic", "perspective", "name"):
            value = getattr(item, attr)
            if value is not None:
                result[attr] = value
        return result

    def _skin_json(self, item, accessor_index):
        result = self._common_json(item)
        result["joints"] = [self._node_index_by_key[key] for key in item.joints]
        if item.skeleton is not None:
            result["skeleton"] = self._node_index_by_key[item.skeleton]
        if item.name is not None:
            result["name"] = item.name
        if item.inverse_bind_matrices is not None:
            result["inverseBindMatrices"] = accessor_index
        return result

    def _image_json(self, item: ImageData, uri, buffer_view):
        result = self._common_json(item)
        if item.name is not None:
            result["name"] = item.name
        if item.mime_type is not None:
            result["mimeType"] = item.mime_type
        if uri is not None:
            result["uri"] = uri
        elif buffer_view is not None:
            result["bufferView"] = buffer_view
        elif item.uri is not None:
            result["uri"] = item.uri
        return result

    def _mesh_json(self, item, primitives):
        result = self._common_json(item)
        result["primitives"] = primitives
        if item.mesh_name is not None:
            result["name"] = item.mesh_name
        if item.weights is not None:
            result["weights"] = item.weights
        return result

    def _primitive_json(self, item, indices, attributes, targets):
        result = self._common_json(item)
        if indices is not None:
            result["indices"] = indices
        if item.material is not None:
            result["material"] = self._material_index_by_key[item.material]
        if item.mode is not None:
            result["mode"] = item.mode
        if attributes:
            result["attributes"] = attributes
        if targets:
            result["targets"] = targets
        return result

    def _scene_json(self, item):
        result = self._common_json(item)
        if item.children:
            result["nodes"] = [self._node_index_by_key[key] for key in item.children]
        if item.name is not None:
            result["name"] = item.name
        return result

    def _node_json(self, item):
        from compas.linalg.transformations import identity_matrix

        from .helpers import matrix_to_col_major_order

        result = self._common_json(item)
        if item.name is not None:
            result["name"] = item.name
        if item.children:
            result["children"] = [self._node_index_by_key[key] for key in item.children]
        if item.matrix and item.matrix != identity_matrix(4):
            result["matrix"] = matrix_to_col_major_order(item.matrix)
        else:
            for attr in ("translation", "rotation", "scale"):
                value = getattr(item, attr)
                if value:
                    result[attr] = value
        for attr, mapping, key in (("mesh_key", self._mesh_index_by_key, "mesh"), ("camera", self._camera_index_by_key, "camera"), ("skin", self._skin_index_by_key, "skin")):
            value = getattr(item, attr)
            if value is not None:
                result[key] = mapping[value]
        if item.weights is not None:
            result["weights"] = item.weights
        return result

    def _animation_sampler_json(self, item, input_accessor, output_accessor):
        result = self._common_json(item)
        result.update({"input": input_accessor, "output": output_accessor})
        if item.interpolation is not None:
            result["interpolation"] = item.interpolation
        return result

    def _animation_json(self, item, samplers):
        sampler_indices = item.get_sampler_index_by_key()
        result = self._common_json(item)
        result["samplers"] = samplers
        result["channels"] = []
        for channel in item.channels:
            target = self._common_json(channel.target)
            target["path"] = channel.target.path
            if channel.target.node is not None:
                target["node"] = self._node_index_by_key[channel.target.node]
            channel_json = self._common_json(channel)
            channel_json.update({"sampler": sampler_indices[channel.sampler], "target": target})
            result["channels"].append(channel_json)
        if item.name is not None:
            result["name"] = item.name
        return result

    def _extension_json(self, item):
        result = self._common_json(item)
        fields = {
            "transmission_factor": "transmissionFactor",
            "specular_factor": "specularFactor",
            "specular_color_factor": "specularColorFactor",
            "ior": "ior",
            "clearcoat_factor": "clearcoatFactor",
            "clearcoat_roughness_factor": "clearcoatRoughnessFactor",
            "offset": "offset",
            "rotation": "rotation",
            "scale": "scale",
            "tex_coord": "texCoord",
            "diffuse_factor": "diffuseFactor",
            "glossiness_factor": "glossinessFactor",
        }
        textures = {
            "transmission_texture": "transmissionTexture",
            "specular_texture": "specularTexture",
            "specular_color_texture": "specularColorTexture",
            "clearcoat_texture": "clearcoatTexture",
            "clearcoat_roughness_texture": "clearcoatRoughnessTexture",
            "clearcoat_normal_texture": "clearcoatNormalTexture",
            "diffuse_texture": "diffuseTexture",
            "specular_glossiness_texture": "specularGlossinessTexture",
        }
        for attr, key in fields.items():
            if hasattr(item, attr) and getattr(item, attr) is not None:
                result[key] = getattr(item, attr)
        for attr, key in textures.items():
            if hasattr(item, attr) and getattr(item, attr) is not None:
                result[key] = self._texture_info_json(getattr(item, attr))
        return result
