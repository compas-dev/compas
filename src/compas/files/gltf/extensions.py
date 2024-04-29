from .data_classes import BaseGLTFDataClass
from .data_classes import NormalTextureInfoData
from .data_classes import TextureInfoData


def create_if_data(cls, data, attr):
    return cls.from_data(data.get(attr)) if attr in data and data[attr] is not None else None


class KHR_materials_transmission(BaseGLTFDataClass):
    """glTF extension that defines the optical transmission of a material.

    https://github.com/KhronosGroup/glTF/blob/master/extensions/2.0/Khronos/KHR_materials_transmission
    """

    key = "KHR_materials_transmission"

    def __init__(
        self,
        transmission_factor=None,
        transmission_texture=None,
        extensions=None,
        extras=None,
    ):
        super(KHR_materials_transmission, self).__init__(extras, extensions)
        self.transmission_factor = transmission_factor
        self.transmission_texture = transmission_texture

    def to_data(self, texture_index_by_key, **kwargs):
        dct = {}
        if self.transmission_factor is not None:
            dct["transmissionFactor"] = self.transmission_factor
        if self.transmission_texture is not None:
            dct["transmissionTexture"] = self.transmission_texture.to_data(texture_index_by_key)
        if self.extras is not None:
            dct["extras"] = self.extras
        if self.extensions is not None:
            dct["extensions"] = self.extensions_to_data()
        return dct

    @classmethod
    def from_data(cls, dct):
        if dct is None:
            return None
        return cls(
            transmission_factor=dct.get("transmissionFactor"),
            transmission_texture=create_if_data(TextureInfoData, dct, "transmissionTexture"),
            extensions=cls.extensions_from_data(dct.get("extensions")),
            extras=dct.get("extras"),
        )


class KHR_materials_specular(BaseGLTFDataClass):
    """glTF extension that defines the optical transmission of a material.

    https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_materials_specular
    """

    key = "KHR_materials_specular"

    def __init__(
        self,
        specular_factor=None,
        specular_texture=None,
        specular_color_factor=None,
        specular_color_texture=None,
        extensions=None,
        extras=None,
    ):
        super(KHR_materials_specular, self).__init__(extras, extensions)
        self.specular_factor = specular_factor
        self.specular_texture = specular_texture
        self.specular_color_factor = specular_color_factor
        self.specular_color_texture = specular_color_texture

    def to_data(self, texture_index_by_key, **kwargs):
        dct = {}
        if self.specular_factor is not None:
            dct["specularFactor"] = self.specular_factor
        if self.specular_texture is not None:
            dct["specularTexture"] = self.specular_texture.to_data(texture_index_by_key)
        if self.specular_color_factor is not None:
            dct["specularColorFactor"] = self.specular_color_factor
        if self.specular_color_texture is not None:
            dct["specularColorTexture"] = self.specular_color_texture.to_data(texture_index_by_key)
        if self.extras is not None:
            dct["extras"] = self.extras
        if self.extensions is not None:
            dct["extensions"] = self.extensions_to_data()
        return dct

    @classmethod
    def from_data(cls, dct):
        if dct is None:
            return None
        return cls(
            specular_factor=dct.get("specularFactor"),
            specular_texture=create_if_data(TextureInfoData, dct, "specularTexture"),
            specular_color_factor=dct.get("specularColorFactor"),
            specular_color_texture=create_if_data(TextureInfoData, dct, "specularColorTexture"),
            extensions=cls.extensions_from_data(dct.get("extensions")),
            extras=dct.get("extras"),
        )


class KHR_materials_ior(BaseGLTFDataClass):
    """glTF extension that defines the optical transmission of a material.

    https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_materials_ior
    """

    key = "KHR_materials_ior"

    def __init__(
        self,
        ior=None,
        extensions=None,
        extras=None,
    ):
        super(KHR_materials_ior, self).__init__(extras, extensions)
        self.ior = ior

    def to_data(self, texture_index_by_key, **kwargs):
        dct = {}
        if self.ior is not None:
            dct["ior"] = self.ior
        if self.extras is not None:
            dct["extras"] = self.extras
        if self.extensions is not None:
            dct["extensions"] = self.extensions_to_data()
        return dct

    @classmethod
    def from_data(cls, dct):
        if dct is None:
            return None
        return cls(
            ior=dct.get("ior"),
            extensions=cls.extensions_from_data(dct.get("extensions")),
            extras=dct.get("extras"),
        )


