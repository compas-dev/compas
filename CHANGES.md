# Migration Changes

## Public package APIs

- Added explicit `__all__` declarations to every direct `compas.*` package.
  These second-level package exports now define the official public API, and
  the former blanket Ruff suppressions for re-exported imports were removed.
- Removed the nonfunctional `Pointcloud.from_pcd` constructor, which silently
  returned `None`; no PCD reader exists in the core package.
- Corrected unavailable constrained Delaunay triangulation and Brep loop
  validation implementations to raise through their documented extension
  contracts instead of returning `None` or an exception class.

## Tolerance

- Modernized `Tolerance` with Python 3.12 annotations and MkDocs-compatible
  documentation, including its public properties and context manager.
- Explicit zero tolerance values now remain valid settings and overrides;
  omitted values alone fall back to the configured defaults.
- Removed the unused deprecated `Tolerance.units` alias. Use
  `Tolerance.unit`.
- Preserved subclass construction through `Tolerance.__from_data__` and added
  regression coverage for serialization, temporary settings, and exact
  comparisons.
- Made `Tolerance.is_allclose` accept nested iterables and generators, reject
  unequal lengths and mismatched nesting, and retain element-wise recursive
  comparison without materializing the inputs.
- Defined `Tolerance.precision_from_tolerance` for positive tolerances smaller
  than one and made values outside that domain raise `ValueError` consistently.

## Utilities

- Removed the private `compas._os` compatibility module. The core package now
  uses `pathlib` and standard platform paths directly while preserving its
  existing string-valued package, data, temporary, and user-data constants.
  This removes the unused Python 2 Windows symlink polyfill, administrator
  elevation, Conda bootstrapper integration, vendored app-directory logic, and
  Rhino, Grasshopper, Blender, and Mono runtime probes.
- Modernized the shared internal I/O helpers with explicit path, URL, text
  stream, and binary stream types. Stream ownership now uses standard context
  managers directly: caller-owned streams remain open, while paths, URL
  responses, and URL buffers opened by COMPAS are closed predictably.
- Removed the `compas.utilities` package. Its remaining callback adapter,
  timestamp helpers, remote operations, compatibility decorators, caching,
  and profiling helpers were either unused, duplicated standard-library
  functionality, or unrelated to the host-independent core framework.
- Removed the unused SSH and remote-download helpers. The SSH wrapper depended
  on undeclared Paramiko functionality, invoked shell commands, changed the
  process working directory, and was unrelated to the host-independent core.
- Removed the obsolete `abstractclassmethod` and `abstractstaticmethod`
  compatibility decorators. Compose `classmethod` or `staticmethod` with
  `abc.abstractmethod` directly on supported Python versions.
- Removed `print_profile` and the custom `memoize` decorator. Use `cProfile`
  and `functools.cache` or `functools.lru_cache` from the standard library.
- Removed the unused `await_callback`, `timestamp`, and `now` helpers. Use
  application-specific synchronization and Python's `datetime` module.

## Topology

- Modernized all connectivity, combinatorics, orientation, and traversal APIs
  with generic hashable-key annotations and MkDocs-compatible documentation.
- Removed the remaining Rhino-specific face-adjacency fallback. Spatial face
  searches now use SciPy when available and the core `KDTree` otherwise.
- Exposed `breadth_first_tree` from `compas.topology` and corrected it to
  return one root-to-node path per node in breadth-first order.
- Defined identity paths consistently: unweighted, A*, and Dijkstra path
  searches now return `[root]` when their start and goal are the same.
- Made A* support arbitrary hashable keys when candidates have equal
  priorities, without requiring the keys themselves to be orderable.
- Added behavioral coverage for connectivity construction, face assembly,
  graph coloring, connected components, unweighted traversal, weighted paths,
  identity paths, and non-orderable graph keys.

## Linear algebra edge cases

- Removed the undocumented `Memoized` class and `memoize` decorator from
  `compas.linalg`. The public `chofactor()` and `lufactorized()` functions now
  directly factor the supplied matrix rather than sharing a process-global
  cache keyed by an ignored extra argument.
- Corrected `vector_variance` to return population variance and
  `vector_standard_deviation` to return its square root.
- Fixed Gram-Schmidt orthonormalization for residual vectors whose nonzero
  components are negative, and made `sum_vectors` reject axes other than `0`
  and `1`.
- Defined determinants and inverses for 0x0 and 1x1 matrices, and applied the
  tolerance policy when rejecting singular matrices.
- Made `decompose_matrix` explicitly require a 4x4 transformation matrix.
- Added explicit errors for zero rotation axes, zero plane normals, and
  projection directions parallel to a plane, while preserving a zero
  axis-angle vector as the identity transformation.
- Removed the long-deprecated `compas.linalg.close` and
  `compas.linalg.allclose` helpers. Use `TOL.is_close` and `TOL.is_allclose`,
  which support the shared absolute and relative tolerance policy.

## Triangle-mesh algorithms

- Grouped triangle-mesh algorithms in the `compas.geometry.trimesh`
  subpackage, with capability modules for curvature, gradients, matrices,
  parametrisation, remeshing, sampling, slicing, smoothing, and related tasks.
- Preserved root-level `compas.geometry` imports while removing the former
  direct `trimesh_*.py` module paths.
- Renamed `trimesh_gradient_numpy`, `trimesh_descent_numpy`,
  `trimesh_pull_points_numpy`, and `trimesh_samplepoints_numpy` to
  `trimesh_gradient`, `trimesh_descent`, `trimesh_pull_points`, and
  `trimesh_sample_points` without compatibility aliases.
- Exposed the previously hidden cotangent-matrix, point-pulling, sampling, and
  smoothing functions through the triangle-mesh subpackage and root geometry
  API, and merged the two matrix modules.
- Fixed Gaussian curvature to count each incident corner once and use the
  correct angular deficit for boundary vertices.
- Replaced the broken nearest-vertex point-pulling implementation with a
  complete closest-point search over mesh triangles, including degenerate
  triangle handling.
