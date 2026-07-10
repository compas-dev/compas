"""Registry of serialization formats under test.

Each format is a :class:`Format` with ``dumps(obj) -> bytes`` and ``loads(bytes) -> obj``.
Phase 1 ships the two JSON baselines (compact text, and zip-compressed) that every
later format (safe protobuf, Arrow/columnar) is measured against. Register new
formats with :func:`register`; the runner picks them up automatically.

Formats whose optional dependency (protobuf, pyarrow, ...) is missing should register
with ``available=False`` and be skipped by the runner rather than crashing it.
"""

import io
import zipfile

import compas

_REGISTRY = {}


class Format(object):
    """A named, round-trippable serialization format.

    Parameters
    ----------
    name : str
        Unique identifier used in result rows.
    dumps : callable
        ``obj -> bytes``.
    loads : callable
        ``bytes -> obj``.
    available : bool, optional
        False if a required optional dependency is missing; the runner skips it.
    note : str, optional
        Short human-readable description of the profile (e.g. "lossy float32").
    """

    def __init__(self, name, dumps, loads, available=True, note=""):
        self.name = name
        self.dumps = dumps
        self.loads = loads
        self.available = available
        self.note = note


def register(fmt):
    _REGISTRY[fmt.name] = fmt
    return fmt


def formats():
    """Return the registered formats in registration order."""
    return list(_REGISTRY.values())


# ---------------------------------------------------------------------------
# JSON baselines (phase 1)
# ---------------------------------------------------------------------------

def _json_compact_dumps(obj):
    return compas.json_dumps(obj, compact=True).encode("utf-8")


def _json_compact_loads(blob):
    return compas.json_loads(blob.decode("utf-8"))


def _json_zip_dumps(obj):
    buffer = io.BytesIO()
    compas.json_dumpz(obj, buffer, compact=True)
    return buffer.getvalue()


def _json_zip_loads(blob):
    return compas.json_loadz(io.BytesIO(blob))


register(Format("json", _json_compact_dumps, _json_compact_loads, note="compact text, lossless"))
register(Format("json_zip", _json_zip_dumps, _json_zip_loads, note="zip-compressed json, size baseline"))


# ---------------------------------------------------------------------------
# Protobuf (compas_pb plugin, optional). Measured against the optimized branch:
# double precision + flat coordinate arrays + inline attribute maps.
# ---------------------------------------------------------------------------

try:
    import compas_pb  # noqa: F401

    _PB_AVAILABLE = True
except ImportError:
    _PB_AVAILABLE = False


def _pb_dumps(obj):
    from compas_pb import pb_dump_bts

    return pb_dump_bts(obj)


def _pb_loads(blob):
    from compas_pb import pb_load_bts

    return pb_load_bts(blob)


def _pb_zip_dumps(obj):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("content.pb", _pb_dumps(obj))
    return buffer.getvalue()


def _pb_zip_loads(blob):
    with zipfile.ZipFile(io.BytesIO(blob)) as zf:
        return _pb_loads(zf.read("content.pb"))


register(
    Format(
        "compas_pb",
        _pb_dumps,
        _pb_loads,
        available=_PB_AVAILABLE,
        note="protobuf binary, double + flat arrays (optimized)",
    )
)
register(
    Format(
        "compas_pb_zip",
        _pb_zip_dumps,
        _pb_zip_loads,
        available=_PB_AVAILABLE,
        note="protobuf binary, zip-compressed",
    )
)

try:
    import zstandard  # noqa: F401

    _ZSTD_AVAILABLE = _PB_AVAILABLE
except ImportError:
    _ZSTD_AVAILABLE = False


def _pb_zstd_dumps(obj):
    import zstandard

    return zstandard.ZstdCompressor(level=10).compress(_pb_dumps(obj))


def _pb_zstd_loads(blob):
    import zstandard

    return _pb_loads(zstandard.ZstdDecompressor().decompress(blob))


register(
    Format(
        "compas_pb_zstd",
        _pb_zstd_dumps,
        _pb_zstd_loads,
        available=_ZSTD_AVAILABLE,
        note="protobuf binary, zstandard-compressed",
    )
)


# ---------------------------------------------------------------------------
# MessagePack over the JSON-shape tree (the Kumiki-project approach, applied to COMPAS
# types via an msgspec enc_hook instead of Kumiki's own Serializable dataclasses).
# Binary but row-oriented / schemaless — a midpoint between JSON and the columnar compas_pb.
# ---------------------------------------------------------------------------

try:
    import msgspec  # noqa: F401

    _MSGPACK_AVAILABLE = True
except ImportError:
    _MSGPACK_AVAILABLE = False


def _msgpack_enc_hook(obj):
    # msgspec calls this for types it doesn't natively encode; COMPAS Data objects expose
    # their {dtype, data, guid, name} dict via __jsondump__, and nested Data recurse the same way.
    if hasattr(obj, "__jsondump__"):
        return obj.__jsondump__()
    raise NotImplementedError("Cannot msgpack-encode {}".format(type(obj)))


def _msgpack_reconstruct(node):
    from compas.data.encoders import cls_from_dtype

    if isinstance(node, dict):
        if "dtype" in node:
            data = _msgpack_reconstruct(node["data"])
            cls = cls_from_dtype(node["dtype"], node.get("inheritance"))
            return cls.__jsonload__(data, guid=node.get("guid"), name=node.get("name"))
        return {key: _msgpack_reconstruct(value) for key, value in node.items()}
    if isinstance(node, list):
        return [_msgpack_reconstruct(item) for item in node]
    return node


def _msgpack_dumps(obj):
    import msgspec

    return msgspec.msgpack.encode(obj, enc_hook=_msgpack_enc_hook)


def _msgpack_loads(blob):
    import msgspec

    return _msgpack_reconstruct(msgspec.msgpack.decode(blob))


def _msgpack_zstd_dumps(obj):
    import zstandard

    return zstandard.ZstdCompressor(level=10).compress(_msgpack_dumps(obj))


def _msgpack_zstd_loads(blob):
    import zstandard

    return _msgpack_loads(zstandard.ZstdDecompressor().decompress(blob))


register(
    Format(
        "compas_msgpack",
        _msgpack_dumps,
        _msgpack_loads,
        available=_MSGPACK_AVAILABLE,
        note="msgpack over the JSON-shape tree (Kumiki-style)",
    )
)
register(
    Format(
        "compas_msgpack_zstd",
        _msgpack_zstd_dumps,
        _msgpack_zstd_loads,
        available=_MSGPACK_AVAILABLE and _ZSTD_AVAILABLE,
        note="msgpack, zstandard-compressed",
    )
)
