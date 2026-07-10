"""Dump small, human-readable encoded artifacts for the three main (uncompressed) formats.

The benchmark runs on large fixtures; these are *tiny* fixtures whose whole encoded shape is
inspectable. For each subject we write, into ``results/samples/``:

* ``<subject>.json``          -- the JSON wire format (already text);
* ``<subject>.pb``            -- the raw protobuf bytes (binary);
* ``<subject>.pb.json``       -- the protobuf message rendered as JSON (``pb_dump_json``),
  i.e. the same bytes deserialized and re-serialized to JSON so the wire *structure* is
  readable (flat coordinate arrays, CSR faces, attribute columns, ...);
* ``<subject>.msgpack``       -- the raw MessagePack bytes (binary);
* ``<subject>.msgpack.json``  -- the decoded MessagePack tree as JSON (the row-oriented
  ``{dtype, data, ...}`` shape).

Comparing ``*.pb.json`` (schema'd / columnar) with ``*.msgpack.json`` (row-oriented tree)
shows how the two binary encodings differ in shape.
"""

import json
import os

import compas
from benchmarks.serialization import fixtures

# Small, fully-inspectable fixtures per subject.
SAMPLES = {
    "mesh": lambda seed: fixtures.make_mesh(4, with_attributes=True, seed=seed),
    "pointcloud": lambda seed: fixtures.make_pointcloud(4, seed=seed),
    "graph": lambda seed: fixtures.make_graph(4, seed=seed),
    "boxes": lambda seed: fixtures.make_primitives("box", 2, seed=seed),
}

_README = """# Encoded-format samples

Tiny, fully-inspectable fixtures encoded with the three main (uncompressed) formats, so you
can see the *shape* of each encoding. Regenerate with:

    python -m benchmarks.serialization.samples

Per subject:

| file | what it is |
|------|------------|
| `<subject>.json` | JSON wire format (text) |
| `<subject>.pb` | raw protobuf bytes |
| `<subject>.pb.json` | protobuf message deserialized + re-serialized to JSON (readable wire structure) |
| `<subject>.msgpack` | raw MessagePack bytes |
| `<subject>.msgpack.json` | decoded MessagePack tree as JSON (row-oriented `{dtype, data}`) |

`*.pb.json` shows the schema'd/columnar layout (flat vertex arrays, CSR faces, attribute
columns); `*.msgpack.json` shows the row-oriented dict tree.
"""


def _write_text(path, text):
    with open(path, "w") as f:
        f.write(text)


def _write_bytes(path, data):
    with open(path, "wb") as f:
        f.write(data)


def dump_samples(out_dir, seed=fixtures.DEFAULT_SEED):
    """Write encoded-format samples for each subject into ``out_dir``.

    Binary formats whose optional dependency is missing are skipped (only their readable
    JSON renderings are skipped too).

    Returns
    -------
    list[str]
        The files written.
    """
    os.makedirs(out_dir, exist_ok=True)
    written = []

    try:
        from compas_pb import pb_dump_bts
        from compas_pb import pb_dump_json
    except ImportError:
        pb_dump_bts = pb_dump_json = None

    try:
        import msgspec

        from benchmarks.serialization.formats import _msgpack_enc_hook
    except ImportError:
        msgspec = None

    for subject, factory in SAMPLES.items():
        # Fresh object per format: JSON dumping forces .guid, which would then appear in a
        # subsequent pb/msgpack dump of the same object. Independent objects show each
        # format's true shape (e.g. pb omitting auto-generated guids).
        json_path = os.path.join(out_dir, subject + ".json")
        _write_text(json_path, compas.json_dumps(factory(seed), pretty=True))
        written.append(json_path)

        if pb_dump_bts is not None:
            pb_path = os.path.join(out_dir, subject + ".pb")
            _write_bytes(pb_path, pb_dump_bts(factory(seed)))
            pbjson_path = os.path.join(out_dir, subject + ".pb.json")
            _write_text(pbjson_path, pb_dump_json(factory(seed)))
            written.extend([pb_path, pbjson_path])

        if msgspec is not None:
            blob = msgspec.msgpack.encode(factory(seed), enc_hook=_msgpack_enc_hook)
            mp_path = os.path.join(out_dir, subject + ".msgpack")
            _write_bytes(mp_path, blob)
            mpjson_path = os.path.join(out_dir, subject + ".msgpack.json")
            _write_text(mpjson_path, json.dumps(msgspec.msgpack.decode(blob), indent=2))
            written.extend([mp_path, mpjson_path])

    _write_text(os.path.join(out_dir, "README.md"), _README)
    return written


def main():
    here = os.path.dirname(__file__)
    out_dir = os.path.join(here, "results", "samples")
    written = dump_samples(out_dir)
    print("Wrote {} sample files to {}".format(len(written), out_dir))


if __name__ == "__main__":
    main()