- Fixed sampled normals to preserve their direction, made the gradient accept
  raw list data and honor its documented `"list"` result format, and fixed
  cotangent smoothing for meshes with non-contiguous vertex keys.
- Removed the unimplemented positive cotangent Laplacian stub. Curvature,
  geodesic, isoline, mass-matrix, parametrisation, remeshing, and slicing
  operations that lack core implementations remain explicitly pluggable.
- Standardized raw triangle-mesh parameters as `mesh`, added precise dense and
  sparse matrix return overloads, and made zero-area sampling and
  zero-normalization cotangent inputs raise explicit `ValueError` exceptions.
- Made datastructure remeshing initialize its convergence baseline explicitly,
  reject meshes without edges, and treat a nonpositive iteration count as a
  no-op.

## Transformation package

- Moved `Transformation`, `Translation`, `Rotation`, `Reflection`, `Projection`,
  `Scale`, and `Shear` into the `compas.geometry.transformations` subpackage.
- Root-level imports such as `from compas.geometry import Rotation` remain the
  canonical public API, and serialized dtype identifiers remain unchanged.
- Removed the former direct module paths such as `compas.geometry.rotation` and
  replaced circular root-package imports between transformation classes with
  local subpackage imports.
- Aligned `Rotation.from_euler_angles` with the base constructor contract,
  including its optional rotation point, and now use the shared `Data.copy`
  implementation for transformation copies.
- Added complete Python 3.12 annotations and MkDocs-compatible docstrings to
  the transformation classes, including subclass-preserving factory return
  types and documented computed properties.
- Replaced mutable rotation-point defaults with immutable coordinate tuples,
  corrected the invalid base `Transformation.__repr__`, and removed needless
  coordinate-to-list conversions from rotation and reflection construction.
- Broadened low-level frame, projection, translation, shear, and normalization
  annotations to match the structural coordinate objects already accepted at
  runtime.

## Quad-mesh planarization

- Moved the legacy pure-Python planarization algorithm out of the unused
  `quadmesh_planarize_none.py` module and made it the default implementation of
  the public `quadmesh_planarize` pluggable.
- The default implementation operates directly on the public
  `(vertices, faces)` input, returns new vertex coordinates without mutating the
  input, honors `kmax` and `maxdev`, and remains overridable by plugins.

## Principal component analysis

- Renamed `pca_numpy` to the canonical `pca` function and moved it from
  `pca_numpy.py` to `pca.py`.
- Removed the old `compas.geometry.pca_numpy` import without a compatibility
  alias and updated bounding-box, best-fit, and ICP algorithms to use `pca`.
- NumPy and SciPy imports are now local to `pca`, avoiding eager numerical
  imports when loading `compas.geometry`.

## Interpolation modules

- Consolidated `interpolation_barycentric.py`, `interpolation_coons.py`, and
  `interpolation_tweening.py` into `compas.geometry.interpolation`.
- Preserved the public `barycentric_coordinates`, `discrete_coons_patch`,
  `tween_points`, and `tween_points_distance` imports from `compas.geometry`.
- Removed the three obsolete module import paths without compatibility aliases.
- Modernized interpolation annotations and documentation while preserving point
  pairing, vertex ordering, face ordering, and triangular Coons patch behavior.

## Scalar-field contours

- Added a built-in `scalarfield_contours` implementation based on SciPy linear
  interpolation and a Python marching-squares pass, removing the need for a
  plotting backend or contour plugin.
- `scalarfield_contours` now accepts either a contour count or explicit contour
  levels and returns the levels with joined XY paths.
- NumPy and SciPy imports remain local so importing `compas.geometry` does not
  eagerly import the numerical stack.

## Framework scope

- Focused this repository entirely on the host-independent COMPAS core
  framework. Removed the bundled `compas_rhino`, `compas_ghpython`, and
  `compas_blender` integration packages; host-specific integrations belong in
  separate projects.
- Migrated CI, coverage, documentation, pull-request checks, and releases to
  the composable `compas-dev/compas-actions` v1 workflows. Releases now use a
  reviewed release pull request, trusted PyPI publishing, and a separately
  permissioned GitHub release.
- Removed Grasshopper and Yak workflows and Invoke tasks, and aligned package
  versioning and metadata with the core-only distribution.
- Removed the `compas.rpc` package, its `compas_rpc` command-line entry point,
  and its obsolete integration tests.
- Replaced the Sphinx documentation tree with a MkDocs site organized into
  Getting Started, Examples, Reference, and Background tabs. Migrated the core
  user guide to Markdown, generated API reference pages with mkdocstrings, and
  consolidated images, JavaScript, and runnable example sources under
  `docs/assets`.
- Raised the minimum Python version to 3.12 and migrated annotations to built-in
  generics and PEP 604 unions. Removed the remaining Python 2 and IronPython
  flags, branches, filesystem fallbacks, test skips, and .NET exception shim,
  and replaced legacy explicit-class `super()` calls with zero-argument
  `super()`.

## Colors

- Modernized `Color`, `ColorDict`, and `ColorMap` for Python 3.12 with
  subclass-preserving constructors, explicit input and mapping types, and
  MkDocs-compatible documentation.
- Consolidated color coercion for `Color` objects, RGB1 and RGB255 sequences,
  hexadecimal strings, CSS color names, and `None`. Invalid component counts
  now raise `ColorError` instead of being accepted ambiguously.
- Added correct three-digit hexadecimal expansion, safe zero saturation for
  black, and comparison with unrelated objects without raising exceptions.
- Made `ColorMap` serializable `Data`, preserved alpha while copying colors,
  validated zero-length lookup ranges, and removed the remaining Rhino-specific
  compatibility wording.
- Made `ColorDict` a standard mutable mapping with arbitrary hashable keys,
  explicit fallback colors, pair-based JSON data that preserves non-string key
  identity, and rejection of `None` values.

## Data

- Removed the remaining `.NET` serialization compatibility hooks and the
  IronPython-only `Data.ToString` method.
