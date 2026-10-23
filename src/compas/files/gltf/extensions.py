from dataclasses import dataclass
from typing import Any
from typing import ClassVar

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

    transmission_factor: float | None = None
    transmission_texture: TextureInfoData | None = None
    extensions: dict[str, Any] | None = None
    extras: Any = None


@dataclass
class KHR_materials_specular(BaseGLTFDataClass):
    """Specular reflectance material extension.

    References
    ----------
    - [KHR_materials_specular](https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_materials_specular)

    """

    key: ClassVar[str] = "KHR_materials_specular"

    specular_factor: float | None = None
    specular_texture: TextureInfoData | None = None
    specular_color_factor: list[float] | None = None
    specular_color_texture: TextureInfoData | None = None
    extensions: dict[str, Any] | None = None
    extras: Any = None


@dataclass
class KHR_materials_ior(BaseGLTFDataClass):
    """Index-of-refraction material extension.

    References
    ----------
    - [KHR_materials_ior](https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_materials_ior)

    """

    key: ClassVar[str] = "KHR_materials_ior"

    ior: float | None = None
    extensions: dict[str, Any] | None = None
    extras: Any = None


@dataclass
class KHR_materials_clearcoat(BaseGLTFDataClass):
    """Clearcoat material extension.

    References
    ----------
    - [KHR_materials_clearcoat](https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_materials_clearcoat)

    """

    key: ClassVar[str] = "KHR_materials_clearcoat"

    clearcoat_factor: float | None = None
    clearcoat_texture: TextureInfoData | None = None
    clearcoat_roughness_factor: float | None = None
    clearcoat_roughness_texture: TextureInfoData | None = None
    clearcoat_normal_texture: NormalTextureInfoData | None = None
    extensions: dict[str, Any] | None = None
    extras: Any = None


@dataclass
class KHR_Texture_Transform(BaseGLTFDataClass):
    """Texture-coordinate transformation extension.

    References
    ----------
    - [KHR_texture_transform](https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_texture_transform)

    """

    key: ClassVar[str] = "KHR_texture_transform"

    offset: list[float] | None = None
    rotation: float | None = None
    scale: list[float] | None = None
    tex_coord: int | None = None
    extensions: dict[str, Any] | None = None
    extras: Any = None


@dataclass
class KHR_materials_pbrSpecularGlossiness(BaseGLTFDataClass):
    """Specular-glossiness material extension."""

    key: ClassVar[str] = "KHR_materials_pbrSpecularGlossiness"

    diffuse_factor: list[float] | None = None
    diffuse_texture: TextureInfoData | None = None
    specular_factor: list[float] | None = None
    glossiness_factor: float | None = None
    specular_glossiness_texture: TextureInfoData | None = None
    extensions: dict[str, Any] | None = None
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
