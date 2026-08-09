# Migration Changes

## Colors

## Data

## Datastructures

### Mesh

This document summarizes the changes to `compas.datastructures.mesh` on the
`remove-future` branch relative to `origin/remove-future`.

#### Type annotations and API documentation

- Added shared mesh type aliases for vertices, faces, edges, attributes, and
  point coordinates in `mesh/types.py`.
- Added Python 3.9-compatible annotations throughout the `Mesh` class, mesh
  operations, Conway operators, duality, remeshing, slicing, smoothing, and
  subdivision.
- Added overloads where return types depend on input options and used `Self` or
  bounded type variables where functions preserve a custom `Mesh` subclass.
- Updated docstrings to use the current NumPy-style format and documented new
  explicit failure modes.
- Removed legacy type comments, redundant compatibility syntax, unused imports,
  and an empty `operations/extrude.py` module.

#### Mesh class

- Typed the internal halfedge, vertex, face, face-data, and edge-data mappings.
- Typed construction, serialization, attribute, topology, geometry, traversal,
  and transformation methods.
- Improved return contracts for methods that can return no result and added
  overloads for methods whose output depends on flags such as `data` and
  `include_none`.
- Preserved subclass types in alternate constructors and copy-like operations.
- Added explicit validation around invalid vertices, faces, edges, and attribute
  requests where the previous implementation failed indirectly.
- Expanded tests for construction, serialization, topology queries, attributes,
  transformations, and edge cases.

#### Topology operations

- Added typed contracts to edge collapse, insertion, face merging, edge and face
  splitting, vertex substitution, edge swapping, and unwelding.
- Standardized invalid-edge handling and documented operations that raise
  `ValueError` for invalid input.
- Added explicit `RuntimeError` failures when an operation unexpectedly produces
  an invalid face or cannot complete a requested topology change.
- Improved handling of boundary cases, fixed vertices, and optional operation
  results.
- Added regression coverage for successful operations, rejected operations,
  invalid inputs, boundaries, and fixed vertices.

#### Conway operators

- Added subclass-preserving return types to all Conway operators.
- Clarified that their documented topological relationships assume closed
  manifold seed meshes.
- Improved boundary handling and removed assumptions that both sides of every
  edge have an incident face.
- Simplified face construction and corrected connectivity used by several
  operators.
- Added tests for topology counts, validity, source immutability, subclass
  preservation, and open-mesh behavior.

#### Duality

- Added subclass-preserving overloads, including support for an explicitly
  requested output mesh class.
- Removed unused constants and consolidated boundary discovery.
- Added an explicit, documented `RuntimeError` when boundary vertices are not
  ordered consistently.
- Added coverage for closed and open meshes, geometry, oriented connectivity,
  boundary elements, and output types.

#### Remeshing

- Added types for remeshing options, fixed vertices, and iteration callbacks.
- Replaced the accidental division failure for a nonpositive target length with
  an explicit, documented `ValueError`.
- Clarified the meaning of the divergence threshold and callback arguments.
- Added coverage for target validation, boundary splitting, mesh validity, and
  callback invocation.

#### Mesh slicing

- Added types to the slicing helper and intersection state.
- Preserved custom `Mesh` subclasses in both resulting submeshes.
- Added explicit failures when an intersected edge cannot be split or two
  submeshes cannot be constructed.
- Narrowed face-splitting exception handling from all exceptions to the expected
  `ValueError`.
- Added coverage for valid closed slices, non-intersections, and subclass
  preservation.
- Documented that the current implementation assumes the input mesh represents a
  closed volume, but does not check this condition.

#### Smoothing

- Added common types for fixed vertices and iteration callbacks across centroid,
  center-of-mass, and area smoothing.
- Replaced generic callback exceptions with a documented `TypeError` for a
  non-callable callback.
- Made callback handling consistently distinguish `None` from a supplied
  callback.
- Added coverage for the geometry produced by every smoothing method, fixed
  vertices, callback invocation, and callback validation.

#### Subdivision

- Added typed, subclass-preserving contracts for the dispatcher and all
  subdivision schemes: triangle, quad, corner, Catmull-Clark, Doo-Sabin, frames,
  and Loop.
- Improved unsupported-scheme errors by including the requested scheme.
- Added explicit, documented failures when Catmull-Clark or Loop subdivision
  cannot split an edge, and when quad subdivision produces an invalid face.
- Changed frame offsets to accept any face-to-distance mapping, in addition to a
  single distance.
- Corrected zero-level quad subdivision so that it returns an unchanged,
  independent copy instead of adding internal path metadata.
- Documented that the Doo-Sabin `fixed` parameter is currently retained for API
  compatibility but has no effect.
- Expanded tests to cover every scheme, expected topology counts, validity,
  source immutability, zero subdivision levels, unsupported schemes, and custom
  mesh subclasses.

#### Known compatibility notes

- Collection-based attribute methods still use the legacy behavior in which an
  explicitly empty key collection may select all elements. This has not been
  changed because existing callers may rely on it.
- Edge-data keys remain direction-independent serialized strings internally.
  Centralizing canonical edge-key handling remains future work.
- Mesh slicing does not validate its closed-volume assumption.
- The Doo-Sabin `fixed` parameter remains nonfunctional.

### VolMesh

#### Type annotations and API documentation

- Added shared VolMesh types for vertices, edges, faces, halffaces, cells,
  attributes, coordinates, and cell topology.
- Added Python 3.9-compatible annotations throughout serialization,
  construction, accessors, attributes, topology, geometry, boundaries, and
  transformation.
- Added overloads for accessors and attribute methods whose return type depends
  on a data or setter argument.
- Preserved custom VolMesh subclasses in constructors and data round-trips.
- Documented explicit validation failures and the currently unimplemented
  `is_valid()` method.

#### Data and construction

- Fixed serialization of non-empty cell attributes.
- Prevented builders and default-attribute updates from mutating caller-owned
  mappings.
- Changed `add_halfface()` to reject vertex identifiers that are not already
  part of the VolMesh, avoiding vertices with implicit default geometry.
- Added canonical, direction-independent helpers for edge and face attribute
  data keys.
- Documented that these local helpers should become a dedicated data-key API
  used consistently by storage and serialization.

#### Attributes and queries

- Added support for explicitly storing `None` as a vertex, edge, face, or cell
  attribute value.
- Prevented filtering methods from modifying caller-owned condition mappings.
- Added the missing `has_cell()` query and corrected reversed-edge handling in
  `has_edge()`.
- Corrected semantic sample types, distinguishing faces from halffaces.

#### Topology and geometry

- Fixed `delete_vertex()` so that it removes the requested vertex after deleting
  its incident cells.
- Fixed edge and face attribute cleanup so shared topology retains its data until
  the final incident cell is removed.
- Fixed halfface manifold-neighbor traversal and support for unattached
  halffaces.
- Added explicit validation for vertex and halfface neighborhood rings below 1.
- Fixed cell vertex-neighbor traversal on Python 3, deduplicated cell edges, and
  deduplicated adjacent-cell results.
- Typed and verified vertex, edge, face, cell, boundary, and transformation
  geometry APIs.

#### Tests

- Expanded VolMesh coverage for serialization, constructors, builders,
  modifiers, samples, all attribute domains, filtering, topology, geometry,
  boundaries, data cleanup, subclass preservation, and transformation.

#### Known compatibility notes

- `VolMesh.is_valid()` remains unimplemented and raises `NotImplementedError`.
- Edge and face data keys remain serialized strings internally pending a
  dedicated canonical data-key API.