- Added trusted `Frame` reconstruction from canonical serialized data, avoiding
  redundant axis orthonormalization. `Frame.__from_data__` now assumes its axes
  came from `Frame.__data__` and copies them without validation, unitization, or
  orthogonalization; malformed data can therefore construct an invalid frame.
  Arbitrary axes must continue to use `Frame(...)`, which establishes the
  orthonormal invariant. In the `compas3` environment this reduced direct
  reconstruction from approximately 8.08 μs to 1.74 μs and a complete JSON
  round trip from approximately 12.3 μs to 5.74 μs.
- Reused the trusted `Frame` construction path for copies, world frames, and
  rotation-based factories whose axes are already orthonormal. Direct copies
  dropped from approximately 6.68 μs to 2.58 μs, world-frame construction
  from 8.03 μs to 1.63 μs, and copy-plus-transform from 77.3 μs to 58.9 μs
  in the `compas3` environment. Batches of 10,000 world frames, copies, and
  canonical reconstructions took approximately 17.4 ms, 25.7 ms, and 16.0 ms.
  The ordinary public constructor remains defensive for arbitrary axes.
- Cached successful JSON dtype resolution and consolidated malformed, missing
  module, and missing class failures into one `DecoderError` path. Repeated
  lookup of `compas.geometry/Frame` dropped from approximately 583 ns to 124 ns
  in the `compas3` environment.
- Replaced the global mutable `DataEncoder.minimal` flag with per-encoder state,
  preventing configuration leakage between sequential, nested, or concurrent
  serialization calls.
- Removed the redundant `Data.__clstype__` hook. Datastructure inheritance
  fallback identifiers are now generated directly where they are used, while
  `Data.__dtype__` remains the canonical serialized instance identifier.
- Simplified `Data` pickle state to its instance dictionary instead of embedding
  a redundant COMPAS JSON dump that restoration ignored. `Frame` pickling in
  the `compas3` environment dropped from approximately 13 μs to 6.31 μs.
- Made the optional copy class check explicit with `cls is None` and renamed the
  data copy test fixture so pytest no longer mistakes it for a test class.
- Modernized the public `Data` and JSON annotations and MkDocs docstrings,
  including precise text and binary stream aliases, `Self` return documentation,
  Markdown cross-references, and removal of redundant `None` return sections.
  An explicitly assigned empty data-object name is now preserved; only `None`
  selects the class-name default.
- Removed unused sequence coercion and concrete-type validation helpers. The
  remaining iterable check now uses Python's iterator protocol directly without
  allocating a list or consuming iterator input.

## Geometry offsets

- Added Python 3.12 annotations and MkDocs-compatible documentation throughout
  the line, polygon, and polyline offset utilities. Replaced mutable normal
  defaults with immutable coordinate tuples and corrected the documented
  distance parameter and polygon closure behavior.

## Best-fit geometry

- Consolidated the pure-Python and NumPy best-fit implementations in
  `bestfit.py`. Removed the implementation-specific `_numpy` public functions
  and the `bestfit_numpy` module; the canonical API is now `bestfit_line()`,
  `bestfit_plane()`, `bestfit_frame()`, `bestfit_circle()`, and
  `bestfit_sphere()`.
- Made NumPy and SciPy imports local to best-fit calls. `bestfit_plane()` now
  uses the PCA implementation that previously lived in `bestfit_plane_numpy()`;
  mesh face-curvature results can therefore differ slightly from the former
  approximate determinant fit.
- Standardized fitted circle and sphere radii as scalar `float` results instead
  of leaking NumPy scalar or one-element array details.

## Hulls, ICP, and booleans

- Consolidated convex-hull algorithms in `hull.py` and removed `hull_numpy.py`
  and the `_numpy` function names. `convex_hull()` and `convex_hull_xy()` now
  use SciPy and return hull vertex indices together with face or edge indices.
- Corrected `Polyhedron.from_convex_hull()` to remap hull faces onto boundary
  vertices, omit interior points, and unify face cycles before construction.
- Replaced `icp_numpy()` and its module with `icp()` in `icp.py`. ICP now
  consistently returns transformed points and the accumulated transformation,
  including when the initial PCA alignment already satisfies the tolerance.
- Moved the optional Shapely polygon-boolean defaults into `booleans.py` with a
  local import and removed the separate `booleans_shapely` plugin module. Mesh
  booleans remain plugin-only extension points.
- Changed polygon Boolean operations to consistently return
  `list[PlanarRegion]`, preserving empty results, disconnected components, and
  interior holes. Polygon and raw-loop inputs remain supported, and
  `PlanarRegion` inputs are now accepted directly. Shapely is therefore a core
  dependency.
- Removed the unused `watchdog` dependency. It was only used by the removed RPC
  auto-reloader.
- Removed stale setuptools declarations for the already removed
  `requirements.txt` and `requirements-dev.txt` files.

## Plugin system

- Replaced ambient scanning and importing of every installed `compas*` package
  with explicit discovery through the `compas.plugins` package entry-point
  group. Core plugin modules are registered explicitly, module registration is
  idempotent, discovery order is deterministic, and independent plugin manager
  instances can be reset cleanly in tests.
- Replaced relative `tryfirst` and `trylast` flags with explicit integer
  priorities. Selection now rejects equally preferred implementations instead
  of depending on discovery order. Both selection modes validate that every
  selected callable accepts the actual extension-point invocation, and errors
  from `collect_all` plugins propagate instead of being returned as ordinary
  values.
- Replaced dictionary-based plugin metadata and string registry keys with
  immutable typed `ExtensionPoint`, `PluginSpec`, and `PluginImpl` records.
  Requirement checking, collection, and selection now belong directly to
  `PluginManager`; class completeness checking is exposed as the standalone
  `validate_plugin_implementation` function.
- Typed `plugin` and `pluggable` with `ParamSpec`, replaced import-based
  requirement probing with `importlib.util.find_spec`, and removed the obsolete
  `Importer` and `PluginValidator` classes. Extension packages now have a
  documented `compas.plugins` entry-point contract.

## Quaternion

- Modernized `Quaternion` with Python 3.12 annotations and MkDocs-compatible
  documentation for its construction, properties, operators, and methods.
