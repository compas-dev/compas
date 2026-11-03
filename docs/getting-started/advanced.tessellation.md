# Geometry Discretization and Tessellation

COMPAS uses explicit verbs and result types for approximating continuous geometry.
The distinction matters because a sampled surface, a triangle buffer, and an editable
half-edge mesh have different guarantees and costs.

## Terminology

| Operation | Meaning |
| --- | --- |
| Sampling | Evaluate points, tangents, normals, or other quantities on continuous geometry. |
| Discretization | The broad category of operations that produce a finite representation of continuous geometry. |
| Polygonization | Apply `polygonize(strategy)` to continuous defining geometry and produce a persistent `PolygonalSurface`, retaining polygonal topology where possible. |
| Tessellation | Apply `tessellate(strategy)` to continuous defining geometry and produce an ephemeral, indexed `Tessellation` made exclusively of triangles. |
| Triangulation | Split existing polygonal faces, or construct a planar triangle complex from points and constraints. |
| Refinement | Add resolution while preserving the represented domain and constraints. |
| Remeshing | Reconstruct an existing mesh to improve element size, shape, or distribution. |

Continuous defining geometry uses `polygonize(strategy)` and `tessellate()` or
`tessellate(strategy)`. Shape and Surface tessellation has a deterministic
default; polygonization and BRep tessellation require an explicit strategy.
Already polygonal geometry instead uses
`triangulate(strategy)` for in-place mutation or `triangulated(strategy)` for an
ephemeral triangle result. Refinement and remeshing are processing operations;
they are not synonyms for tessellation.

## Choose the result representation

| Type | Role | Serialized | Topology |
| --- | --- | --- | --- |
| `Tessellation` | Short-lived rendering and triangle-processing input | No | Indexed triangles, optional aligned attributes and boundary polylines |
| `PolygonalSurface` | Lightweight persistent polygonal geometry | Yes | Indexed polygonal faces |
| `Mesh` | Persistent editable data structure | Yes | Half-edge topology and attributes |

Use `Tessellation` when the next operation consumes triangle buffers. Convert it
with `to_polygonal_surface()` or `to_mesh()` when an independent persistent object
is required.

## Polygonize and tessellate a surface

Strategies are immutable `compas.data.Data` configurations. Grid counts are positive
integers. Angular values use degrees at the public API boundary; linear values use
the model's units.

```python
from compas.geometry import FaceTriangulation
from compas.geometry import PlanarSurface
from compas.geometry import UVGrid

surface = PlanarSurface(xsize=4.0, ysize=2.0)
strategy = UVGrid(u=8, v=4)

polygonal = surface.polygonize(strategy)
tessellation = surface.tessellate(strategy)
default_tessellation = surface.tessellate()  # equivalent to UVGrid(64, 64)

# Triangulation is also explicit when starting from polygonal geometry.
triangulated = polygonal.triangulated(FaceTriangulation())
```

The two triangle results need not have identical indexing. They do have the same
representation contract: exactly three valid indices per face and finite 3D vertex
coordinates.

## Strategies

`Native` requests fixed natural topology. `UGrid` and `UVGrid` request parameter-grid
sampling. `Deflection` supplies linear and angular targets, and `Adaptive` supplies
one or more of maximum deviation, normal angle, and edge length. A producer implements
only the strategies appropriate to its geometry. Producers validate the
supplied strategy directly and raise `TypeError` or `ValueError` when it is not
supported. Supported strategies are documented with each producer:

```python
from compas.geometry import PlanarSurface
from compas.geometry import UVGrid

surface = PlanarSurface()
result = surface.tessellate(UVGrid(16, 8))
```

An omitted Shape or Surface tessellation strategy uses a fixed core default:

| Geometry | Default strategy |
| --- | --- |
| `Box` | `Native()` |
| `Cylinder`, `Cone` | `UGrid(64)` |
| `Sphere`, `Torus`, `Capsule` | `UVGrid(64, 64)` |
| every `Surface` | `UVGrid(64, 64)` |

Grid values count cells, not sample points. Defaults are resolved for each
operation and are neither stored nor cached. `polygonize(strategy)` remains
explicit because its result is persistent. `Brep` and `BrepFace` tessellation
also remain explicit because their deflection targets have no universal default.

Deflection and adaptive values are requests, not proof of achieved error.
Enriched results containing provenance and measured-error reports are deliberately
deferred; the current operation result is `Tessellation` itself.

## Triangulate polygonal geometry and planar domains

`EarClipping` triangulates an existing planar polygon or `PlanarRegion` without
inserting free interior vertices. It supports holes and preserves the supplied
boundary vertices. Constrained Delaunay triangulation instead constructs a planar
domain triangulation and requires a plugin implementation of
`triangulate_planar_domain()`.

```python
from compas.geometry import ConstrainedDelaunay
from compas.geometry import EarClipping
from compas.geometry import PlanarRegion
from compas.geometry import triangulate_planar_domain

outer = [[0, 0, 0], [4, 0, 0], [4, 4, 0], [0, 4, 0]]
hole = [[1, 1, 0], [1, 3, 0], [3, 3, 0], [3, 1, 0]]

region = PlanarRegion(outer, holes=[hole])
local = region.triangulated(EarClipping())

# With a constrained-triangulation plugin such as compas_cgal installed:
domain = triangulate_planar_domain(
    outer,
    holes=[hole],
    strategy=ConstrainedDelaunay(),
)
```

