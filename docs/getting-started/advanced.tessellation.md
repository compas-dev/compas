# Geometry Discretization and Tessellation

COMPAS separates structured polygonization, triangulation of existing discrete
geometry, and precision-controlled BRep tessellation. The operations produce
related representations, but their controls and guarantees are different.

## Choose the result representation

| Type | Role | Serialized | Topology |
| --- | --- | --- | --- |
| `Tessellation` | Short-lived rendering and triangle-processing result | No | Indexed triangles with optional aligned attributes and boundary polylines |
| `PolygonalSurface` | Lightweight persistent polygonal geometry | Yes | Indexed polygonal faces of arbitrary arity |
| `Mesh` | Persistent editable data structure | Yes | Half-edge topology, keys, and attributes |

## Structured shapes and surfaces

Shapes and untrimmed surfaces convert to a polygonal representation through
producer-owned resolution keywords. `nu` and `nv` count cells in the relevant
parameter directions; they are not geometric error bounds.

```python
from compas.geometry import PlanarSurface
from compas.geometry import Sphere

surface = PlanarSurface(xsize=4.0, ysize=2.0)
polygonal = surface.to_polygonal_surface(nu=8, nv=4)
triangles = surface.to_tessellation(nu=8, nv=4)

sphere = Sphere(1.0)
sphere_triangles = sphere.to_tessellation(nu=32, nv=16)
```

`to_tessellation(...)` uses exactly the vertices and triangle topology of
`to_polygonal_surface(...).triangulated()` with the same arguments. Surface
normals and texture coordinates are included when one aligned value exists for
each polygonized vertex.

Default resolutions are:

| Producer | Default controls |
| --- | --- |
| `Box` | Natural six-face topology |
| `Cylinder`, `Cone` | `nu=64` |
| `Sphere`, `Torus`, `Capsule` | `nu=64, nv=64` |
| untrimmed `Surface` | `nu=64, nv=64` |

## Triangulate discrete geometry

Named functions select polygon algorithms. Aggregate `triangulated` methods
accept any callable with the same structural contract. An omitted selector or
explicit `None` uses `triangulate_polygon`.

A callable returns exactly $n - 2$ nondegenerate triangles for an $n$-vertex
face. Indices refer to the ordered source vertices, every source boundary edge
appears once with the same direction, and every interior edge appears twice in
opposite directions. Aggregate operations validate this result before creating
or mutating topology.

```python
from functools import partial

from compas.geometry import Polygon
from compas.geometry import triangulate_polygon_projected

polygon = Polygon([[0, 0, 0], [2, 0, 0], [2, 2, 0.01], [0, 2, 0]])
triangulator = partial(triangulate_polygon_projected, max_deviation=0.02)
result = polygon.triangulated(triangulator)
```

The public polygon operations are:

- `triangulate_polygon` for the default arity-based behavior;
- `triangulate_quadrilateral` for explicit diagonal selection, with
  `"shortest"` choosing the shortest valid interior diagonal;
- `triangulate_polygon_earclip` for planar polygons;
- `triangulate_polygon_projected` for bounded near-planar projection; and
- `triangulate_polygon_minimum_area` for a source-vertex minimum-area split.

`Mesh.triangulate()` modifies a mesh in place after staging every replacement.
`Mesh.triangulated()` returns an independent triangulated mesh of the same
concrete type, preserving the mesh data model. Numerical consumers extract its
structural buffers explicitly:

```python
triangle_mesh = mesh.triangulated()
vertices, triangles = triangle_mesh.to_vertices_and_faces()
```

`Polygon`, `PolygonalSurface`, and `Polyhedron` instead return an ephemeral
`Tessellation`. `PlanarRegion.triangulated()` also returns a `Tessellation` and
has no algorithm argument because its exterior-and-holes contract determines
the operation.

## Planar Delaunay operations

Planar point and domain functions return structural `(vertices, triangles)`
buffers. They accept Python and NumPy coordinate buffers without requiring a
COMPAS geometry representation.

```python
from compas.geometry import constrained_delaunay_triangulation
from compas.geometry import delaunay_triangulation

points = [[0, 0, 0], [2, 0, 0], [2, 1, 0], [0, 1, 0]]
vertices, triangles = delaunay_triangulation(points)

boundary = [[0, 0, 0], [4, 0, 0], [4, 4, 0], [0, 4, 0]]
vertices, triangles = constrained_delaunay_triangulation(boundary)
```

Inputs lie in world XY unless an explicit frame is supplied. The constrained
and conforming operations require a plugin. Conforming triangulation alone may
insert Steiner vertices and accepts the optional positive finite
`max_edge_length` refinement target.

## BRep tessellation

BReps and trimmed BRep faces expose only precision-controlled tessellation:

```python
tessellation = brep.to_tessellation(
    linear_deflection=0.01,
    angular_deflection=15.0,
)
```

Linear deflection uses model units and angular deflection uses degrees. Omitted
values resolve from `TOL.lineardeflection` and the degree equivalent of
`TOL.angulardeflection` before plugin dispatch. These values are requested
approximation controls, not proof that a backend achieved an error bound.

BReps do not provide `to_polygonal_surface`: their trimmed faces have no single
uniform parameter-grid structure to preserve.