class KHR_materials_clearcoat(BaseGLTFDataClass):
    """glTF extension that defines the clearcoat material layer.

    https://github.com/KhronosGroup/glTF/blob/master/extensions/2.0/Khronos/KHR_materials_clearcoat
    """

    key = "KHR_materials_clearcoat"

    def __init__(
        self,
        clearcoat_factor=None,
        clearcoat_texture=None,
        clearcoat_roughness_factor=None,
        clearcoat_roughness_texture=None,
        clearcoat_normal_texture=None,
        extensions=None,
        extras=None,
    ):
        super(KHR_materials_clearcoat, self).__init__(extras, extensions)
        self.clearcoat_factor = clearcoat_factor
        self.clearcoat_texture = clearcoat_texture
        self.clearcoat_roughness_factor = clearcoat_roughness_factor
        self.clearcoat_roughness_texture = clearcoat_roughness_texture
        self.clearcoat_normal_texture = clearcoat_normal_texture

    def to_data(self, texture_index_by_key, **kwargs):
        dct = {}
        if self.clearcoat_factor is not None:
            dct["clearcoatFactor"] = self.clearcoat_factor
        if self.clearcoat_texture is not None:
            dct["clearcoatTexture"] = self.clearcoat_texture.to_data(texture_index_by_key)
        if self.clearcoat_roughness_factor is not None:
            dct["clearcoatRoughnessFactor"] = self.clearcoat_roughness_factor
        if self.clearcoat_roughness_texture is not None:
            dct["clearcoatRoughnessTexture"] = self.clearcoat_roughness_texture.to_data(texture_index_by_key)
        if self.clearcoat_normal_texture is not None:
            dct["clearcoatNormalTexture"] = self.clearcoat_normal_texture.to_data(texture_index_by_key)
        if self.extras is not None:
            dct["extras"] = self.extras
        if self.extensions is not None:
            dct["extensions"] = self.extensions_to_data()
        return dct

    @classmethod
    def from_data(cls, dct):
        if dct is None:
            return None
        return cls(
            clearcoat_factor=dct.get("clearcoatFactor"),
            clearcoat_texture=create_if_data(TextureInfoData, dct, "clearcoatTexture"),
            clearcoat_roughness_factor=dct.get("clearcoatRoughnessFactor"),
            clearcoat_roughness_texture=create_if_data(TextureInfoData, dct, "clearcoatRoughnessTexture"),
            clearcoat_normal_texture=create_if_data(NormalTextureInfoData, dct, "clearcoatNormalTexture"),
            extensions=cls.extensions_from_data(dct.get("extensions")),
            extras=dct.get("extras"),
        )


class KHR_Texture_Transform(BaseGLTFDataClass):
    """glTF extension that enables shifting and scaling UV coordinates on a per-texture basis.

    https://github.com/KhronosGroup/glTF/tree/master/extensions/2.0/Khronos/KHR_texture_transform
    """

    key = "KHR_texture_transform"

    def __init__(
        self,
        offset=None,
        rotation=None,
        scale=None,
        tex_coord=None,
        extensions=None,
        extras=None,
    ):
        super(KHR_Texture_Transform, self).__init__(extras, extensions)
        self.offset = offset  # or [0.0, 0.0]
        self.rotation = rotation  # or 0.
        self.scale = scale  # or [1., 1.]
        self.tex_coord = tex_coord

    def to_data(self, **kwargs):
        dct = {}
        if self.offset is not None:
            dct["offset"] = self.offset
        if self.rotation is not None:
            dct["rotation"] = self.rotation
        if self.scale is not None:
            dct["scale"] = self.scale
        if self.tex_coord is not None:
            dct["texCoord"] = self.tex_coord
        if self.extras is not None:
            dct["extras"] = self.extras
        if self.extensions is not None:
            dct["extensions"] = self.extensions_to_data()
        return dct

    @classmethod
    def from_data(cls, dct):
        if dct is None:
            return None
        return cls(
            offset=dct.get("offset"),
            rotation=dct.get("rotation"),
            scale=dct.get("scale"),
            tex_coord=dct.get("texCoord"),
            extensions=cls.extensions_from_data(dct.get("extensions")),
            extras=dct.get("extras"),
        )


class KHR_materials_pbrSpecularGlossiness(BaseGLTFDataClass):
    """glTF extension that defines the specular-glossiness material model from Physically-Based Rendering (PBR) methodology."""

    key = "KHR_materials_pbrSpecularGlossiness"

    def __init__(
        self,
        diffuse_factor=None,
        diffuse_texture=None,
        specular_factor=None,
        glossiness_factor=None,
        specular_glossiness_texture=None,
        extensions=None,
        extras=None,
    ):
        super(KHR_materials_pbrSpecularGlossiness, self).__init__(extras, extensions)
        self.diffuse_factor = diffuse_factor or [1.0, 1.0, 1.0, 1.0]
        self.diffuse_texture = diffuse_texture
        self.specular_factor = specular_factor or [1.0, 1.0, 1.0]
        self.glossiness_factor = glossiness_factor or 1.0
        self.specular_glossiness_texture = specular_glossiness_texture

    def to_data(self, texture_index_by_key, **kwargs):
        dct = {}
        if self.diffuse_factor is not None:
            dct["diffuseFactor"] = self.diffuse_factor
        if self.diffuse_texture is not None:
            dct["diffuseTexture"] = self.diffuse_texture.to_data(texture_index_by_key)
        if self.specular_factor is not None:
            dct["specularFactor"] = self.specular_factor
        if self.glossiness_factor is not None:
            dct["glossinessFactor"] = self.glossiness_factor
        if self.specular_glossiness_texture is not None:
            dct["specularGlossinessTexture"] = self.specular_glossiness_texture.to_data(texture_index_by_key)
        if self.extras is not None:
            dct["extras"] = self.extras
        if self.extensions is not None:
            dct["extensions"] = self.extensions_to_data()
        return dct

    @classmethod
    def from_data(cls, dct):
        if dct is None:
            return None
        return cls(
            diffuse_factor=dct.get("diffuseFactor"),
            diffuse_texture=create_if_data(TextureInfoData, dct, "diffuseTexture"),
            specular_factor=dct.get("specularFactor"),
            glossiness_factor=dct.get("glossinessFactor"),
            specular_glossiness_texture=create_if_data(TextureInfoData, dct, "specularGlossinessTexture"),
            extensions=cls.extensions_from_data(dct.get("extensions")),
            extras=dct.get("extras"),
        )


SUPPORTED_EXTENSIONS = {
    KHR_materials_transmission.key: KHR_materials_transmission,
    KHR_materials_clearcoat.key: KHR_materials_clearcoat,
    KHR_Texture_Transform.key: KHR_Texture_Transform,
    KHR_materials_pbrSpecularGlossiness.key: KHR_materials_pbrSpecularGlossiness,
    KHR_materials_specular.key: KHR_materials_specular,
    KHR_materials_ior.key: KHR_materials_ior,
}
