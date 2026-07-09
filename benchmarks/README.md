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
- `compas_pb` — protobuf binary via the [`compas_pb`](https://pypi.org/project/compas_pb/)
  plugin (optional dep; `pip install compas_pb`). Skipped automatically if not installed.
  Currently **float32 → lossy** for float64 geometry; the harness quantifies the error
  (see `max_abs_error` / `rms_error`).

Later phases register a `compas_pb` `double` variant and an Arrow/columnar prototype the same
way; the runner picks up any registered, available format automatically and skips those whose
optional dependency is missing (`available=False`).

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

- `results/baseline_quick.{csv,html}` — JSON, JSON+zip, and `compas_pb` (**as shipped**,
  float32) on the quick corpus. Findings: `json_zip` is 2–3.6× smaller than compact JSON
  for ~1.5–1.8× slower round-trips; `compas_pb` as-is is **larger and slower than JSON**
  and **lossy** (float32), with the error scaling with coordinate magnitude
  (mesh ~1.5e-08, pointcloud ~3.8e-06).
- `results/pb_precision_compare.{csv,html}` — **Phase 2 precision probe**: `compas_pb`
  float32 vs a `double` build. Double drives coordinate error to **0** and makes
  `Pointcloud` fully lossless, for ~+6% (mesh) / ~+19% (pointcloud) wire size. `Mesh`
  stays non-lossless even with double — but now purely from **int/float coercion** of
  zero-valued `default_vertex_attributes` (magnitude error 0), a defect separate from
  precision (PRD §2.2 "Integer coercion").

### Reproducing the `double` variant

The `double` numbers come from an experimental branch of the external `compas_pb` repo,
not the shipped wheel:

```bash
# in the compas_pb checkout, on a branch:
#   flip float -> double in protobuf_defs/compas_pb/generated/geometry.proto (PointData etc.)
#   regenerate with the pinned protoc (invocations.PROTOC_VERSION, 31.1):
protoc --proto_path=src/compas_pb/protobuf_defs \
       --python_out=src --pyi_out=src \
       src/compas_pb/protobuf_defs/compas_pb/generated/geometry.proto
pip install -e .            # into the compas .venv
python -m benchmarks.serialization.run --formats json compas_pb --out benchmarks/serialization/results/pb_double.csv
pip install --force-reinstall --no-deps compas_pb   # restore the as-shipped float32 build
```

## Status

Phase 1: baseline harness + JSON numbers, plus `Data.canonical_hash()` decoupling object
identity from the JSON text (`sha256()` is unchanged).
Phase 2 (in progress): `compas_pb` measured; precision fix (double) quantified above. Still
open: the int-coercion fix, a real version-compat policy, and reducing per-type boilerplate.
N1 speed/memory targets for the columnar direction will be set from these baselines.
