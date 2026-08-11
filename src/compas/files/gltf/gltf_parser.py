"""Parser from raw glTF sources to semantic content."""

from typing import cast

from .data_classes import AnimationData
from .data_classes import AnimationSamplerData
from .data_classes import CameraData
from .data_classes import ChannelData
from .data_classes import ImageData
from .data_classes import MaterialData
from .data_classes import NormalTextureInfoData
from .data_classes import OcclusionTextureInfoData
from .data_classes import PBRMetallicRoughnessData
from .data_classes import PrimitiveData
from .data_classes import SamplerData
from .data_classes import SkinData
from .data_classes import TargetData
from .data_classes import TextureData
from .data_classes import TextureInfoData
from .extensions import SUPPORTED_EXTENSIONS
from .extensions import KHR_materials_clearcoat
from .extensions import KHR_materials_ior
from .extensions import KHR_materials_pbrSpecularGlossiness
from .extensions import KHR_materials_specular
from .extensions import KHR_materials_transmission
from .extensions import KHR_Texture_Transform
from .gltf_accessors import GLTFAccessorDecoder
from .gltf_accessors import data_uri_mime_type
from .gltf_container import parse_container
from .gltf_document import GLTFDocument
from .gltf_mesh import GLTFMesh
from .gltf_node import GLTFNode
from .gltf_resources import GLTFSource
from .gltf_scene import GLTFScene
from .gltf_types import AccessorData
from .gltf_types import GLTFJson


class GLTFParser:
    """Parse a complete primary source and its referenced resources."""

    def __init__(self, source: GLTFSource) -> None:
        self.source = source

    def parse(self) -> GLTFDocument:
        """Parse semantic glTF content.

        Returns
        -------
        GLTFDocument
            Parsed scenes and associated data.

        """
        _, document, binary_chunk = parse_container(self.source.data)
        decoder = GLTFAccessorDecoder(document, binary_chunk, self.source.resource_loader)
        accessors = decoder.decode_all()
        content = GLTFDocument()
        content.default_scene_key = document.get("scene")
        content.extras = document.get("extras")
        content.extensions = document.get("extensions")
        content.extensions_used = document.get("extensionsUsed")
        content.extensions_required = document.get("extensionsRequired")
        content.asset = document["asset"].copy()
        known = {
            "accessors", "animations", "asset", "bufferViews", "buffers", "cameras", "extensions",
            "extensionsRequired", "extensionsUsed", "extras", "images", "materials", "meshes", "nodes",
            "samplers", "scene", "scenes", "skins", "textures",
        }
        content.unknown = {key: value for key, value in document.items() if key not in known}
        content.images = {
            key: _image_data(image, decoder) for key, image in enumerate(document.get("images", []))
        }
        content.samplers = {
            key: _sampler_data(value)
            for key, value in enumerate(document.get("samplers", []))
        }
        content.textures = {
            key: _texture_data(value)
            for key, value in enumerate(document.get("textures", []))
        }
        content.materials = {
            key: _material_data(value)
            for key, value in enumerate(document.get("materials", []))
        }
        content.cameras = {
            key: _camera_data(value)
            for key, value in enumerate(document.get("cameras", []))
        }
        content.skins = {
            key: _skin_data(value, accessors[value["inverseBindMatrices"]] if "inverseBindMatrices" in value else None)
            for key, value in enumerate(document.get("skins", []))
        }
        content.animations = {
            key: _animation_data(value, accessors) for key, value in enumerate(document.get("animations", []))
        }
        for mesh in document.get("meshes", []):
            _add_mesh(mesh, accessors, content)
        for node in document.get("nodes", []):
            _add_node(node, content)
        for scene in document.get("scenes", []):
            _add_scene(scene, content)
        content.validate()
        content.update_node_transforms_and_positions()
        return content


def _image_data(image: GLTFJson, decoder: GLTFAccessorDecoder) -> ImageData:
    uri = image.get("uri")
    mime_type = image.get("mimeType") or data_uri_mime_type(uri)
    data = decoder.buffer_view_bytes(image["bufferView"]) if "bufferView" in image else None
    if uri:
        data = decoder.resource_bytes(uri)
    return ImageData(
        uri=image.get("uri"),
        mime_type=image.get("mimeType") or mime_type,
        name=image.get("name"),
        extras=image.get("extras"),
        extensions=_extensions_from_json(image.get("extensions")),
        data=data,
    )