- Preserved subclasses across multiplication, alternative constructors,
  unitization, canonization, conjugation, and spherical interpolation.

## KD-tree

- Modernized `KDTree` with typed nodes and neighbor results and
  MkDocs-compatible documentation.
- Empty or fully excluded searches now return `None`, and multi-neighbor
  searches stop when the tree is exhausted instead of returning invalid
  `[None, None, inf]` entries.
- Made point-cloud set operations handle empty point clouds consistently.
- Completed the adjacent `Pointcloud` typing and documentation pass, preserved
  subclasses for non-mutating set operations, honored explicit zero
  tolerances, and invalidated its spatial index after indexed replacement or
  transformation.

## Delaunay triangulation

- Completed the Delaunay typing and MkDocs documentation pass and documented
  that the built-in SciPy implementation triangulates only XY coordinates.
- Added direct coverage for NumPy triangle-index output, geometry-object input,
  ignored Z coordinates, and both plugin-only constrained extension points.

## Brep interfaces

- Replaced backend-specific `Brep` class substitution with a stable public
  `compas.geometry.Brep` wrapper that owns the backend-native payload. Brep
  construction, serialization, queries, conversion, and modeling behavior now
  dispatch through operation-level plugin extension points; backends implement
  those operations without replacing the public class. The typed extension
  contracts live in `compas.geometry.brep.operations`, use dedicated factory,
  query, operation, serialization, and I/O categories, and explicitly return
  the concrete core `Brep` rather than a backend-specific `Self` subtype.
- Modernized the lightweight `BrepVertex`, `BrepTrim`, and `BrepLoop`
  interfaces with precise backend-neutral property types, subclass-preserving
  constructors, and MkDocs-compatible documentation.
- Modernized `BrepEdge`, resolved its hyperbola, parabola, and B-spline
  conversion contracts, and added the previously documented but missing
  `native_edge` property to the backend interface.
- Modernized `BrepFace`, aligned face area and centroid with the property-based
  backend contract, added the missing cylinder constructor argument, corrected
  the `SURFACE_OF_EXTRUSION` name, and formalized analytic and NURBS surface
  conversions. `to_polygon()` explicitly returns only the outer boundary;
  `to_polygons()` returns all loops.
- Modernized the main `Brep` interface, restored the complete `BrepType` value
  set, formalized its backend-neutral component and classification properties,
  and aligned area, volume, and centroid with the property-based backend
  contract. Migrated all `Brep` docstrings from Sphinx roles and legacy type
  notation to MkDocs-compatible NumPy style. Typed the factory constructors and
  defined Boolean factories and operators to return one Brep consistently,
  removing the operators' legacy first-item extraction for list results.
- Aligned the remaining `Brep` conversion, relationship, and modeling contracts
  with the active backend: tessellation and view-mesh methods return a mesh plus
  edge polylines, `slice()` returns an optional section Brep, `edge_loops()` is
  plural, trimming no longer declares an unused tolerance argument, and overlap
  exposes both linear and angular meshing controls.

## NURBS interfaces

- Replaced backend-specific `NurbsCurve` subclasses with a stable public
  wrapper that owns the native curve payload. Construction, queries,
  evaluation, mutation, and I/O now dispatch through typed operation-level
  extension points grouped by capability. Factory contracts explicitly return
  the concrete core `NurbsCurve`, including when invoked through a subclass.
- Applied the same design to `NurbsSurface`. Its wrapper owns the native
  surface payload, preserves the canonical V-row/U-column control-grid and
  full-knot-vector contracts, and dispatches construction, queries,
  evaluation, transformation, conversion, and I/O through focused extension
  points that return the concrete core `NurbsSurface`.

## Bounding boxes

- Standardized axis-aligned and oriented bounding volumes as `aabb()` and
  `obb()` methods returning `Box` across geometry and datastructures. Removed
  the redundant `compute_aabb()` and `compute_obb()` names.
- Removed bounding-box caches and their invalidation plumbing. Bounds are now
  computed from current geometry on every call, which avoids stale results for
  mutable objects and datastructures whose public storage can be edited
  directly.
- Changed `CellNetwork.aabb()` from raw box coordinates to the shared `Box`
  result and added `CellNetwork.obb()`.
- Removed the redundant `Polygon.bounding_box` property; `Polygon.aabb()` is
  the canonical object-level axis-aligned bounding-box API.
- Consolidated the pure-Python and NumPy bounding-box implementations in
  `bbox.py`. Removed the implementation-specific `_numpy` public names and the
  `bbox_numpy` module, added the canonical `oriented_bounding_box_xy()` entry
  point, and made NumPy and SciPy imports local to numerical calls. Internal
  minimum-box helpers are now private.
- Added Python 3.12 annotations and MkDocs-compatible documentation to the raw
  bounding-box functions, including precise overloads for the private helpers.
- Standardized computed geometric measurements as methods. `area()`,
  `volume()`, and `centroid()` now use the same call syntax across geometry,
  datastructures, polygonal regions and surfaces, analytic shapes and surfaces,
  point clouds, polyhedra, and Brep interfaces.
- Kept structural vector attributes such as `Frame.normal` and `Plane.normal`
  as properties because they describe object state. Standardized computed
  normals as methods: `Polygon.normal()` now matches `Mesh.normal()`.

## Iteration utilities

- Added Python 3.12 generic annotations and MkDocs-compatible documentation to
  the iteration utilities. `iterable_like` now uses overloads so callers that
  provide a fill value get a non-optional iterator result.
- Removed the obsolete Python 2 `izip_longest` fallback and commented-out random
  selection recipes. Added direct coverage for numeric remapping, grids,
  spacing, reshaping, flattening, sliding windows, padding, grouping, defaults,
  generator inputs, and lazy consumption.

## Type suppression audit

- Removed obsolete casts from glTF matrix construction, point transformation,
  scene reconstruction, format selection, and mesh subdivision. Added
  subclass-preserving overloads to `gltf_to_scene` so `Scene.from_gltf` no
  longer needs to assert its return type.
