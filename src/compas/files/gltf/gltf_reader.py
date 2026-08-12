"""Primary source acquisition for glTF files."""

from os import PathLike
from pathlib import Path
from typing import Optional

from compas import _iotools

from .gltf_resources import GLTFResourceLoader
from .gltf_resources import GLTFSource
from .gltf_resources import PathResourceLoader
from .gltf_resources import URLResourceLoader


class GLTFReader:
    """Read a primary glTF source without parsing it."""

    def __init__(self, source: _iotools.IOSource, resource_loader: Optional[GLTFResourceLoader] = None) -> None:
        self.source = source
        self.resource_loader = resource_loader

    def read(self) -> GLTFSource:
        """Read the primary source and configure relative resource loading.

        Returns
        -------
        GLTFSource
            Complete primary data and an optional resource loader.

        """
        loader = self.resource_loader
        if loader is None and isinstance(self.source, (str, PathLike)):
            if isinstance(self.source, str) and self.source.startswith(("http://", "https://")):
                loader = URLResourceLoader(self.source)
            else:
                loader = PathResourceLoader(Path(self.source).parent)
        return GLTFSource(_iotools.read_bytes(self.source), loader)
