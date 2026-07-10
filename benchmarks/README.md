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
| `graph`       | jittered grid, nodes (x,y,z) + edges       | per-node coords |
| `points`, `vectors`, `lines`, `frames`, `planes`, `boxes`, `spheres`, `circles` | a list of N primitives/shapes | — |
| `polylines`, `polygons`, `beziers`, `polyhedrons` | a list of N compound objects (each holds several points) | — |
| `transformations` | a list of N 4×4 matrices | — |

¹ The COMPAS `Pointcloud` type has no per-point attribute slot, so the "with per-element
attributes" case lives on `mesh_attrs`.

The primitive/shape subjects are **collections** (a Python `list` of N objects, a common
real-world payload — e.g. a list of frames as robot targets). The compound subjects
(polylines/polygons/beziers/polyhedrons) each hold several points, so they exercise
compas_pb's flat `repeated double` point arrays. This covers ~15 of compas_pb's ~31 native
geometry types; still uncovered: the conics (Arc/Ellipse/Parabola/Hyperbola), the remaining
shapes (Cylinder/Cone/Capsule/Torus), Quaternion, and the specific transformation subtypes
(Translation/Rotation/Scale/… — which have their own proto messages beyond the base matrix).

Fixtures are seeded ([`fixtures.py`](serialization/fixtures.py)) so runs are comparable and
reused across every format; the harness measures a list or a single `Data` object
transparently.

## Formats under test

Registered in [`formats.py`](serialization/formats.py):

- `json` — compact text (the default, lossless);
- `json_zip` — zip-compressed JSON (size baseline);
- `compas_pb` — protobuf binary via the `compas_pb` plugin (optional dep). We track the
  **optimized branch** (`benchmark/double-precision`): double precision, flat packed
  coordinate arrays, columnar vertex attributes. Skipped automatically if not installed.
  The harness still quantifies any residual error (`max_abs_error` / `rms_error`).
- `compas_pb_zip` — the above, zip-compressed (DEFLATE);
- `compas_pb_zstd` — the above, zstandard-compressed (optional `zstandard` dep; similar
  ratio to zip at ~3× faster compression).
- `compas_msgpack` — **MessagePack over the JSON-shape tree**, the approach from the Kumiki
  project (which uses `msgspec`), applied to COMPAS types via an `msgspec` `enc_hook` on
  `__jsondump__` (no `Mesh` subclass needed). Optional `msgspec` dep. Binary but
  row-oriented / schemaless — a midpoint between JSON and the columnar `compas_pb`.
- `compas_msgpack_zstd` — the above, zstandard-compressed.

An Arrow/columnar prototype registers the same way; the runner picks up any registered,
available format automatically and skips those whose optional dependency is missing
(`available=False`).

## Running

Every run writes a CSV **and** a self-contained, theme-aware HTML report next to it
(`results/<name>.html`) — open it in a browser for a readable, per-subject view with
grouped bars (round-trip time, wire size) and a full table. The CSV is the machine
record; the HTML is the human one. Each format serializes a **fresh** fixture, so one
format's dump (JSON accesses `.guid`) can't mutate what a later format encodes.

It also writes **encoded-format samples** to `results/samples/` — tiny, fully-inspectable
fixtures encoded with the three main formats, so you can see the *shape* of each encoding:
`<subject>.json`, `<subject>.pb` + `<subject>.pb.json` (the protobuf bytes rendered back to
JSON, showing the flat/columnar wire structure), and `<subject>.msgpack` +
`<subject>.msgpack.json` (the row-oriented tree). Regenerate standalone with
`python -m benchmarks.serialization.samples`; skip during a run with `--no-samples`.

