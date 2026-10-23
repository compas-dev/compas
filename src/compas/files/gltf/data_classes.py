from collections.abc import Iterator
from dataclasses import dataclass
from dataclasses import field
from typing import Any


class BaseGLTFDataClass:
    """Base behavior for structured glTF values with extras and extensions."""

    extras: Any
    extensions: dict[str, Any] | None

    def add_extension(self, extension: Any) -> None:
        """Attach a typed extension by its declared key."""
        if not self.extensions:
            self.extensions = {}
        self.extensions[extension.key] = extension

    def iter_data(self) -> Iterator["BaseGLTFDataClass"]:
        """Iterate recursively over this value and nested structured values.

        Yields
        ------
        BaseGLTFDataClass
            This value followed by nested values.

        """
        yield self
        for value in vars(self).values():
            yield from _iter_data(value)

    def extension_keys(self) -> set[str]:
        """Collect extension keys from this value hierarchy.

        Returns
        -------
        set[str]
            Referenced extension keys.

        """
        keys = set()
        for item in self.iter_data():
            if item.extensions:
                keys.update(item.extensions)
        return keys


def _iter_data(value: Any) -> Iterator[BaseGLTFDataClass]:
    if isinstance(value, BaseGLTFDataClass):
        yield from value.iter_data()
    elif isinstance(value, dict):
        for item in value.values():
            yield from _iter_data(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _iter_data(item)


@dataclass
class SamplerData(BaseGLTFDataClass):
    mag_filter: int | None = None
    min_filter: int | None = None
    wrap_s: int | None = None
    wrap_t: int | None = None
    name: str | None = None
    extras: Any = None
    extensions: dict[str, Any] | None = None


@dataclass
class TextureData(BaseGLTFDataClass):
    sampler: int | None = None
    source: int | None = None
    name: str | None = None
    extras: Any = None
    extensions: dict[str, Any] | None = None


@dataclass
class TextureInfoData(BaseGLTFDataClass):
    index: int
    tex_coord: int | None = None
    extras: Any = None
    extensions: dict[str, Any] | None = None


@dataclass
class OcclusionTextureInfoData(TextureInfoData):
    strength: float | None = None


@dataclass
class NormalTextureInfoData(TextureInfoData):
    scale: float | None = None


@dataclass
class PBRMetallicRoughnessData(BaseGLTFDataClass):
    base_color_factor: list[float] | None = None
    base_color_texture: TextureInfoData | None = None
    metallic_factor: float | None = None
    roughness_factor: float | None = None
    metallic_roughness_texture: TextureInfoData | None = None
    extras: Any = None
    extensions: dict[str, Any] | None = None


@dataclass
class MaterialData(BaseGLTFDataClass):
    name: str | None = None
    extras: Any = None
    pbr_metallic_roughness: PBRMetallicRoughnessData | None = None
    normal_texture: NormalTextureInfoData | None = None
    occlusion_texture: OcclusionTextureInfoData | None = None
    emissive_texture: TextureInfoData | None = None
    emissive_factor: list[float] | None = None
    alpha_mode: str | None = None
    alpha_cutoff: float | None = None
    double_sided: bool | None = None
    extensions: dict[str, Any] | None = None


@dataclass
class CameraData(BaseGLTFDataClass):
    type_: str
    orthographic: dict[str, Any] | None = None
    perspective: dict[str, Any] | None = None
    name: str | None = None
    extras: Any = None
    extensions: dict[str, Any] | None = None

    @property
    def type(self) -> str:
        return self.type_


@dataclass
class AnimationSamplerData(BaseGLTFDataClass):
    input_: list[Any]
    output: list[Any]
    interpolation: str | None = None
    extras: Any = None
    extensions: dict[str, Any] | None = None

    @property
    def input(self) -> list[Any]:
        return self.input_


@dataclass
class TargetData(BaseGLTFDataClass):
    path: str
    node: int | None = None
    extras: Any = None
    extensions: dict[str, Any] | None = None


@dataclass
class ChannelData(BaseGLTFDataClass):
    sampler: int
    target: TargetData
    extras: Any = None
    extensions: dict[str, Any] | None = None


@dataclass
class AnimationData(BaseGLTFDataClass):
    channels: list[ChannelData]
    samplers_dict: dict[int, AnimationSamplerData]
    name: str | None = None
    extras: Any = None
    extensions: dict[str, Any] | None = None
    _sampler_index_by_key: dict[int, int] | None = field(init=False, default=None, repr=False, compare=False)

    def get_sampler_index_by_key(self) -> dict[int, int]:
        self._sampler_index_by_key = {key: index for index, key in enumerate(self.samplers_dict)}
        return self._sampler_index_by_key


@dataclass
class SkinData(BaseGLTFDataClass):
    joints: list[int]
    inverse_bind_matrices: list[Any] | None = None
    skeleton: int | None = None
    name: str | None = None
    extras: Any = None
    extensions: dict[str, Any] | None = None


@dataclass
class ImageData(BaseGLTFDataClass):
    data: bytes | None = None
    uri: str | None = None
    mime_type: str | None = None
    name: str | None = None
    extras: Any = None
    extensions: dict[str, Any] | None = None


@dataclass
class PrimitiveData(BaseGLTFDataClass):
    attributes: dict[str, list[Any]]
    indices: list[int] | None = None
    material: int | None = None
    mode: int | None = None
    targets: list[dict[str, list[Any]]] | None = None
    extras: Any = None
    extensions: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if not self.attributes:
            self.attributes = {}
