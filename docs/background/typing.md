# Type Annotations

COMPAS type annotations describe the values that an API can consume. They help
static type checkers find mistakes, but they do not add runtime validation or
conversion.

## Numeric input families

The public aliases in `compas.typing` cover the numeric families used by COMPAS APIs:

- `RealInput` accepts the built-in `int` and `float` families and NumPy integer
  and floating scalar families.
- `IntegralInput` accepts the built-in `int` family and the NumPy integer scalar
  family.
- `NumericArray`, `FloatingArray`, and `IntegerArray` describe NumPy arrays by
  scalar family. `Float64Array` and `Int32Array` describe the two cases where an
  exact dtype is part of the contract.
- `FloatSequenceLike` describes a neutral indexed numeric sequence, such as a
  quaternion. `PointLike` and `VectorLike` accept the same structure but state
  whether an argument is positional or directional.
- `PointsLike`, `IndicesLike`, `PointGroupsLike`, and `IndexGroupsLike` combine
  structural Python inputs with the corresponding NumPy array families.
- `VerticesFaces` is the single neutral structural `(vertices, faces)` tuple.
  It can describe an input or result without requiring a `Mesh`,
  `PolygonalSurface`, or `Tessellation` object. Whether faces must be triangles
  is an operation contract, not part of the alias name.

These aliases intentionally support duck typing. APIs should operate on the
capabilities they need instead of requiring a particular concrete container or
performing nominal type checks. Conversion belongs at an explicit boundary only
when an implementation requires a specific representation.

Python's `bool` is a subclass of `int`, so static checkers include it in the
built-in integer family. NumPy's `bool_` is not a NumPy integer and is excluded.
An API that cannot meaningfully accept boolean values should reject them at its
own runtime boundary; the shared aliases do not add a blanket runtime check.

Every member of `RealInput` supports `float(value)`. A coordinate element can
therefore be handed directly to an existing scalar setter that already
normalizes with `float(...)`, such as `point.x = point_like[0]`. This does not
authorize additional conversions in numerical functions: values continue to
participate in direct arithmetic where that is the established behavior.

`CoordinateProtocol` includes length, iteration, integer indexing, and slicing.
A slice returns a neutral `Sequence`, because a two-component slice is not
necessarily a point or vector. `Point` and `Vector` explicitly implement this
protocol. `CoordinateProtocol` and `PointsProtocol` are runtime-checkable only
for existing structural equality behavior; the `Like` aliases are static
unions and must not be used as runtime validation gates.

## Static types and runtime invariants

An annotation cannot express every runtime requirement. For example, a numeric
array annotation does not specify that a coordinate has exactly three values,
that a collection has a particular rank, that every face of a
`VerticesFaces` has three indices, or that indices are within bounds. Such
requirements remain part of the documented API contract and should be checked
only where the operation needs them.

Retained-buffer APIs keep the concrete type inferred for their primary buffers.
For example, `Tessellation` accepts Python structural buffers and NumPy numeric
arrays while its `vertices`, `triangles`, and `to_vertices_and_triangles()`
annotations preserve the concrete input buffer types. Optional aligned buffers
accept the same broad families without adding generic parameters. Nested
structural buffers are described by `IndicesProtocol`, `IndexGroupsProtocol`, and
`PointGroupsProtocol`, so compatible native wrappers do not have to inherit
from `Sequence`. Validation
uses the operations required by the invariants (`index` for triangle indices
and finiteness testing for coordinates); it does not copy, coerce, mutate, or
take ownership of supplied buffers.

`Transformation` likewise retains a mutable nested-list matrix instead of
copying it. Python mutable lists are invariant, so a pre-bound
`list[list[int]]` or `list[list[numpy.float64]]` cannot be widened to the
matrix's writable element type soundly: a later floating-point assignment
would violate the caller's narrower annotation. Context-typed numeric literals
and core matrix results remain accepted. APIs using the neutral
`TransformationType` boundary also accept NumPy matrix arrays. Callers that
want retained mutable nested lists should annotate their elements with
`RealInput` or `float` at the ownership boundary.

Copying constructors use the structural aliases when their existing ownership
path already consumes those values. `Plane`, `Line`, `Frame`, `Polyline`,
`Polygon`, and `Pointcloud` accept compatible Python and NumPy coordinates.
`PolygonalSurface` and `Polyhedron` additionally accept NumPy integral face
indices, normalize copied indices to Python `int`, and reject Python and NumPy
booleans as indices. No separate eager validation pass is implied.

The former private `compas._typing` module and its overlapping coordinate and
mesh aliases were removed. Integrations should import the shared vocabulary
from `compas.typing`.

## Static fixture convention

Static typing behavior is characterized by `tests/typing/accepted.py` and
`tests/typing/expected_errors.py`. The accepted fixture must produce no Pyright
diagnostics. Every diagnostic in the negative fixture is declared on the same
line with an exact rule marker:

```python
value: IntegralInput = 1.5  # expected-error: reportAssignmentType
```

The pytest harness compares the diagnostic file, line, and rule with these
markers. Missing, additional, or moved diagnostics therefore fail the tests.