- Replaced ignored enumerations of NumPy scalar classes with `numpy.integer`
  and `numpy.floating`, corrected the `JSONDecoder.object_hook` override
  contract, and removed the final Python 2 `urllib` fallback.
- Retained narrowly scoped casts and ignores where they document actual dynamic
  boundaries, validated payload invariants, optional dependencies, or gaps in
  third-party type information.

## Scene foundation

- Made automatic scene-context selection deterministic: the sole registered
  named context is selected, while no context is guessed when several are
  available. Removed Rhino, Grasshopper, and Blender host detection from the
  core scene package.
- Removed the obsolete pre-Python-3.6 descriptor metaclass compatibility layer.
  Scene descriptors now rely directly on Python's native `__set_name__`
  protocol.
- Simplified scene-object serialization to store only local transformations.
  The derived world frame is no longer constructed or serialized redundantly;
  nested world transformations are reconstructed from the scene hierarchy.
- Added regression coverage for context selection, local transformation
  payloads, nested transformation reconstruction, and shared item identity.
- Changed `Scene` from a `Tree` subclass to a `Data` object that owns a typed
  `Tree[SceneObject]` through its `tree` attribute. The scene root is now a
  private `Group`, so every node in the scene tree follows the same
  `SceneObject` contract.
- Made `Tree` and `TreeNode` generic over their node family. Parent, child,
  root, traversal, lookup, and conversion APIs now preserve specialized node
  types, and tree subclasses can configure `node_type` for subclass-preserving
  deserialization.
- Made `TreeNode.children` an immutable sequence, made `TreeNode.add` return the
  added node, and rejected cycles, implicit reparenting, and attaching a root
  already owned by another tree.
- Added lazy transformation revision tracking for graph and volmesh view-coordinate
  caches. Changing a local or ancestor transformation now refreshes coordinates
  computed from the underlying data without eagerly walking the scene subtree.
- Explicitly assigned view-coordinate mappings remain caller-controlled and are
  not recomputed when an ancestor changes.
- Migrated all `compas.scene` docstrings to MkDocs-compatible NumPy style,
  documented public properties on their getters, and removed stale constructor
  parameters, attribute inventories, and visualization-context references.
- Typed the scene registry, color descriptors, factory selection, item accessors,
  context identifiers, and abstract drawing methods. Broad `Any` remains only
  at open-ended scene setting and serialized-payload boundaries.
- Made scene color descriptors return themselves during class-level access.
  Assigning a `ColorDict` now preserves its default color, and assigning an
  empty mapping clears existing per-item colors.
- Kept `sceneobject_type` as a construction-time factory override without
  exposing it as scene-object initialization state.
- Added `SceneObject.invalidate()` as the explicit cache invalidation path for
  mutations of underlying items that scene objects cannot observe directly.

## Standard library mapping ABCs

- Removed the vendored `compas.datastructures._mutablemapping` implementation,
  which existed only to avoid ABC metaclasses on IronPython 2.7. Production
  mapping types already use `collections.abc` directly.
- Removed tests that duplicated standard-library `MutableMapping` behavior.
- Audited the principal COMPAS base classes for conversion to ABCs. Kept
  `Datastructure`, `Geometry`, `Curve`, `Surface`, `Brep`, and `SceneObject`
  non-abstract because their `NotImplementedError` methods represent a mixture
  of optional capabilities and factory dispatch rather than one minimal
  mandatory subclass contract.

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
- Consolidated shared PLY domain declarations such as formats, data types,
  byte order, scalar values, and records in `ply_types.py`, while reusing the
  generic `_iotools` source and target aliases for I/O.
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

### STL

- Replaced the stateful legacy `STL` facade with the aligned `STLReader`,
  `STLParser`, `STLDocument`, and `STLWriter` pipeline.
- Added `read_stl()` and `write_stl()` convenience functions for ASCII and
  binary STL using shared path and stream I/O, while preserving solid names,
  binary headers, facet normals, and binary attribute values.
- Added strict document validation and parsing for facet structure, coordinate
  dimensions, incomplete ASCII input, binary facet counts, and exact binary
  payload sizes. Binary files whose header starts with `solid` are detected by
  their declared facet count rather than by the header text.
- Added identity-preserving `stl_data()` and explicit `weld_stl_data()` mesh
  projections. `Mesh.from_stl()` requests welding explicitly because STL stores
  independent facet vertices, while parsing itself no longer merges geometry.
- Applied numeric precision only during ASCII serialization, retained document
  formats by default, and stopped translating negative coordinates during
  writing.
- Added separated reader, parser, document, writer, malformed-input, stream,
  welding, and ASCII and binary mesh roundtrip tests.

### glTF

- Removed postponed-annotation and other legacy Python compatibility syntax
  from the glTF package, using explicit forward references where required.
- Removed JSON-oriented `to_data()` and `from_data()` methods from glTF
  semantic objects. `GLTFParser` now owns JSON decoding and `GLTFEncoder` owns
  JSON construction and index remapping, leaving document objects focused on
  semantic content, validation, editing, and COMPAS conversions.
- Converted passive glTF semantic and extension values to Python dataclasses.
  Document, scene, node, and mesh entities retain explicit constructors because
  they allocate keys and establish validated document relationships.
- Added complete scene conversion with `Scene.from_gltf()` and
  `Scene.to_gltf()`. The adapter preserves node hierarchy and local
  transformations, converts meshes, point clouds, lines, and polylines, expands
  all glTF line and triangle topology modes, and warns when unsupported COMPAS
  scene items are omitted from glTF geometry.
- Added explicit, symmetric primitive conversion functions for glTF points,
  lines, line strips and loops, triangles, triangle strips and fans, and their
  closest COMPAS mesh, point-cloud, line, and polyline equivalents.
- Introduced an explicit source-to-document pipeline: `GLTFReader` now only
  acquires primary bytes and configures relative resource loading, while
  `GLTFParser` owns JSON and GLB decoding, resource resolution, accessor
  decoding, and semantic document construction.
- Added typed `GLTFSource`, filesystem and URL resource loaders, strict JSON and
  GLB container parsing, and dedicated buffer, buffer-view, data-URI, sparse,
  interleaved, and normalized accessor decoding.
