from collections.abc import Iterator
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Optional


class BaseGLTFDataClass:
    """Base behavior for structured glTF values with extras and extensions."""

    extras: Any
    extensions: Optional[dict[str, Any]]

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
    mag_filter: Optional[int] = None
    min_filter: Optional[int] = None
    wrap_s: Optional[int] = None
    wrap_t: Optional[int] = None
    name: Optional[str] = None
    extras: Any = None
    extensions: Optional[dict[str, Any]] = None


@dataclass
class TextureData(BaseGLTFDataClass):
    sampler: Optional[int] = None
    source: Optional[int] = None
    name: Optional[str] = None
    extras: Any = None
    extensions: Optional[dict[str, Any]] = None


@dataclass
class TextureInfoData(BaseGLTFDataClass):
    index: int
    tex_coord: Optional[int] = None
    extras: Any = None
    extensions: Optional[dict[str, Any]] = None


@dataclass
class OcclusionTextureInfoData(TextureInfoData):
    strength: Optional[float] = None


@dataclass
class NormalTextureInfoData(TextureInfoData):
    scale: Optional[float] = None


@dataclass
class PBRMetallicRoughnessData(BaseGLTFDataClass):
    base_color_factor: Optional[list[float]] = None
    base_color_texture: Optional[TextureInfoData] = None
    metallic_factor: Optional[float] = None
    roughness_factor: Optional[float] = None
    metallic_roughness_texture: Optional[TextureInfoData] = None
    extras: Any = None
    extensions: Optional[dict[str, Any]] = None


@dataclass
class MaterialData(BaseGLTFDataClass):
    name: Optional[str] = None
    extras: Any = None
    pbr_metallic_roughness: Optional[PBRMetallicRoughnessData] = None
    normal_texture: Optional[NormalTextureInfoData] = None
    occlusion_texture: Optional[OcclusionTextureInfoData] = None
    emissive_texture: Optional[TextureInfoData] = None
    emissive_factor: Optional[list[float]] = None
    alpha_mode: Optional[str] = None
    alpha_cutoff: Optional[float] = None
    double_sided: Optional[bool] = None
    extensions: Optional[dict[str, Any]] = None


@dataclass
class CameraData(BaseGLTFDataClass):
    type_: str
    orthographic: Optional[dict[str, Any]] = None
    perspective: Optional[dict[str, Any]] = None
    name: Optional[str] = None
    extras: Any = None
    extensions: Optional[dict[str, Any]] = None

    @property
    def type(self) -> str:
        return self.type_


@dataclass
class AnimationSamplerData(BaseGLTFDataClass):
    input_: list[Any]
    output: list[Any]
    interpolation: Optional[str] = None
    extras: Any = None
    extensions: Optional[dict[str, Any]] = None

    @property
    def input(self) -> list[Any]:
        return self.input_


@dataclass
class TargetData(BaseGLTFDataClass):
    path: str
    node: Optional[int] = None
    extras: Any = None
    extensions: Optional[dict[str, Any]] = None


@dataclass
class ChannelData(BaseGLTFDataClass):
    sampler: int
    target: TargetData
    extras: Any = None
    extensions: Optional[dict[str, Any]] = None


@dataclass
class AnimationData(BaseGLTFDataClass):
    channels: list[ChannelData]
    samplers_dict: dict[int, AnimationSamplerData]
    name: Optional[str] = None
    extras: Any = None
    extensions: Optional[dict[str, Any]] = None
    _sampler_index_by_key: Optional[dict[int, int]] = field(init=False, default=None, repr=False, compare=False)

    def get_sampler_index_by_key(self) -> dict[int, int]:
        self._sampler_index_by_key = {key: index for index, key in enumerate(self.samplers_dict)}
        return self._sampler_index_by_key


@dataclass
class SkinData(BaseGLTFDataClass):
    joints: list[int]
    inverse_bind_matrices: Optional[list[Any]] = None
    skeleton: Optional[int] = None
    name: Optional[str] = None
    extras: Any = None
    extensions: Optional[dict[str, Any]] = None


@dataclass
class ImageData(BaseGLTFDataClass):
    data: Optional[bytes] = None
    uri: Optional[str] = None
    mime_type: Optional[str] = None
    name: Optional[str] = None
    extras: Any = None
    extensions: Optional[dict[str, Any]] = None


@dataclass
class PrimitiveData(BaseGLTFDataClass):
    attributes: dict[str, list[Any]]
    indices: Optional[list[int]] = None
    material: Optional[int] = None
    mode: Optional[int] = None
    targets: Optional[list[dict[str, list[Any]]]] = None
    extras: Any = None
    extensions: Optional[dict[str, Any]] = None

    def __post_init__(self) -> None:
        if not self.attributes:
            self.attributes = {}
