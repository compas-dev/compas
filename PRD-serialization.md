# PRD — Improving Serialization in COMPAS core

**Status:** Draft / exploratory
**Author:** (you)
**Date:** 2026-07-07
**Related code:** `compas.data` (JSON), `compas_pb` (protobuf), `arrow-opfs-poc` (zero-deserialization experiment)

---

## 1. Summary

COMPAS has two serialization modes today:

1. **JSON (default, in core)** — human-readable, universal, self-describing via a
   `dtype` string; implemented in `compas/data/`.
2. **Protobuf binary (opt-in, external)** — `compas_pb`, a plugin that maps
   registered COMPAS types to hand-written `.proto` messages for a smaller,
   faster wire format.

Both are **row/object-oriented and fully deserializing**: every element is parsed
into a Python object on load. For COMPAS's heavy payloads — meshes, pointclouds,
graphs with millions of numeric values — this is the dominant cost in time,
memory, and (for JSON) size. This PRD scopes the problem and lays out candidate
directions, informed by a separate Arrow experiment showing that the expensive
part to eliminate is **deserialization**, not the unavoidable I/O copy.

**This is a measurement-driven PRD.** No direction is adopted on argument alone;
each is decided against a benchmark suite built around two representative
large-data types — **`Mesh`** and **`Pointcloud`** — at varying sizes (§10).

## 2. Background — current state

### 2.1 JSON path (core)

- `Data.__jsondump__()` produces `{"dtype", "data", "guid", "name"}`;
  `__data__` is the per-class payload.
- `DataEncoder(json.JSONEncoder)` walks objects; `DataDecoder` reads `dtype`
  (e.g. `"compas.geometry/Point"`), imports the class, and calls
  `__from_data__(data)`.
- Entry points: `json_dump/dumps/load/loads`, plus zip-compressed
  `json_dumpz/loadz`. Options: `pretty`, `compact`, `minimal`.
- Numpy arrays are flattened with `.tolist()`.
- **Coupling to hashing:** `Data.sha256()` hashes `json_dumps(self)`. Object
  identity / change detection is therefore tied to the JSON text encoding.

**Strengths:** universal, debuggable, no schema/codegen, forward/backward
tolerant.
**Weaknesses:** large (text + repeated keys), slow to parse, float precision
depends on `repr`, no columnar/bulk representation for numeric arrays.

### 2.2 Protobuf path (`compas_pb`)

- Plugin discovered via `compas_pb.plugins` entry-point group; a
  `SerializerRegistry` maps `type → serializer` and `proto type_url → deserializer`,
  registered by `@pb_serializer` / `@pb_deserializer` decorators in
  `conversions.py`.
- Container schema (`message.proto`): `AnyData` is a `oneof` of a packed
  `google.protobuf.Any`, a `struct.Value` primitive, or a `FallbackData`
  wrapping a `DictData`. `MessageData` carries `data` + a `version` string.
- Hand-written `.proto` per type (`geometry.proto`, `datastructures.proto`) plus
  two conversion functions per type.
- **Fallback:** unregistered `Data` subclasses are serialized as their
  `__jsondump__()` dict inside a protobuf `DictData` — i.e. the JSON shape in a
  protobuf envelope, with little size/speed benefit and still routed through the
  JSON `DataDecoder` on the way back.

**Strengths:** compact binary, schema'd, cross-language potential (any protobuf
runtime, including JS/Wasm), versioned envelope.
**Weaknesses (as-is):**

- **Precision loss.** Geometry `.proto` stores coordinates as proto `float`
  (32-bit IEEE-754). COMPAS geometry is float64 → **lossy round-trip** for
  `x/y/z`, matrices, radii, angles. (To be quantified in the benchmark suite.)
- **Integer coercion.** The primitive path routes `int` through
  `struct.Value.number_value` (float64), reconstructing `int` only when the
  value `is_integer()`. Large/precise ints and the int/float distinction are at
  risk.
- **Coverage & maintenance.** Every new type needs a `.proto` message, codegen,
  and two hand-written functions. Anything not covered silently degrades to the
  JSON-shaped fallback.
- **Brittle versioning.** `version` compatibility is an exact string match that
  only emits a warning on mismatch.
- **Still fully deserializing.** Numeric bulk (vertices, faces) is decoded
  element-by-element into Python objects, same as JSON.

## 3. Motivation / problem statement

1. **Heavy numeric payloads are the real cost.** A `Mesh`/`Pointcloud` with N
   vertices pays O(N) Python-object construction on load in *both* modes.
   Neither format has a bulk/columnar representation for coordinate and index
   arrays.
2. **Browser & cross-language interop is growing** (web viewers, JS tooling).
   JSON is large and slow there; protobuf needs generated JS stubs and still
   deserializes fully.
3. **The binary path has correctness gaps** (float32, int coercion) that make it
   unsafe as a silent drop-in for JSON today.
4. **Two divergent code paths** with different type coverage, guarantees, and
   failure modes create a maintenance and correctness burden.

## 4. Findings from the Arrow zero-deserialization experiment