- Added `GLTFDocument` as the semantic document and scene-editing model.
- Added non-mutating `GLTFEncoder`, structured `GLTFPayload`, and `GLTFWriter`
  layers, plus `read_gltf()` and `write_gltf()` convenience functions. JSON
  glTF resources are written adjacent to path targets, and GLB output is
  supported for paths and binary streams.
- Removed the stateful `GLTF` facade in favor of `read_gltf()` and
  `write_gltf()`.
- Removed remaining IronPython buffer-packing compatibility and fixed matrix
  accessor packing to select padding from the accessor type.
- Added separated reader, container, parser, encoder, writer, resource,
  non-mutation, external-buffer, stream, JSON glTF, and GLB roundtrip tests.
- Modernized the semantic document core (`GLTFDocument`, `GLTFScene`,
  `GLTFNode`, `GLTFMesh`, and `GLTFChildren`) with Python 3.12 type
  annotations and MkDocs-oriented docstrings, and removed the obsolete
  executable example embedded in `gltf_content.py`.
- Added whole-document validation for scene, node, mesh, camera, and skin
  references, multiple node parents, and hierarchy cycles. Parsing and encoding
  now validate semantic content explicitly.
- Added `without_orphans()` for non-destructive cleanup. Encoding operates on
  the cleaned copy rather than modifying the caller's scene graph.
- Fixed `GLTFChildren.pop(0)`, `index()`, and `count()` return behavior, corrected
  node skin lookup to use the document's skin collection, and made animation
  and skin cleanup safe while filtering collections.
- Added semantic document tests for child-sequence behavior, skin references,
  cyclic and multiply-parented hierarchies, and non-mutating orphan cleanup.
- Modernized material, texture, image, camera, animation, skin, primitive, and
  supported-extension data classes with typed construction and serialization,
  modern `super()` usage, and explicit recursive semantic traversal.
- Removed the IronPython-only semantic marker attributes and replaced
  reflection through `dir()` with `iter_data()` and `extension_keys()`.
- Fixed material serialization keys for occlusion textures and alpha cutoff,
  preserved explicit zero glossiness, remapped skin skeleton keys during
  serialization, and omitted absent primitive index accessors.
- Preserved asset metadata, required versus used extensions, and unknown
  top-level properties across semantic roundtrips.
- Extended validation to materials, textures, images, samplers, primitive
  modes and indices, animation targets and interpolation, skins, cameras, asset
  versions, and required-extension declarations.
- Merged JSON and binary construction directly into `GLTFEncoder` and removed
  the redundant encoding-state and legacy `GLTFExporter` classes.
- Added automatic 32-bit index accessors for large meshes, four-byte buffer-view
  alignment, padded matrix accessor decoding, and normalized non-sparse
  accessor decoding.
- Added regression tests for specification property names, skin remapping,
  nested extensions, metadata preservation, deterministic encoding, large
  indices, padded matrices, normalized accessors, and invalid strides and
  references.
- Removed unused alpha-mode and MIME-type containers, the unused component-size
  table, duplicate orphan cleanup and hierarchy checks during encoding, and the
  `GLTFContent` alias module. Updated tests to use only the explicit document
  pipeline instead of private exporter state.

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

## Geometry

### General

- Modernized the geometry package for Python 3.12 with explicit annotations,
  subclass-preserving `Self` return types, overloads for argument-dependent
  results, modern `super()` calls, and MkDocs-compatible NumPy-style docstrings.
- Removed the remaining IronPython, Python 2, and old-CPython compatibility
  paths, postponed-annotation imports, legacy type comments, and geometry
  `DATASCHEMA` declarations.
- Added shared structural coordinate and transformation protocols. Public
  geometry APIs accept the representations supported at runtime, while the
  low-level `_core` functions remain typed against raw numerical structures and
  do not depend on geometry classes.
- Standardized geometry properties and setters, documenting when coordinate,
  point, vector, plane, and frame inputs are copied and ensuring mutable input
  objects are not retained unexpectedly.
- Increased unit and doctest coverage throughout the geometry primitives,
  parametric curves, intersections, and analytic surfaces, including subclass
  construction, transformed coordinate systems, overloads, and boundary cases.
- Organized the root `Geometry`, `Pointcloud`, `KDTree`, and
  `IntersectionResult` class members into the shared section order, including
  moving point-cloud bounding and centroid queries out of the property group.
- Aligned the optional rotation-point annotations of `Geometry.rotate`,
  `Geometry.rotated`, and `Rotation.from_axis_and_angle` with their existing
  origin-defaulting behavior.
- Organized `Brep` and its vertex, edge, trim, loop, and face interfaces into
  the shared class-member sections without changing the operation-level plugin
  contract. Moved boolean operators beside the other dunder methods and
  corrected their operand descriptions.
- Organized `Scene`, `SceneObject`, `Group`, and the geometry, graph, mesh, and
  volmesh scene-object adapters into the shared class-member sections. Cache
  invalidation hooks now live with private helpers while remaining available to
  subclasses through the same override contract.
- Completed the class-member organization of `Polygon`, `Polyline`, and
  `Polyhedron`. Removed the empty polyline constructor section, grouped bounding
  box queries with regular methods, and moved polyhedron boundary validation to
  its private-helper section.
- Completed the repository-wide class-organization audit, removed residual
  empty sections, and standardized private-helper section names.
- Rewrote `AGENTS.md` as a forward-looking guide for Python 3.12+, current
  typing and documentation conventions, class organization, geometry
  architecture, and validation. Removed migration history and obsolete
  compatibility-oriented instructions.

### Linear algebra separation

- Removed general vector, matrix, quaternion, decomposition, solver, and
  transformation algebra from `compas.geometry._core`. Geometry now imports
  these operations from the dedicated `compas.linalg` package described below.
- Kept `_core` focused on geometry-specific numerical algorithms such as
  angles, centroids, distances, normals, predicates, sizes, tangents, and NURBS
  helpers.

### Primitives

