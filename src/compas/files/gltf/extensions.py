from dataclasses import dataclass
from typing import Any
from typing import ClassVar
from typing import Optional

from .data_classes import BaseGLTFDataClass
from .data_classes import NormalTextureInfoData
from .data_classes import TextureInfoData


@dataclass
class KHR_materials_transmission(BaseGLTFDataClass):
    """Optical transmission material extension.

    References
    ----------
    - [KHR_materials_transmission](https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_materials_transmission)

    """

    key: ClassVar[str] = "KHR_materials_transmission"

    transmission_factor: Optional[float] = None
    transmission_texture: Optional[TextureInfoData] = None
    extensions: Optional[dict[str, Any]] = None
    extras: Any = None


@dataclass
class KHR_materials_specular(BaseGLTFDataClass):
    """Specular reflectance material extension.

    References
    ----------
    - [KHR_materials_specular](https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_materials_specular)

    """

    key: ClassVar[str] = "KHR_materials_specular"

    specular_factor: Optional[float] = None
    specular_texture: Optional[TextureInfoData] = None
    specular_color_factor: Optional[list[float]] = None
    specular_color_texture: Optional[TextureInfoData] = None
    extensions: Optional[dict[str, Any]] = None
    extras: Any = None


@dataclass
class KHR_materials_ior(BaseGLTFDataClass):
    """Index-of-refraction material extension.

    References
    ----------
    - [KHR_materials_ior](https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_materials_ior)

    """

    key: ClassVar[str] = "KHR_materials_ior"

    ior: Optional[float] = None
    extensions: Optional[dict[str, Any]] = None
    extras: Any = None


@dataclass
class KHR_materials_clearcoat(BaseGLTFDataClass):
    """Clearcoat material extension.

    References
    ----------
    - [KHR_materials_clearcoat](https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_materials_clearcoat)

    """

    key: ClassVar[str] = "KHR_materials_clearcoat"

    clearcoat_factor: Optional[float] = None
    clearcoat_texture: Optional[TextureInfoData] = None
    clearcoat_roughness_factor: Optional[float] = None
    clearcoat_roughness_texture: Optional[TextureInfoData] = None
    clearcoat_normal_texture: Optional[NormalTextureInfoData] = None
    extensions: Optional[dict[str, Any]] = None
    extras: Any = None


@dataclass
class KHR_Texture_Transform(BaseGLTFDataClass):
    """Texture-coordinate transformation extension.

    References
    ----------
    - [KHR_texture_transform](https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_texture_transform)

    """

    key: ClassVar[str] = "KHR_texture_transform"

    offset: Optional[list[float]] = None
    rotation: Optional[float] = None
    scale: Optional[list[float]] = None
    tex_coord: Optional[int] = None
    extensions: Optional[dict[str, Any]] = None
    extras: Any = None


@dataclass
class KHR_materials_pbrSpecularGlossiness(BaseGLTFDataClass):
    """Specular-glossiness material extension."""

    key: ClassVar[str] = "KHR_materials_pbrSpecularGlossiness"

    diffuse_factor: Optional[list[float]] = None
    diffuse_texture: Optional[TextureInfoData] = None
    specular_factor: Optional[list[float]] = None
    glossiness_factor: Optional[float] = None
    specular_glossiness_texture: Optional[TextureInfoData] = None
    extensions: Optional[dict[str, Any]] = None
    extras: Any = None

    def __post_init__(self) -> None:
        if self.diffuse_factor is None:
            self.diffuse_factor = [1.0, 1.0, 1.0, 1.0]
        if self.specular_factor is None:
            self.specular_factor = [1.0, 1.0, 1.0]
        if self.glossiness_factor is None:
            self.glossiness_factor = 1.0


SUPPORTED_EXTENSIONS = {
    KHR_materials_transmission.key: KHR_materials_transmission,
    KHR_materials_clearcoat.key: KHR_materials_clearcoat,
    KHR_Texture_Transform.key: KHR_Texture_Transform,
    KHR_materials_pbrSpecularGlossiness.key: KHR_materials_pbrSpecularGlossiness,
    KHR_materials_specular.key: KHR_materials_specular,
    KHR_materials_ior.key: KHR_materials_ior,
}