Use ear clipping for a faithful split of an existing face. Use constrained Delaunay
when constraints, interior points, or later quality refinement are part of the
problem.

For a slightly warped polygon, projection must be explicit and bounded:

```python
from compas.geometry import FaceTriangulation
from compas.geometry import PolygonalSurface
from compas.geometry import ProjectedEarClipping

surface = PolygonalSurface(
    [[0, 0, 0], [2, 0, 0.01], [2, 2, 0], [0, 2, -0.01]],
    [[0, 1, 2, 3]],
)
strategy = FaceTriangulation(
    quad=ProjectedEarClipping(max_deviation=0.01),
    ngon=ProjectedEarClipping(max_deviation=0.01),
)
tessellation = surface.triangulated(strategy)
```

`ProjectedEarClipping` uses a best-fit plane, rejects vertices beyond the maximum
deviation, and rejects degenerate or self-intersecting projections. It returns
indices into the original 3D vertices and never inserts vertices.

For a heavily twisted ordered 3D boundary that should not be projected, use the
minimum-area dynamic program explicitly:

```python
from compas.geometry import FaceTriangulation
from compas.geometry import MinimumAreaTriangulation
from compas.geometry import PolygonalSurface

surface = PolygonalSurface(
    [[0, 0, 0], [2, 0, 1], [3, 1, -1], [2, 3, 2], [0, 2, -1]],
    [[0, 1, 2, 3, 4]],
)
strategy = FaceTriangulation(
    quad=MinimumAreaTriangulation(),
    ngon=MinimumAreaTriangulation(),
)
tessellation = surface.triangulated(strategy)
```

`MinimumAreaTriangulation` minimizes total triangle area using only the boundary
vertices. It takes $O(n^3)$ time and $O(n^2)$ space. The result is a
combinatorially manifold disk, but it is not guaranteed to be geometrically
intersection-free. [^barequet-sharir]

[^barequet-sharir]: G. Barequet and M. Sharir, “Filling gaps in the boundary of a
    polyhedron,” *Computer Aided Geometric Design* 12(2), 1995.
    <https://doi.org/10.1016/0167-8396(94)00011-G>

## Pass tessellations to geometry plugins

Triangle-processing plugin boundaries accept `Tessellation`, not raw
`(vertices, faces)` tuples or `Mesh`. This keeps one validation and ownership
contract across backends.

```python
from compas.geometry import Native
from compas.geometry import Sphere
from compas.geometry import UVGrid
from compas.geometry import Box
from compas.geometry import boolean_difference_mesh_mesh

box = Box(2.0).tessellate(Native())
sphere = Sphere(1.25).tessellate(UVGrid(u=32, v=16))
result = boolean_difference_mesh_mesh(box, sphere)
```

The selected plugin remains authoritative for its algorithm. The same rule applies
to CGAL and libigl triangle-processing operations: callers pass a validated
`Tessellation`, and receive the documented result type.

## Trims, seams, singularities, and validation

A tessellator must respect trimmed domains. BRep tessellations may expose sampled
trim and edge boundaries through `Tessellation.polylines`. Periodic seams and
parametric singularities may require duplicate vertices. Normals and texture
coordinates share vertex indexing, so a producer duplicates a vertex at a normal or
texture seam rather than introducing a second index buffer.

Construction validates coordinate dimensions and finiteness, triangle arity and
index range, and alignment of normals and texture coordinates. Domain operations
add their own geometric checks: planarity, simple boundary loops, valid hole
containment, and non-intersection where applicable.

`Tessellation` retains supplied buffers without copying or converting them. This
permits Python sequences, NumPy arrays, and compatible native buffers. Producers own
buffers they create; callers must treat all buffers as immutable for the lifetime of
the tessellation. `to_polygonal_surface()` and `to_mesh()` create independent
COMPAS objects.

## Migration from pre-3.0 APIs

COMPAS 3 intentionally has no compatibility aliases for the removed legacy
conversion methods. Make the desired operation and representation explicit,
and provide a strategy whenever the default tessellation density is not
appropriate.

| Removed or old pattern | COMPAS 3 replacement |
| --- | --- |
| `to_tessellation()`, `to_tesselation()`, `compute_tessellation()` | `tessellate()` or `tessellate(strategy)` |
| `to_viewmesh()` for display triangles | `tessellate()` or `tessellate(strategy)` |
| `to_polygonal_surface()` or backend-specific mesh conversion from continuous geometry | `polygonize(strategy)` |
| Positional `u`, `v`, or resolution arguments | `UGrid(u)` or `UVGrid(u, v)` |
| Backend-specific tolerance arguments | `Deflection(linear, angular)` or a supported `Adaptive(...)` |
| `quads_to_triangles()` and implicit diagonal selection | `triangulate(FaceTriangulation(...))` or `triangulated(...)` |
| `to_vertices_and_faces(triangulated=True)` | `triangulated(strategy).to_vertices_and_triangles()` |
| Raw `(vertices, faces)` triangle-plugin input | `Tessellation(vertices, triangles)` |
| Planar Delaunay entry points | `triangulate_planar_points(..., strategy=Delaunay())` or `triangulate_planar_domain(...)` |

In-place `triangulate(strategy)` returns `None`. Non-mutating
`triangulated(strategy)` returns a `Tessellation`. Polygonization and tessellation
never imply remeshing or refinement.