def _animation_data(animation: GLTFJson, accessors: list[AccessorData]) -> AnimationData:
    samplers = {
        index: AnimationSamplerData(
            input_=accessors[value["input"]],
            output=accessors[value["output"]],
            interpolation=value.get("interpolation"),
            extras=value.get("extras"),
            extensions=_extensions_from_json(value.get("extensions")),
        )
        for index, value in enumerate(animation["samplers"])
    }
    channels = []
    for value in animation["channels"]:
        target = value["target"]
        channels.append(
            ChannelData(
                sampler=value["sampler"],
                target=TargetData(
                    path=target["path"],
                    node=target.get("node"),
                    extras=target.get("extras"),
                    extensions=_extensions_from_json(target.get("extensions")),
                ),
                extras=value.get("extras"),
                extensions=_extensions_from_json(value.get("extensions")),
            )
        )
    return AnimationData(
        channels=channels,
        samplers_dict=samplers,
        name=animation.get("name"),
        extras=animation.get("extras"),
        extensions=_extensions_from_json(animation.get("extensions")),
    )


def _add_mesh(mesh: GLTFJson, accessors: list[AccessorData], content: GLTFDocument) -> None:
    primitives = []
    for primitive in mesh["primitives"]:
        if "POSITION" not in primitive["attributes"]:
            continue
        attributes = {name: accessors[index] for name, index in primitive["attributes"].items()}
        indices = accessors[primitive["indices"]] if "indices" in primitive else list(range(len(attributes["POSITION"])))
        targets = [
            {name: accessors[index] for name, index in target.items()} for target in primitive.get("targets", [])
        ]
        primitives.append(
            PrimitiveData(
                attributes=attributes,
                indices=indices,
                material=primitive.get("material"),
                mode=primitive.get("mode"),
                targets=targets,
                extras=primitive.get("extras"),
                extensions=_extensions_from_json(primitive.get("extensions")),
            )
        )
    GLTFMesh(
        primitive_data_list=primitives,
        context=content,
        mesh_name=mesh.get("name"),
        weights=mesh.get("weights"),
        extras=mesh.get("extras"),
        extensions=_extensions_from_json(mesh.get("extensions")),
    )


def _add_node(node: GLTFJson, content: GLTFDocument) -> None:
    result = GLTFNode(content, node.get("name"), node.get("extras"), _extensions_from_json(node.get("extensions")))
    # Child nodes may occur later in the source array and therefore do not yet
    # exist in the semantic document during this construction pass.
    result.children._values = node.get("children", [])
    if "matrix" in node:
        from .helpers import get_matrix_from_col_major_list

        result.matrix = get_matrix_from_col_major_list(node["matrix"])
    else:
        result.translation = node.get("translation")
        result.rotation = node.get("rotation")
        result.scale = node.get("scale")
    result.mesh_key = node.get("mesh")
    result.weights = node.get("weights")
    result.camera = node.get("camera")
    result.skin = node.get("skin")


def _add_scene(scene: GLTFJson, content: GLTFDocument) -> None:
    GLTFScene(
        context=content,
        children=scene.get("nodes"),
        name=scene.get("name"),
        extras=scene.get("extras"),
        extensions=_extensions_from_json(scene.get("extensions")),
    )


def _sampler_data(data: GLTFJson) -> SamplerData:
    return SamplerData(
        data.get("magFilter"),
        data.get("minFilter"),
        data.get("wrapS"),
        data.get("wrapT"),
        data.get("name"),
        data.get("extras"),
        _extensions_from_json(data.get("extensions")),
    )


def _texture_data(data: GLTFJson) -> TextureData:
    return TextureData(
        data.get("sampler"),
        data.get("source"),
        data.get("name"),
        data.get("extras"),
        _extensions_from_json(data.get("extensions")),
    )


