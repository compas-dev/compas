# Modernization TODO

This is the repository's lightweight modernization backlog. Add tasks to
**Inbox** whenever they come up, without assigning priority or making them the
next piece of work. Move an item to **Next** only when it is intentionally
selected for implementation.

Keep entries short and outcome-oriented. Link to an issue, design note, or
section of `AGENTS.md` when a task needs more context.

## Next

_No task currently selected._

## Inbox

- [ ] Define a geometry fingerprint and revision protocol for mutable COMPAS
  objects and backend-native geometry. Separate intrinsic geometry,
  placement, topology, and discretisation keys so caches can invalidate only
  affected results. Use deterministic equality-comparable keys for cache
  correctness; reserve Python `__hash__` for genuinely immutable objects and
  derive compact hashes only as an optional lookup optimization.
- [ ] Complete the shared `Tessellation` migration. Add Brep and backend integration,
  analytic normals and UVs for shapes, explicit seam and pole handling, a
  reliable geometry-revision contract for position caching, and contiguous
  NumPy/GPU buffer support. Parametric surfaces already provide aligned
  positions, analytic normals, and normalized UVs. Shape and surface polygonal
  representations are cached independently by resolution, while triangles
  belong only to `Tessellation` results.
- [ ] Add conversions from relevant primitive and polygon geometry to `Mesh`
  and `Brep`.
- [ ] Define a reliable mutation or geometry-revision contract for mutable
  datastructures before using revision-keyed caches. Account for public storage
  dictionaries and mutable `AttributeView` objects, which currently bypass
  public mutation methods; do not add counters that cover only some mutation
  paths. Until then, provide an explicit cache invalidation path where needed.
- [ ] Add conversions from `Mesh` to edge graphs, face graphs, and other useful
  topology-derived graphs.
- [ ] Add coherent bidirectional conversion between `Mesh` and `Brep`.
- [ ] Evaluate `cadquery-ocp-novtk`, or another pip-installable OpenCascade
  binding, as a replacement for `pythonocc-core`.
- [ ] Make NumPy the default representation where it materially improves
  geometry processing, storage, or interoperability, including revisiting
  NumPy-backed vertex storage for `PolygonalSurface` and the future GPU-buffer
  API.
- [ ] Minimize data conversions between COMPAS, viewers, C++ backends, and
  plugin-provided kernels; investigate direct access to shared NumPy buffers.
- [ ] Migrate the other core packages to the revised plugin contract and
  coordinate a full framework audit across `compas_occ`,
  `compas_cgal`, `compas_libigl`, `compas_shapeop`, `compas_gmsh`,
  `compas_model`, and `compas_viewer`. Include pluggable signature and return
  contracts, keyword forwarding, renamed entry points, backend discovery,
  optional dependency boundaries, and avoidable data conversions. Verify the
  triangle-mesh mass-matrix, curvature, remeshing, slicing, isoline, and
  parametrization contracts as part of that audit.
- [ ] Introduce ABCs only for future extension points with a small, mandatory
  runtime contract. Do not convert `Datastructure`, `Geometry`, `Curve`,
  `Surface`, `Brep`, or `SceneObject` wholesale: they currently mix concrete
  base behavior, factory dispatch, and optional capabilities. Prefer protocols
  for structural typing and define focused ABCs alongside the planned Brep,
  NURBS, and plugin API redesigns. The obsolete vendored mapping ABCs have been
  removed.
- [ ] Audit public API naming for consistency across geometry,
  datastructures, serialization, conversions, and scene functionality. Treat
  renames as coordinated breaking changes with updated consumers and docs.
- [ ] Complete the geometry typing and docstring pass outside the already
  modernized modules. Prioritize `Brep` and its component interfaces, and
  coordinate that work with the planned pluggable-operation design above.
- [ ] Finish the residual datastructure documentation migration. Runtime
  typing is substantially complete, but legacy Sphinx markup remains in mesh,
  graph, cell-network, and volmesh docstrings.
- [ ] Finish the residual file-format modernization, especially the untyped
  glTF helper functions and remaining partially annotated glTF document APIs.
- [ ] Audit migrated guides and examples for stale public imports and removed
  APIs, including moved modules and renamed NumPy-backed functions.

## Done

Completed work remains documented in `CHANGES.md`; move finished items there
rather than maintaining a second changelog here.
