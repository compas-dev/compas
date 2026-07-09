# Serialization benchmarks

The measurement instrument for [`PRD-serialization.md`](../PRD-serialization.md). Directions A–D
in the PRD are accepted or rejected on the numbers this harness produces, not on argument.

## What it measures (PRD §10)

For each **subject × size × format**:

- **serialized size** (bytes on the wire) and compression ratio vs JSON;
- **serialize** and **deserialize** time (median + spread over `--repeat` runs), the
  **round-trip total**, and **throughput** (MB of wire per second) so formats are
  comparable across sizes — this is how the impact of zipping / protobuf / Arrow gets read;
- **peak memory** during deserialize (`tracemalloc`);
- **round-trip fidelity**: exact equality of `__data__` and of the format-independent
  `canonical_hash` — where a lossy profile (e.g. protobuf float32) will show up.

## Subjects (PRD §10.1)

| Subject       | Payload                                    | Attributes |
|---------------|--------------------------------------------|------------|
| `mesh`        | jittered grid, float64 verts + int faces   | none |
| `mesh_attrs`  | same + a per-vertex float                  | per-element (hybrid-layout cost) |
| `pointcloud`  | N float64 points                           | none¹ |

¹ The COMPAS `Pointcloud` type has no per-point attribute slot, so the "with per-element
attributes" case lives on `mesh_attrs`.

Fixtures are seeded ([`fixtures.py`](serialization/fixtures.py)) so runs are comparable and
reused across every format.

## Formats under test

Registered in [`formats.py`](serialization/formats.py):

- `json` — compact text (the default, lossless);
- `json_zip` — zip-compressed JSON (size baseline);
- `compas_pb` — protobuf binary via the `compas_pb` plugin (optional dep). We track the
  **optimized branch** (`benchmark/double-precision`): double precision, flat packed
  coordinate arrays, and inline attribute maps. Skipped automatically if not installed.
  The harness still quantifies any residual error (`max_abs_error` / `rms_error`).

An Arrow/columnar prototype registers the same way; the runner picks up any registered,
available format automatically and skips those whose optional dependency is missing
(`available=False`).

## Running

Every run writes a CSV **and** a self-contained, theme-aware HTML report next to it
(`results/<name>.html`) — open it in a browser for a readable, per-subject view with
grouped bars (round-trip time, wire size) and a full table. The CSV is the machine
record; the HTML is the human one.

```bash
# Quick baseline (small sizes, fast) — writes results/baseline_quick.{csv,html}
python -m benchmarks.serialization.run

# Full PRD corpus (large; slow, memory-hungry)
python -m benchmarks.serialization.run --preset full --out benchmarks/serialization/results/baseline_full.csv

# Subset
python -m benchmarks.serialization.run --subjects mesh pointcloud --formats json
```

Run from the repository root so `benchmarks` imports as a package. Requires a working
`numpy` (COMPAS geometry imports it at load time).

## Results

`results/baseline_quick.{csv,html}` — JSON, JSON+zip, and the **optimized** `compas_pb`
(raw and zip-compressed) on the quick corpus. The HTML report opens with an **executive
summary** (headline stat tiles + a per-subject winners table) so the conclusion is visible
before any detail. Headline: with double precision + flat coordinate arrays + inline
attribute maps, `compas_pb` goes from *larger and slower than JSON* (as shipped) to the
**smallest and fastest lossless** option on numeric-heavy data:

| subject (largest size) | JSON | json_zip | compas_pb | compas_pb_zip |
|---|---|---|---|---|
| mesh @10k, wire | 864 KB | 238 KB | 320 KB | **158 KB** |
| mesh @10k, round-trip | 66 ms | 87 ms | **50 ms** | 58 ms |
| mesh_attrs @10k, wire | 1.1 MB | 339 KB | 651 KB | **273 KB** |
| pointcloud @100k, wire | 5.5 MB | 2.7 MB | 2.3 MB | **2.2 MB** |
| pointcloud @100k, round-trip | 343 ms | 551 ms | **186 ms** | 254 ms |

All four formats are now **lossless on every subject**. `compas_pb_zip` is smallest;
raw `compas_pb` is fastest (no compress step). Applied optimizations:

- **Precision fixed** (`float → double`): coordinate error is **0** everywhere.
- **Flat coordinate arrays** replaced a `PointData` message *per vertex/point* (each of
  which carried a per-point UUID + name) with packed `repeated double` triplets — the
  dominant size/speed win, for Mesh, Pointcloud, Polyline, Polygon, Bezier, Polyhedron.
- **Inline `map<string, AnyData>` attributes** (Mesh, Graph) dropped the `DictData`
  wrapper and skip empty/default entries.
- **Int/float distinction preserved** — `AnyData` gained explicit `int64`/`double` arms
  instead of routing numbers through `google.protobuf.Value`, so `0.0` no longer comes
  back as `0`. This makes `Mesh`/`Graph` fully lossless (canonical hash matches).
- **CSR face storage** — faces are a flat packed `face_vertices` index array + a
  `face_sizes` length array, instead of one `FaceList` message per face.
- **No `Any` wrapper on plain dicts/lists** — `AnyData` gained explicit `dict_value` /
  `list_value` arms, so every nested dict/list no longer carries a ~44-byte
  `google.protobuf.Any` `type_url`. This cut `mesh_attrs@10k` from **1.1 MB → 651 KB**
  (now below JSON) and helps Graph, fallback, and any nested container.

The optimizations live on the `benchmark/double-precision` branch of the external
`compas_pb` repo (regenerate `_pb2` with the pinned protoc `invocations.PROTOC_VERSION`,
then `pip install -e .` into this `.venv`).

## Pending optimizations

1. **Columnar vertex attributes** — `mesh_attrs` is now small but still slower than JSON to
   *load* (each vertex rebuilds a `DictData` and repeats the attribute-name string). Storing
   attributes column-wise (name once + a packed value array aligned to vertices) is the
   Phase-3 columnar layout; it should make attribute-heavy meshes beat JSON on both axes.
2. **Standalone `PointData` guid/name** — still serialized on every standalone Point/Line/
   Frame. Omitting them (design decision: binary parity with JSON vs compactness) would
   shrink primitive-heavy payloads.
3. **Graph flat coordinates** — Graph nodes still carry coordinates inside per-node
   `AnyData` dicts. A flat node-key + coordinate layout is the analog of the Mesh rewrite,
   but node keys are arbitrary so it needs a small schema redesign.

## Status

Phase 1: baseline harness + JSON numbers, plus `Data.canonical_hash()` decoupling object
identity from the JSON text (`sha256()` is unchanged).
Phase 2 (in progress): `compas_pb` measured and **optimized** — double precision, flat
coordinate arrays, inline attribute maps, explicit int/float, CSR faces — now a fully
**lossless** binary mode, smaller and faster than JSON on numeric data. Still open: a real
version-compat policy and reducing per-type boilerplate.
N1 speed/memory targets for the columnar direction will be set from these baselines.