```bash
# Quick baseline (small sizes, fast) — writes results/baseline_quick.{csv,html} + samples/
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
| mesh_attrs @10k, wire | 1.1 MB | 339 KB | 398 KB | **233 KB** |
| mesh_attrs @10k, round-trip | 67 ms | 97 ms | **52 ms** | 65 ms |
| pointcloud @100k, wire | 5.5 MB | 2.7 MB | 2.3 MB | **2.2 MB** |
| pointcloud @100k, round-trip | 343 ms | 551 ms | **186 ms** | 254 ms |

On the bulk-numeric types every format is **lossless** and `compas_pb` is smallest+fastest
(`_zip`/`_zstd` smallest on the wire, raw `compas_pb` fastest to load). Applied optimizations:

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
  `google.protobuf.Any` `type_url`. Helps Graph, fallback, and any nested container.
- **Columnar attributes (mesh vertices + graph nodes/edges)** — each attribute name is
  stored once with a packed value array (typed `double`/`int`/`bool`, generic fallback,
  dense columns skip indices), instead of a dict per element. `mesh_attrs@10k`:
  **1.1 MB → 398 KB** / **130 ms → 56 ms**; `graph@10k`: **931 KB → 360 KB** / **379 ms →
  87 ms** — both now smaller *and* faster to load than JSON.
- **guid/name only when explicitly set** — auto-generated guids and default names are no
  longer written (an object serializes its guid only if `_guid` was set). This removes
  ~40 bytes per object, including every `Point`/`Vector` nested in Lines/Frames/shapes.
  `boxes@10k` **3.4 MB → 1.6 MB** (now < JSON 2.7 MB). Contract change: auto guids no longer
  round-trip (they are session-local uuid4s); explicit guids still do.

### What the expanded corpus shows

The corpus also covers `graph` and collections of primitives/shapes, plus a third format:
`compas_msgpack` (MessagePack over the JSON-shape tree — the Kumiki approach). Findings:

- **`compas_pb` is the smallest on 11/12 subjects** (bulk-numeric *and* primitive/shape
  lists) after the guid fairness fix (see below). It is also **fastest to load on the
  bulk-numeric types** (mesh, mesh_attrs, pointcloud, graph). For **small-primitive lists**
  (points/vectors/lines/…) it is still smallest but *loads* slightly slower than JSON —
  each element goes through registry dispatch + message unpack. See Pending #1.
- **`compas_msgpack` sits between JSON and `compas_pb`**: binary and ~30–45% smaller than
  JSON with *very fast encode*, but row-oriented — so its **load speed is JSON-like** (no
  columnar/bulk win). A cheap JSON upgrade that does not fix deserialization.
- **`frames`/`planes` show `lossless=no` for every format including JSON** (~1e-16 error):
  `Frame`/`Plane` re-normalize their vectors on construction, so `normalize(normalize(v))`
  differs at the last ULP. A COMPAS geometry quirk the fidelity check surfaces, not a
  serialization defect.

> **Fairness fix.** Each format serializes a *fresh* fixture. Serializing to JSON accesses
> `.guid` (forcing it onto the object); when all formats shared one object, `compas_pb` then
> re-serialized those forced guids, overstating its size on primitive/shape lists by ~30%.
> With independent objects, `compas_pb`'s smallest-on-11/12 result stands.

The HTML report opens with a **three-pill toggle** (Uncompressed / Compressed / All) that
hides non-matching formats, re-normalizes the bars, and re-bases the summary — so you can
read *json vs compas_pb vs compas_msgpack* raw, or the compressed variants, in isolation.
The summary tiles report **median** ratios with their range across subjects (not a single
best), plus how many subjects `compas_pb` wins on size/speed.

To inspect the actual encodings, see `results/samples/` (per subject: `.json`, `.pb` +
`.pb.json`, `.msgpack` + `.msgpack.json`) — `*.pb.json` shows the columnar/flat wire shape,
`*.msgpack.json` the row-oriented tree.

The optimizations live on the `benchmark/double-precision` branch of the external
`compas_pb` repo (regenerate `_pb2` with the pinned protoc `invocations.PROTOC_VERSION`,
then `pip install -e .` into this `.venv`).

## Pending optimizations

1. **Batched primitive lists** — collections of small primitives load slightly slower than
   JSON because each element goes through registry lookup + message unpack. A batched/columnar
   encoding for homogeneous primitive lists (e.g. N points/frames as flat arrays) would close
   it, the same way the mesh/graph rewrites did.
2. **Mesh face/edge attributes** — still stored as `map<string, AnyData>` (cheap when empty,
   which is the common case). Could reuse the columnar layout when populated; low priority
   since the corpus doesn't exercise face/edge attributes.
3. **Compare against MsgSpec** — evaluate the Kumiki-project MsgSpec-based serialization as an
   additional format (next step).

## Status

Phase 1: baseline harness + JSON numbers, plus `Data.canonical_hash()` decoupling object
identity from the JSON text (`sha256()` is unchanged).
Phase 2 (in progress): `compas_pb` measured and **optimized** — double precision, flat
coordinate arrays, inline attribute maps, explicit int/float, CSR faces — now a fully
**lossless** binary mode, smaller and faster than JSON on numeric data. Still open: a real
version-compat policy and reducing per-type boilerplate.
N1 speed/memory targets for the columnar direction will be set from these baselines.
