"""Registry of serialization formats under test.

Each format is a :class:`Format` with ``dumps(obj) -> bytes`` and ``loads(bytes) -> obj``.
Phase 1 ships the two JSON baselines (compact text, and zip-compressed) that every
later format (safe protobuf, Arrow/columnar) is measured against. Register new
formats with :func:`register`; the runner picks them up automatically.

Formats whose optional dependency (protobuf, pyarrow, ...) is missing should register
with ``available=False`` and be skipped by the runner rather than crashing it.
"""

import io

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
# Protobuf (compas_pb plugin, optional). float32 wire -> lossy for float64 geometry.
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


register(
    Format(
        "compas_pb",
        _pb_dumps,
        _pb_loads,
        available=_PB_AVAILABLE,
        note="protobuf binary, float32 (lossy)",
    )
)
