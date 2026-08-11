# Migration Changes

## Colors

## Data

## Files

### General

- Updated file-format documentation to the current MkDocs-compatible
  NumPy-style conventions by removing Sphinx roles, directives, duplicated
  parameter types, and unnecessary fully qualified return-type paths.
- Removed the remaining Python 2, old CPython, and IronPython compatibility
  paths from the file-format infrastructure.
- Added shared `_iotools.read_bytes()` and `_iotools.write_bytes()` helpers for
  consistent path, URL, text-stream, and binary-stream handling across formats.

### OBJ

- Replaced the stateful legacy `OBJ` facade with an explicit document-based
  pipeline consisting of `OBJReader`, `OBJParser`, `OBJDocument`, and
  `OBJWriter`.
- Added typed OBJ document elements for vertices and their texture and normal
  references, points, lines, faces, ordered elements, objects, groups,
  materials, and smoothing groups.
- Added `read_obj()` and `write_obj()` convenience functions supporting paths,
  URLs, text streams, and binary streams. Writing supports documents, individual
  meshes, multiple named meshes, metadata headers, and explicitly unwelded face
  output.
- Added `OBJData` and `obj_data()` as an identity-preserving projection from
  structured OBJ elements to plain vertex indices. Reading no longer welds
  coincident vertices implicitly.
- Added the explicitly named `weld_obj_data()` conversion for workflows that
  require coordinate-based vertex merging, with a configurable geometric-key
  precision.
- Added `read_obj_meshes()` to extract all named polygon meshes from a source,
  preserve object names and independent vertex identities, collect unassigned
  faces, and optionally request explicit welding.
- Updated OBJ integration in Mesh, Graph, VolMesh, and CellNetwork. Indexed mesh
  faces preserve their OBJ vertex identities, line-based graph and mesh
  construction performs topology merging in `from_lines()`, and cell-based
  datastructures request welding explicitly when shared cell vertices are
  required.
- Added parsing for positive and negative vertex references, texture and normal
  references, objects, groups, material libraries, active materials, smoothing
  groups, continuations, comments, and degree-one `curv` statements.
- Preserved standalone and inline comments in `OBJDocument`, moved all OBJ
  serialization helpers out of the writer class, and made generated metadata a
  document concern rather than writer configuration.
- Aligned OBJ and PLY pipeline responsibilities: readers now only normalize
  paths, URLs, and streams to bytes, while parsers own decoding, lexical
  processing, format syntax, and document construction.
- Added semantic document, parser, writer, stream, multiple-mesh, welded and
  non-welded projection, and roundtrip tests. Roundtrip coverage verifies that
  identity-preserving reads retain vertex counts while explicit welding produces
  and retains the reduced topology.

### PLY

- Replaced the stateful `PLY` facade with a schema-driven pipeline consisting
  of `PLYReader`, `PLYParser`, `PLYDocument`, and `PLYWriter`.
- Added structured PLY properties and elements that preserve ordered schemas,
  custom scalar and list properties, comments, object information, format, and
  version metadata.
- Added `read_ply()`, `write_ply()`, and the mesh-oriented `ply_data()`
  projection, with support for paths, URLs, text streams, and binary streams.
- Added generic ASCII, binary little-endian, and binary big-endian parsing and
  writing, including variable-length list properties and standard scalar type
  aliases.
- Centralized PLY scalar definitions, parsing, validation, packing, and
  unpacking in a shared codec module.
- Strengthened PLY validation for formats, property schemas, scalar kinds and
  ranges, list-count types and capacities, trailing and truncated data, and
  mesh vertex references.
- Applied numeric precision during ASCII serialization rather than rounding the
  semantic document data, and ensured metadata options are applied to copied
  documents without mutating caller-owned data.
- Updated Mesh and Pointcloud PLY integration without changing their public
  constructors and conversion methods.
- Added tests for custom schemas and properties, ASCII document roundtrips,
  binary fixtures, variable-size binary faces, streams, and mesh roundtrips.

### OFF

- Replaced the stateful `OFF` facade with the aligned `OFFReader`, `OFFParser`,
  `OFFDocument`, and `OFFWriter` pipeline.
- Added `read_off()` and `write_off()` convenience functions using explicit
  source and target parameters and shared byte I/O.