A sibling PoC (`arrow-opfs-poc`) moved large columnar data between Python and a
browser. The transferable conclusions:

- **The boundary copy is unavoidable and cheap; deserialization is the expensive
  part and *is* avoidable.** With a columnar layout (Arrow IPC), the receiver
  points typed vectors straight at the received buffer — **zero per-element
  parsing**. Proven both in Python (mmap; column buffer aliases the mapped file)
  and in the browser (`Float64Array` aliases the fetched `ArrayBuffer`).
- **True cross-sandbox "same physical pages" zero-copy is impossible** (browser
  has no mmap/shared memory with a foreign process). So the realistic target for
  COMPAS is **zero-deserialization**, not zero-copy.
- **Implication for COMPAS:** representing the numeric-heavy parts of data
  structures (vertex coordinates, face indices, pointclouds, transformation
  matrices) as contiguous typed buffers would let both Python and JS consumers
  skip per-element construction — the single biggest lever for large-model load
  time and memory. `Mesh` and `Pointcloud` are the natural first targets.

## 5. Goals / non-goals

### Goals

- Preserve JSON as the **default, universal** format; no regression for existing
  files or callers.
- Make a binary mode that is a **lossless, safe** alternative to JSON (fix
  float32/int issues) with a clear coverage-and-fallback contract.
- Introduce a path that avoids **per-element deserialization** for large numeric
  arrays (columnar/buffer-backed), usable from both Python and the browser.
- Unify the two modes behind a **single, stable serialization API** with format
  negotiation, so callers choose a format without divergent semantics.
- Keep object identity/versioning (`sha256`, schema) **format-independent**.
- **Decide every direction on measured evidence** from the §10 benchmark suite.

### Non-goals

- Replacing JSON as the default.
- True zero-copy across the browser boundary (physically impossible).
- Changing COMPAS object models / public class APIs.
- Solving streaming/partial loading in v1 (note it as future work).

## 6. Constraints & assumptions

- **IronPython/.NET is no longer a binding constraint.** The next major release
  of COMPAS drops IronPython support. This removes the historical barrier to
  numpy/pyarrow-based approaches and makes a columnar/typed-buffer path viable
  much closer to the core rather than only in an isolated extension.
- **Backward compatibility.** Existing `.json` files must keep loading; `dtype`
  resolution and `__from_data__` remain the contract.
- **Precision.** Geometry is float64; the default must be lossless and any binary
  mode must be lossless unless the caller explicitly opts into a compact/lossy
  profile.
- **Dependency weight, not availability, is the trade-off now.** pyarrow/numpy
  are acceptable where they earn their keep; keep them optional extras so a
  minimal core install stays light, but they are no longer disqualified by
  runtime.

## 7. Requirements

### Functional

- **F1** A single high-level API (e.g. `compas.data.dump/load`) that accepts a
  `format=` selector (`"json" | "protobuf" | "arrow" | ...`) and produces/reads a
  self-identifying container (magic bytes / MIME) so `load` can auto-detect.
- **F2** Round-trip **losslessness** for the default and the "safe binary"
  profile across all registered COMPAS types (property-based equality tests).
- **F3** A documented **fallback contract**: unregistered types degrade
  predictably (and loudly, not silently) with a single shared type-resolution
  mechanism (`dtype` ↔ proto type_url ↔ Arrow schema metadata).
- **F4** A **columnar/buffer profile** for numeric-heavy structures (`Mesh`
  vertices/faces, `Pointcloud`, transformation matrices) that reconstructs typed
  arrays without per-element Python object creation.
- **F5** Format-independent **object hashing/versioning** (decouple `sha256` from
  the JSON text; hash the canonical `__data__`/schema instead).

### Non-functional

- **N1** Binary/columnar load of a large `Mesh`/`Pointcloud` is materially faster
  and lower-memory than JSON (targets set from the §10 baseline, not guessed).
- **N2** Default JSON path performance and behavior unchanged (no regression).
- **N3** Heavy deps (pyarrow/protobuf) isolated as optional extras; minimal core
  install works without them.
- **N4** Clear, versioned wire format with a real compatibility policy (not an
  exact-string warning).

## 8. Candidate directions (to evaluate)

These are not mutually exclusive; the likely answer is a layered combination.
**Each is gated on §10 benchmark results.**

### Direction A — Harden & optionally accelerate the JSON path
- Decouple `sha256`/versioning from JSON text (canonical form).
- Optional fast encoder (e.g. `orjson`) behind the same API where available.
- *Pros:* low risk, immediate. *Cons:* doesn't address bulk-numeric cost.

### Direction B — Make `compas_pb` a safe, first-class binary mode
- Fix precision: `double` not `float`; explicit int handling.
- Reduce per-type boilerplate (generate `.proto`/conversions from `__data__`
  schema, or a reflective serializer) and define the fallback contract.
- Real version-compat policy.
- *Pros:* compact, cross-language, builds on existing work. *Cons:* still fully
  deserializing; codegen/runtime dep for consumers.