def _texture_info(data, cls=TextureInfoData):
    if data is None:
        return None
    kwargs = {
        "index": data["index"], "tex_coord": data.get("texCoord"), "extras": data.get("extras"),
        "extensions": _extensions_from_json(data.get("extensions")),
    }
    if cls is NormalTextureInfoData:
        kwargs["scale"] = data.get("scale")
    if cls is OcclusionTextureInfoData:
        kwargs["strength"] = data.get("strength")
    return cls(**kwargs)


def _material_data(data: GLTFJson) -> MaterialData:
    pbr = data.get("pbrMetallicRoughness")
    pbr_data = None
    if pbr is not None:
        pbr_data = PBRMetallicRoughnessData(
            base_color_factor=pbr.get("baseColorFactor"),
            base_color_texture=_texture_info(pbr.get("baseColorTexture")),
            metallic_factor=pbr.get("metallicFactor"), roughness_factor=pbr.get("roughnessFactor"),
            metallic_roughness_texture=_texture_info(pbr.get("metallicRoughnessTexture")),
            extras=pbr.get("extras"), extensions=_extensions_from_json(pbr.get("extensions")),
        )
    return MaterialData(
        name=data.get("name"), extras=data.get("extras"), pbr_metallic_roughness=pbr_data,
        normal_texture=cast(NormalTextureInfoData, _texture_info(data.get("normalTexture"), NormalTextureInfoData)),
        occlusion_texture=cast(
            OcclusionTextureInfoData,
            _texture_info(data.get("occlusionTexture"), OcclusionTextureInfoData),
        ),
        emissive_texture=_texture_info(data.get("emissiveTexture")), emissive_factor=data.get("emissiveFactor"),
        alpha_mode=data.get("alphaMode"), alpha_cutoff=data.get("alphaCutoff"), double_sided=data.get("doubleSided"),
        extensions=_extensions_from_json(data.get("extensions")),
    )


def _camera_data(data: GLTFJson) -> CameraData:
    return CameraData(data["type"], data.get("orthographic"), data.get("perspective"), data.get("name"), data.get("extras"), _extensions_from_json(data.get("extensions")))


def _skin_data(data: GLTFJson, inverse_bind_matrices) -> SkinData:
    return SkinData(data["joints"], inverse_bind_matrices, data.get("skeleton"), data.get("name"), data.get("extras"), _extensions_from_json(data.get("extensions")))


def _extensions_from_json(data):
    if not data:
        return None
    result = {}
    for key, value in data.items():
        cls = SUPPORTED_EXTENSIONS.get(key)
        result[key] = _extension_from_json(cls, value) if cls else value
    return result


def _extension_from_json(cls, data):
    common = {"extras": data.get("extras"), "extensions": _extensions_from_json(data.get("extensions"))}
    if cls is KHR_materials_transmission:
        return cls(data.get("transmissionFactor"), _texture_info(data.get("transmissionTexture")), **common)
    if cls is KHR_materials_specular:
        return cls(
            data.get("specularFactor"),
            _texture_info(data.get("specularTexture")),
            data.get("specularColorFactor"),
            _texture_info(data.get("specularColorTexture")),
            **common,
        )
    if cls is KHR_materials_ior:
        return cls(data.get("ior"), **common)
    if cls is KHR_materials_clearcoat:
        return cls(
            data.get("clearcoatFactor"),
            _texture_info(data.get("clearcoatTexture")),
            data.get("clearcoatRoughnessFactor"),
            _texture_info(data.get("clearcoatRoughnessTexture")),
            cast(
                NormalTextureInfoData,
                _texture_info(data.get("clearcoatNormalTexture"), NormalTextureInfoData),
            ),
            **common,
        )
    if cls is KHR_Texture_Transform:
        return cls(data.get("offset"), data.get("rotation"), data.get("scale"), data.get("texCoord"), **common)
    if cls is KHR_materials_pbrSpecularGlossiness:
        return cls(
            data.get("diffuseFactor"),
            _texture_info(data.get("diffuseTexture")),
            data.get("specularFactor"),
            data.get("glossinessFactor"),
            _texture_info(data.get("specularGlossinessTexture")),
            **common,
        )
    return data