- Modernized `Point`, `Vector`, `Frame`, and `Plane` with complete typing,
  documented arithmetic and sequence behavior, constructor examples, explicit
  three-coordinate contracts, and independent-copy setter semantics.
- Documented all primitive properties and the behavior of forward, reflected,
  and in-place arithmetic operators. Point and vector constructors continue to
  accept integer coordinate values through float conversion but no longer
  advertise strings as valid coordinates.
- Reworked shared coordinate protocols to describe indexable, iterable
  three-component data without unnecessary runtime list allocation or casts.
- Made `Line` and `Polyline` lightweight geometry primitives instead of
  subclasses of `Curve`, and moved them out of `compas.geometry.curves` to
  `compas.geometry.line` and `compas.geometry.polyline`. The old curve-package
  import paths were removed.
- Modernized line and polyline construction, properties, evaluation, length,
  transformations, and documentation. Inputs to properties such as
  `line.point` create independent geometry values.

### Curves

- Simplified `Curve` into the common parametric-curve contract used by analytic
  curves and plugin-backed NURBS implementations, with typed domains,
  evaluation, frames, tangents, normals, curvature, closest-point queries,
  discretization, and native conversion boundaries.
- Modernized `Arc`, `Bezier`, `Circle`, `Ellipse`, `Hyperbola`, `Parabola`, and
  `NurbsCurve`, including constructor examples, property documentation,
  argument-controlled overloads, stricter invariant validation, and expanded
  behavioral tests.
- Removed primitive `Line` and `Polyline` from the curve inheritance hierarchy.
  Dedicated `LineCurve` and `PolylineCurve` wrappers may be introduced later
  where a full parametric curve object is required.
- Restricted frame-valued curve inputs to actual `Frame` objects and moved
  reusable path and typing aliases out of the `Curve` class.

### Intersections

- Added `IntersectionResult`, an immutable result container with geometry,
  point, and line accessors, and introduced the predefined `intersection`
  dispatcher for computing intersections by geometry-type pairs.
- Added a symmetric `Intersection` registration mechanism with reversed-argument
  dispatch and method-resolution-order fallback. Registered initial line-line,
  line-plane, and plane-plane implementations.
- Modernized the free intersection functions with explicit input and return
  types, overloads, consistent three-dimensional input validation, and retained
  XY-specific contracts for explicitly two-dimensional helpers.
- Removed intersection methods from `Plane` and `Surface` so intersection logic
  has one dedicated home, and retained mesh/mesh and ray/mesh extension points
  for backend implementations.
- Fixed segment typing in XY point predicates and slice-related typing in
  intersection calculations without broadening the numerical `_core` APIs to
  geometry object types.

### Surfaces

- Modernized `Surface` state, frame copying, transformations, domains,
  discretization, native conversion, evaluation, isocurves, boundaries, and
  closest-point overloads. Direct frame mutation now updates transformations
  without a stale cache.
- Removed conflicting `Surface.aabb()` and `Surface.obb()` methods in favor of
  the standard `Geometry` bounding-box properties and `compute_aabb()` and
  `compute_obb()` implementation hooks.
- Removed unimplemented generic OBJ, STEP, intersection, and inconsistent
  curvature placeholders from the base surface API. Backend-supported STEP and
  BREP conversion hooks remain where their contracts are meaningful.
- Modernized `PlanarSurface`, `SphericalSurface`, `CylindricalSurface`,
  `ConicalSurface`, and `ToroidalSurface` with typed properties, serialization,
  subclass-preserving constructors, analytic point and normal evaluation,
  frames, isocurves, area and volume formulas, and transformed-coordinate tests.
- Fixed planar frame origins, spherical meridian isocurves, cylindrical
  generator domains and frames, and completed the previously partial cone and
  torus analytic implementations. Regular cylinders and cones require positive
  dimensions, and `ToroidalSurface` represents regular ring tori.
- Removed the empty, unreferenced `extrusion` and `revolution` surface modules.

### Shapes

- Modernized the shared `Shape` discretization, conversion, transformation,
  containment, and bounding-box contracts. Cached topology and bounds are now
  invalidated when frames, resolutions, or dimensions change.
- Kept `Box` as an ordinary solid shape and separated it from bounding-box
  calculation: bounding-box functions continue to return corner coordinates,
  while `Box.from_bounding_box()` provides the explicit conversion to a shape.
- Removed the misleading `Box.xmin`, `xmax`, `ymin`, `ymax`, `zmin`, and `zmax`
  properties, which were incorrect for rotated boxes. `Pointcloud.from_box()`
  now samples in the box's local coordinates and therefore supports boxes in
  arbitrary frames.
- Made `Box.corner(index)` use the same canonical ordering as `Box.points`.
- Modernized `Capsule` and decoupled its topology computation from transformed
  vertex generation. Fixed its circle construction and containment checks for
  capsules placed in arbitrary frames.
- Modernized `Cone`, decoupled topology from vertex generation, added point
  containment, and aligned its positive dimensions with `ConicalSurface`.
  `Cone.from_line_and_radius()` now correctly uses the line start as the base
  and the line end as the apex.
- Modernized `Cylinder`, decoupled topology from vertex generation, and aligned
  its positive dimensions with `CylindricalSurface`. The shape frame remains at
  the solid center, while `base`, `plane`, `circle`, and `axis` now consistently
  describe the lower base and the full cylinder axis. Consequently,
  `Cylinder.from_circle_and_height()` now treats its circle as the lower base.
- Modernized `Torus`, added arbitrary-frame containment, reliable bound
  invalidation, and atomic uniform scaling. Its dimension constraints now match
  `ToroidalSurface`: only regular ring tori with a positive axis radius larger
  than the positive pipe radius are supported.
- Modernized `Sphere`, decoupled topology from vertex generation, and aligned
  its positive radius with `SphericalSurface`. Removed the ambiguous constructor
  `point` parameter; use `Sphere.from_point_and_radius()` to place a sphere by
  its center. Updated boolean and polyhedron consumers.

### Polygonal geometry