- Preserved standalone and inline comments as document metadata and applied
  author, email, and date metadata without mutating caller-owned documents.
- Added strict parsing and validation for headers, counts, coordinate
  dimensions, face degrees, vertex references, incomplete input, and trailing
  data, with support for continuations and counts on the header line.
- Applied numeric precision only during serialization and updated Mesh OFF
  integration without changing `Mesh.from_off()` or `Mesh.to_off()`.
- Added separated reader, parser, document, writer, convenience, malformed-input,
  metadata, and welded and non-welded mesh roundtrip tests.

### XML

- Removed the `XML`, `XMLReader`, `XMLWriter`, and `XMLElement` class hierarchy
  in favor of the explicit `read_xml()`, `parse_xml()`, `write_xml()`, and
  `xml_to_string()` functions.
- Removed the entire private `_xml` compatibility package for IronPython and
  CPython versions older than 3.8.
- Reimplemented XML processing directly with `xml.etree.ElementTree`, while
  retaining COMPAS path, URL, text-stream, and binary-stream support through
  `_iotools`.
- Replaced `minidom` formatting with `ElementTree.indent()` and ensured pretty
  serialization does not mutate the caller's element tree.
- Adopted standard ElementTree namespace semantics: expanded names and namespace
  meaning survive roundtrips, but `xmlns` declarations are no longer injected
  as artificial element attributes and original prefixes are not guaranteed.
- Added coverage for files, URLs, text and binary streams, string parsing,
  string and byte serialization, nonmutating formatting, writing, and namespace
  roundtrips.

## Datastructures

### Shared infrastructure

- Typed the `Datastructure` base class, including serialization, inheritance,
  bounding-box caches, transformation hooks, and copy-transform helpers.
- Replaced legacy return-type comments with subclass-preserving `Self` types and
  made the implicit `to_points()` contract explicit.
- Prevented datastructures from retaining caller-owned attribute mappings.
- Typed the mutable-mapping compatibility implementation with generic key and
  value types and overloads for `get()`, `pop()`, and `setdefault()`.
- Fixed keyword-only `MutableMapping.update()` calls, which previously ignored
  all supplied values.
- Documented that avoiding abstract base classes and metaclasses was an
  IronPython 2.7 workaround that should now be reconsidered.
- Typed the attribute-view hierarchy and fixed `custom_only=True` so lookup,
  membership, iteration, and length expose the same keys.
- Removed redundant specialized attribute-view constructors and corrected the
  `CellAttributeView` description.

### Graph

#### Type annotations and API documentation

- Added shared graph types for hashable node identifiers, edges, and attribute
  dictionaries.
- Added Python 3.9-compatible annotations throughout serialization,
  constructors, conversions, accessors, attributes, topology, geometry,
  transformations, matrices, duality, planarity, operations, and smoothing.
- Added overloads for node and edge accessors and getter/setter attribute APIs,
  and preserved custom Graph subclasses in constructors and graph-producing
  operations.
- Removed the legacy graph data schema and migrated docstrings away from Sphinx
  roles and duplicated parameter types.

#### Graph behavior and operations

- Corrected automatic node-key tracking so only integer keys affect the next
  generated key.
- Added support for explicitly storing `None` in node and edge attributes.
- Fixed connected-component edge grouping and graph explosion for mixed node-key
  types.
- Added safe handling for empty and edgeless cycle searches and typed the cycle
  and neighbor-ordering helpers.
- Improved edge splitting and degree-two edge joining, including validation,
  default attributes, and preservation of remaining node attributes.
- Expanded polyline extraction coverage for empty, open, closed, disconnected,
  branched, and explicitly split graphs.
- Typed and verified crossing detection, planarity checks, planar embeddings,
  and centroid smoothing, including fixed nodes, damping, isolated nodes, and
  callback validation.

#### Tests

- Added focused coverage for graph serialization, mixed key types, nullable
  attributes, duality, topology operations, polylines, planarity, crossings,
  smoothing, callbacks, and empty-graph behavior.

### Tree and HashTree

#### Tree

- Added typed serialization, parent/child relationships, traversal strategies,
  node lookup, hierarchy formatting, and Graph conversion for `Tree` and
  `TreeNode`.
