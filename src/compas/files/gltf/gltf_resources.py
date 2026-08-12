"""Source and external-resource handling for glTF."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from typing import Protocol
from urllib.parse import urljoin

from compas import _iotools


class GLTFResourceLoader(Protocol):
    """Load a resource referenced by a glTF URI."""

    def read(self, uri: str) -> bytes:
        """Read a resource.

        Returns
        -------
        bytes
            Resource contents.

        """
        ...


@dataclass
class GLTFSource:
    """Complete primary source and optional external-resource loader."""

    data: bytes
    resource_loader: Optional[GLTFResourceLoader] = None


@dataclass
class PathResourceLoader:
    """Load resources relative to a filesystem directory."""

    directory: Path

    def read(self, uri: str) -> bytes:
        """Read a relative resource.

        Returns
        -------
        bytes
            Resource contents.

        """
        return _iotools.read_bytes(self.directory / uri)


@dataclass
class URLResourceLoader:
    """Load resources relative to a source URL."""

    base_url: str

    def read(self, uri: str) -> bytes:
        """Read a relative resource.

        Returns
        -------
        bytes
            Resource contents.

        """
        return _iotools.read_bytes(urljoin(self.base_url, uri))
