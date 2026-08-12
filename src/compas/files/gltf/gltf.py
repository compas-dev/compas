"""Convenience functions for reading and writing glTF documents."""

from os import PathLike
from pathlib import Path
from typing import Optional
from typing import cast

from compas import _iotools

from .gltf_document import GLTFDocument
from .gltf_encoder import GLTFEncoder
from .gltf_parser import GLTFParser
from .gltf_reader import GLTFReader
from .gltf_resources import GLTFResourceLoader
from .gltf_types import GLTFFormat
from .gltf_writer import GLTFWriter


def read_gltf(
    source: _iotools.IOSource,
    resource_loader: Optional[GLTFResourceLoader] = None,
) -> GLTFDocument:
    """Read a glTF document.

    Parameters
    ----------
    source
        Path, URL, text stream, or binary stream.
    resource_loader
        Optional loader for external buffers and images.

    Returns
    -------
    GLTFDocument
        Parsed semantic document.

    """
    return GLTFParser(GLTFReader(source, resource_loader).read()).parse()


def write_gltf(
    target: _iotools.IOTarget,
    document: GLTFDocument,
    format: Optional[GLTFFormat] = None,
    embed_data: bool = False,
) -> None:
    """Encode and write a glTF document.

    Parameters
    ----------
    target
        Path or writable stream.
    document
        Semantic glTF document.
    format
        Explicit format required for stream targets.
    embed_data
        Embed binary data in JSON glTF output.

    """
    if format is None:
        if not isinstance(target, (str, PathLike)):
            raise ValueError("A glTF format is required for stream targets.")
        suffix = Path(target).suffix.lower()
        if suffix not in (".gltf", ".glb"):
            raise ValueError("The target must use a .gltf or .glb extension.")
        format = cast(GLTFFormat, suffix[1:])
    filename = Path(target).stem if isinstance(target, (str, PathLike)) else "model"
    payload = GLTFEncoder(format, embed_data, filename).encode(document)
    GLTFWriter(target).write(payload)