### Direction C — Columnar/buffer profile (Arrow-informed) for numeric bulk
- Encode `Mesh` vertex coords + face indices, `Pointcloud` points, and matrices
  as contiguous typed buffers (Arrow IPC or a minimal home-grown buffer format);
  keep metadata/attributes in a flexible container (JSON or protobuf).
- Reconstruct as numpy/typed arrays with **zero per-element parsing**; first-class
  JS consumption via Arrow-JS in the browser.
- *Pros:* attacks the real bottleneck; strong browser story; now viable close to
  core (no IronPython barrier). *Cons:* pyarrow dependency weight; hybrid layout
  (bulk buffers + heterogeneous attributes) needs design.

### Direction D — Unified serialization façade + format negotiation
- One API over all formats, self-identifying containers, shared type registry.
- Callers pick a format by capability/target (debugging → JSON; web/native bulk →
  Arrow/protobuf) without semantic divergence.
- *Pros:* consolidates guarantees and coverage. *Cons:* design/coordination
  effort; must not leak heavy deps into a minimal install.

**Straw-man recommendation for discussion:** D as the umbrella; A first (cheap,
de-risks hashing); B to make binary *safe*; C for the numeric-heavy win —
**pending the numbers**, since C is only worth its dependency weight if the
measured `Mesh`/`Pointcloud` load-time and memory gains are large.

## 9. Open questions

- Where does the **type registry** live so JSON, protobuf, and Arrow share one
  `dtype` ↔ schema mapping instead of three?
- Can `__data__` schemas be introspected to **auto-generate** binary encoders
  (kill the per-type boilerplate), or is hand-tuning required for the hot types?
- What is the **canonical form** for hashing that is stable across formats?
- Attribute dictionaries are heterogeneous — do they stay in a flexible container
  even in the columnar profile (hybrid layout)? (Likely yes.)
- Compatibility policy: semantic versioning of the wire format + capability flags
  vs. current exact-string check.
- Is **streaming / partial load** (huge models) in scope later, and does the
  chosen container support it?

## 10. Benchmarking — the decision instrument

Measurement is the backbone of this PRD, not an afterthought. Directions A–D are
accepted or rejected on these numbers.

### 10.1 Corpus

Two types stand in for "large data chunks", each at several sizes so we can see
scaling, not a single point:

| Subject      | Payload                                   | Sizes (approx.)                       |
|--------------|-------------------------------------------|---------------------------------------|
| `Mesh`       | vertices (float64 ×3) + faces (int index) | 10³, 10⁵, 10⁶, 5·10⁶ vertices         |
| `Pointcloud` | points (float64 ×3), optional attributes  | 10⁴, 10⁶, 10⁷, 5·10⁷ points           |

Include one variant **with per-element attributes** and one **without**, since
attribute dicts are the part a columnar layout cannot flatten — this exposes the
hybrid-layout cost.

Fixtures should be generated deterministically (seeded) so runs are comparable,
and reused across all formats.

### 10.2 Formats under test

- JSON (`compact`), and JSON+zip (`json_dumpz`) as the size baseline.
- `compas_pb` as-is (float32) and a `double` variant (to isolate the precision
  fix's size/speed cost).
- Columnar/Arrow prototype (Direction C).

### 10.3 Metrics (per subject × size × format)

- **Serialized size** (bytes on disk/wire); compression ratio vs JSON.
- **Serialize time** and **deserialize time** (wall clock, warm cache, multiple
  runs → median + spread).
- **Peak memory** during deserialize (e.g. `tracemalloc` / RSS sampling).
- **Round-trip fidelity:** exact equality of `__data__`; for lossy profiles,
  max/RMS coordinate error (this is where float32 gets quantified).
- **Browser** (Direction C): fetch→reconstruct time for the largest `Mesh`/
  `Pointcloud` in JS, and whether typed arrays alias the received buffer.

### 10.4 Reporting

A small, repeatable harness (script + fixtures) that emits a table/CSV per run as
a CI artifact. The PRD records the key conclusions and acceptance thresholds;
generated reports are not version-controlled. Targets for N1 are set **after**
the baseline exists, expressed as a required factor improvement over JSON for
the largest sizes.

## 11. Rough phasing

1. **Baseline & harness.** Build the §10 corpus (`Mesh`, `Pointcloud`) and
   benchmark harness; measure JSON and current `compas_pb`. Decouple `sha256`
   from JSON text. *Exit:* an archived results artifact and agreed N1 targets.
2. **Safe binary.** Fix `compas_pb` precision/int issues; measure the `double`
   cost; define fallback + version policy; expand/auto-generate coverage.
3. **Columnar prototype.** Arrow/buffer profile for `Mesh` + `Pointcloud`; Python
   and browser reconstruction benchmarked against the baseline. *Go/no-go on the
   measured gain vs pyarrow dependency weight.*
4. **Unified API.** Format negotiation + self-identifying containers + shared
   registry; docs and migration guidance.

---

*Appendix — key source references:* `compas/data/data.py`,
`compas/data/encoders.py`, `compas/data/json.py`;
`compas_pb/core.py`, `compas_pb/registry.py`, `compas_pb/conversions.py`,
`compas_pb/protobuf_defs/.../{message,geometry,datastructures}.proto`.