- Added `PolygonalSurface` as a lightweight indexed polygon representation for
  geometry algorithms and visualization without persistent half-edge topology.
  It owns and validates vertex and face data, provides geometric views,
  transformations, bounds, area, mesh conversion, and closure, manifoldness,
  and orientability queries. This is the first step toward reserving
  `Polyhedron` for validated closed polygonal solids.
- Added `Shape.to_polygonal_surface()` and `Surface.to_polygonal_surface()` as
  the explicit lightweight tessellation path for closed shapes and parametric
  surface domains. Existing `to_polyhedron()` methods remain temporarily while
  downstream consumers are migrated.
- Removed `Surface.to_polyhedron()` because a discretized parametric domain is
  generally open and therefore not a polyhedron. Use
  `Surface.to_polygonal_surface()` instead. Migrated the former open-quadrilateral
  `Polyhedron` test to the lightweight representation.
- Redefined `Polyhedron` as a closed polygonal solid composed with a
  `PolygonalSurface` boundary. Construction now requires a closed, manifold,
  consistently oriented boundary with planar faces and nonzero volume;
  consistently inward boundaries are normalized to outward orientation.
  Implemented volume and solid centroid properties and delegated lightweight
  boundary geometry, transformations, bounds, and mesh conversion to the
  polygonal boundary.
- Consolidated polyhedron closure, manifoldness, orientability, and orientation
  validation into one topology analysis pass instead of rebuilding incidence
  maps for every check. The validated signed volume is retained and refreshed
  by transformations; collapsing transformations are rejected without mutating
  the solid.
- Replaced the former custom ear-clipping implementation with Mapbox Earcut.
  `PolygonalSurface` and `Polyhedron` now use the shared adapter for robust
  triangulation of concave planar faces while preserving face orientation.
  Mesh conversion can request triangles explicitly, and all polyhedron boolean
  operators and methods guarantee triangular inputs to lower-level backends.
- Added `PlanarRegion` for a planar exterior boundary with optional holes. It
  provides area, transformation, serialization, bounding boxes, and conversion
  to indexed triangles, `PolygonalSurface`, and `Mesh`. Region triangulation
  flattens the exterior vertices followed by the vertices of each hole.
  Construction performs only inexpensive boundary-size and coplanarity checks;
  tessellation uses Shapely to reject self-intersections, degenerate loops,
  holes outside or touching the exterior, and holes that overlap, touch, or
  contain one another before passing valid boundaries to Mapbox Earcut.
- Added `Tessellation` as the shared indexed triangular result for geometry
  visualization.
  It retains Python, NumPy, or compatible native buffers without conversion and
  can carry per-vertex normals, texture coordinates, and independent boundary
  polylines. All per-vertex attributes share one index domain, so seams are
  represented by duplicated vertices and the buffers map directly to common
  mesh and GPU layouts. Shapes, surfaces, polygons, planar regions, polygonal
  surfaces, and polyhedra now provide `tessellated()`. Direct `to_mesh()` and
  `to_polygonal_surface()` conversions preserve the polygonal topology of the
  source conversion, whereas converting a `Tessellation` produces triangular
  geometry. Shapes and surfaces expose their polygonal parametric
  representation through cached `vertices`, `edges`, and `faces` properties,
  with `points`, `lines`, and `polygons` as geometry-object views. Public
  `compute_vertices()`, `compute_edges()`, and `compute_faces()` methods provide
  uncached computation. Here, discretisation means resolution-dependent
  sampling that retains the natural polygonal topology; tessellation means the
  separate conversion to indexed triangles, with rendering attributes where
  available. Resolution and geometric parameter changes invalidate the full
  discretisation. Placement changes invalidate only world-space vertices:
  shapes reuse cached local vertices and topology, and surfaces preserve their
  cached topology. Triangles exist only in the result of `tessellated()` and
  are not stored as a parallel shape or surface representation. Per-call
  resolution overrides remain non-mutating, and results of
  `to_vertices_and_faces()` cannot mutate cached topology. Surface tessellation
  additionally generates aligned analytic normals, normalized UVs, and
  consistently oriented triangles.
- Renamed the NURBS surface defining-point grid from `points` to
  `control_points`. This leaves `Surface.points` consistently available for
  the sampled polygonal representation and makes the V-by-U NURBS contract
  explicit as `control_points[v][u]`.
- Removed `Shape.to_polyhedron()`. `Polyhedron` is a validated closed solid, not
  the generic polygonal representation of a discretized shape. Use
  `Shape.to_polygonal_surface()`, `Shape.tessellated()`, or `Shape.to_mesh()`.
- Modernized `Polygon` as the single-boundary counterpart to `PlanarRegion`.
  Its public API is typed, its documentation uses the MkDocs conventions,
  transforms invalidate derived lines and bounds, and ear-clipped conversion no
  longer stores triangulation results as mutable polygon state.

## Linear algebra

- Introduced `compas.linalg` as the dedicated home for general-purpose linear
  algebra that was previously mixed into `compas.geometry._core`,
  `compas.linalg.py`, and `compas.matrices.py`.
- Added focused `vectors`, `matrices`, `operators`, `quaternions`,
  `transformations`, `decompositions`, and `solvers` modules with a consolidated
  public API in `compas.linalg`.
- Moved matrix construction and manipulation, vector arithmetic, quaternion
  operations, transformation helpers, matrix decompositions, and linear-system
  solvers to the new package and updated geometry, datastructure, file, and
  Blender consumers to use it.
- Removed the old top-level `compas.linalg` module, `compas.matrices` module,
  geometry `_algebra` module, and geometry `_core.quaternions` module. Imports
  should now target the corresponding `compas.linalg` package API.
- Kept numerical behavior stable during the package move and migrated the
  existing matrix tests to the new module layout. Known numerical edge cases
  requiring behavioral decisions remain documented for dedicated follow-up
  work.

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
- Added Python 3.12 annotations throughout serialization,
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
- Added Python 3.12 annotations throughout the `Mesh` class, mesh
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
- Added Python 3.12 annotations throughout serialization,
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
- Added Python 3.12 annotations throughout serialization,
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