- Preserved subclasses in data construction and added correct optional return
  types for roots, parents, owning trees, and name-based lookup.
- Fixed empty-tree deserialization and replaced breadth-first list popping with
  a deque.
- Added explicit errors for unsupported traversal strategies and orders.
- Documented remaining design questions around ownership, cycles, reparenting,
  mutable child lists, detached subtrees, subclass deserialization, and duplicate
  Graph keys.
- Expanded tests for invalid traversal options, ancestors and descendants,
  empty-tree round-trips, duplicate-name lookup, and limited-depth hierarchy
  output.

#### HashTree

- Reworked `HashTree` and `HashNode` as independent immutable data types instead
  of mutable subclasses of `Tree` and `TreeNode`.
- Added typed serialization, traversal, hierarchy formatting, Graph conversion,
  signatures, and diffing.
- Made children immutable, defensively copied values, and distinguished an
  explicit `None` value from a branch node without a value.
- Made signatures independent of dictionary insertion order and computed them
  lazily from immutable node content.
- Added validation for values combined with children, duplicate sibling paths,
  reused child nodes, invalid roots, missing diff roots, non-Data inputs, and
  duplicate Graph keys.
- Added comprehensive serialization, immutability, signature, validation,
  conversion, and diff regression tests.

### Removed datastructures

- Removed the deprecated `Assembly`, `Part`, and related assembly exceptions and
  tests from `compas.datastructures`.

### Mesh

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

### CellNetwork

#### Type annotations and API documentation

- Added shared CellNetwork types for vertices, edges, faces, cells, attributes,
  and point coordinates.
- Added Python 3.9-compatible annotations throughout serialization,
  construction, conversion, accessors, attributes, topology, boundaries, and
  geometry.
- Added exhaustive overloads for accessors and attribute methods whose return
  type depends on `data`, `names`, `values`, or setter arguments.
- Updated overloaded-function docstrings to document every return or yield
  scenario separately.
- Converted docstrings from Sphinx roles and directives to the NumPy-style
  syntax expected by Griffe and MkDocstrings, and removed duplicated parameter
  type declarations.
- Preserved custom CellNetwork subclasses in data round-trips and alternate
  constructors.

#### Data and construction

- Removed the legacy data schema declaration and typed the internal topology and
  attribute mappings directly.
- Fixed serialization round-trips for edge orientation and complete cell data.
- Prevented builders, filters, and default-attribute updates from mutating
  caller-owned mappings.
- Changed `add_face()` to reject missing vertices and faces with fewer than
  three vertices before modifying topology.
- Added a canonical, direction-independent helper for edge attribute-data keys.
- Fixed edge insertion so adjacency is stored in the supplied direction, and
  fixed edge deletion so its attributes are removed.

#### Attributes and queries

- Added support for explicitly storing `None` as a vertex, edge, face, or cell
  attribute value.
- Made explicitly empty vertex, edge, face, and cell selections remain empty
  instead of selecting every element.
- Fixed list-valued vertex filters so remaining conditions are still evaluated.
- Made `edges(data=True)` return the documented `EdgeAttributeView`, including
  default attributes.
- Added the missing `has_cell()` query and corrected accessor return contracts,
  including sample functions and predicate filters.

#### Topology, geometry, and conversions

- Added explicit validation for vertex neighborhood rings below 1.
- Fixed `vertex_neighbors()` to return the documented list.
- Fixed `edge_cells()` to inspect both edge directions and deduplicate cells.
- Fixed `cell_vertex_neighbors()` to use edge adjacency rather than vertex
  attributes.
- Deduplicated cell edges and documented invalid cell-face membership with an
  explicit `ValueError`.
- Fixed `faces_to_mesh()` for generator inputs and updated OBJ construction to
  use the public parser data.
- Converted attribute views to dictionaries at Graph API boundaries and
  preserved default attributes during graph conversion.
- Typed and verified vertex, edge, face, cell, boundary, and geometry queries.

#### Tests

- Expanded CellNetwork coverage for serialization, subclass preservation,
  clearing, builders, validation, samples, attribute overload scenarios,
  filtering, topology, geometry, boundaries, and graph and mesh conversions.

#### Known compatibility notes

- `CellNetwork.is_valid()` remains unimplemented and raises
  `NotImplementedError`.
