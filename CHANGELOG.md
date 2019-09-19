# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- Added `tol` parameter to `queries.is_colinear`
- Added compas rhino installer for Rhino Mac 6.0 `compas_rhino.__init__`.
- Added oriented bounding box for meshes `compas.datastructures.mesh_oriented_bounding_box_numpy`.
- Added full testing functions for `compas.datastructures.mesh`
- Added `draw_mesh` to `compas_ghpython.artists.MeshArtist`

### Changed

- Extended `offset_polygon` and `offset_polyline` to handle colinear segments
- Fixed unsorted mesh vertex coordinates `xyz` in `compas_viewers.viewer.MeshView`
- Changed stderr parameter from STDOUT to PIPE in `compas.rpc.Proxy` for Rhino Mac 6.0.
- Fixed import of `delaunay_from_points` in `Mesh.from_points`.
- More control over drawing of text labels in Rhino.
- Extension of `face_vertex_descendant` and `face_vertex_ancestor` in `Mesh`.
- Changed the name and meaning of the parameter `oriented` in the function `Mesh.edges_on_boundary`.
- Add `axis` and `origin` defaults to `compas.robots.Joint`
- Unified vertices and face import order for .obj files with python2 and 3
- Changed python interpreter selection (e.g. RPC calls) to fallback to `python` if `pythonw` is not present on the system
- Fixed `compas_ghpython.artists.MeshArtist` to support ngons.
- Deprecate the method `draw` of `compas_ghpython.artists.MeshArtist` in favor of `draw_mesh`.
- Fix icosahedron generation

### Removed


## [0.7.2] 2019-08-09

### Added

- Added `compas_rhino.geometry.RhinoGeometry` to the docs.
- Added `compas.remote.services`.
- Added `compas.remote.services.network.py` service for handling requests for a browser-based network viewer.
- Possibility to call forward_kinematics on `compas.robots.RobotModel`
- Added `compas.set_precision` function for the setting the global precision used by COMPAS as a floating point number.

### Changed

- Fix mesh genus in `compas.datastructures`.
- Fixed missing import in `compas_rhino.geometry`.
- Removed circular imports from `compas_rhino.geometry`.
- Fix duplicate hfkeys in `compas.datastructures.volmesh.halffaces_on_boundary`.
- Moved `compas.remote.service.py` to `compas.remote.services.default.py`.
- Removed processing of face keys from data getter and setter in `compas.datastructures.Network`.
- Using `SimpleHTTPRequestHandler` instead of `BaseHTTPRequestHandler` to provide basic support for serving files via `GET`.
- Mesh mapping on surface without creating new mesh to keep attributes in `compas_rhino.geometry.surface.py`.
- Moving functionality from `compas_fab.artists.BaseRobotArtist` to `compas.robots.RobotModel`
- Fix exception of null-area polygon of centroid polygon in `compas.geometry.average.py`.
- Fix loss of precision during mesh welding in `compas.datastructures.mesh_weld`.

### Removed


## [0.7.1] 2019-06-29

### Added

### Changed

- Include `compas_plotters` and `compas_viewers` in the build instructions.
- Moved import of `subprocess` to Windows-specific situations.
- Fixed document functions failing when document name is `None`.
- Downgraded `numpy` requirements.
- Loosened `scipy` requirements.
- Default Python to `pythonw`.

### Removed


## [0.7.0] 2019-06-27

### Added

- Added filter shorthand for selecting OBJ, JSON files in Rhino.
- Added `compas_plotters`
- Added `compas_viewers`
- Added `compas_rhino.draw_circles` and the equivalent Artist method
- Add class functions to `compas.datastructures.VolMesh`.
- Added `face_neighborhood` class function to `compas.datastructures.Mesh`.
- Added `get_face_attributes_all` to `compas.datastructures._mixins.attributes`.
- Added `get_faces_attributes_all` to `compas.datastructures._mixins.attributes`.
- Added `compas.remote` package for making HTTP based Remote Procedure Calls.

### Changed

- Restructure halffaces as lists in `compas.datastructures.VolMesh`.
- Correctly handle `python-net` module presence during IronPython imports.
- Switched to `compas.IPY` check instead of `try-except` for preventing non IronPython friendly imports.
- Changed installation of compas packages to Rhino to support non-admin user accounts on Windows.
- Copy facedata in `mesh_quads_to_triangles`
- Added non-imported service for `compas.remote` for starting the subprocess that runs the server.

### Removed

- Removed `compas.plotters`
- Removed `compas.viewers`

## [0.6.2] 2019-04-30

### Added

### Changed

- Based mesh drawing for Rhino on RhinoCommon rather than Rhinoscriptsyntax.
- Fixed mesh drawing for Rhino 6

### Removed


## [0.6.1] 2019-04-29

### Added

### Changed

- Fixed bug in RPC. The services cannot have a `pass` statement as class body.

### Removed


## [0.6.0] 2019-04-29

### Added

- Added `center` property getter to `compas.geometry.Cirle` primitive
- Add `astar_shortest_path` to `compas.topology.traversal`.

### Changed

- Updated configuration instructions for Blender.
- Changed naming convention for drawing functions from `xdraw_` to `draw_`.
- Changed mesh drawing in Rhino to use separate mesh vertices per face. This makes the mesh look more "as expected" in *Shaded* view.

### Removed

- Removed support for Python 3.5.x by setting the minimum requirements for Numpy and Scipy to `1.16` and `1.2`, respectively.

## [0.5.2] 2019-04-12

### Added

- Added `draw_polylines` to `compas_rhino.artists.Artist`.
- Added `color` argument to `compas_rhino.artists.MeshArtist.draw_mesh`.
- Added named colors to `compas.utilities.colors.py`.

### Changed

- Fix `mesh_uv_to_xyz` in `RhinoSurface`.
- Fix 'mesh_weld' and 'meshes_join_and_weld' against consecutive duplicates in face vertices.
- Fix setting of environment variables in `System.Diagnostics.Process`-based subprocess for `XFunc` and `RPC`.
- Fix `XFunc` on RhinoMac.
- Fix `trimesh_subdivide_loop` from `compas.datastructures`.
- Changed Numpy and Scipy version requirements to allow for Python 3.5.x.

### Removed

- Removed `mixing.py` from `compas.utilities`.
- Removed `singleton.py` from `compas.utilities`.
- Removed `xscript.py` from `compas.utilities`.
- Removed `sorting.py` from `compas.utilities`.
- Removed `names.py` from `compas.utilities`.
- Removed `xfunc.py` from `compas_rhino.utilities`, use `compas.utilities.XFunc` instead.

## [0.5.1] 2019-03-25

### Added

### Changed

- Fix `XFunc` and `RPC` environment activation.
- Fix exception on Rhino Mac.
- Fix missing import on `compas_rhino.geometry`.
- Fix `compas.geometry.offset_polygon`.
- Fix installation for Rhino, related to implicit import of `matplotlib`.

### Removed

## [0.5.0] 2019-03-15

### Added

- Add `Circle` and `Sphere` primitives to `compas.geometry`.
- Add functions to `Plane` and `Box` primitives.
- Add functions to `compas_rhino` curve: `length` and `is_closed`.
- Add functions to `compas_rhino` surface: `kinks`, `closest_point`, `closest_point_on_boundaries`, and functions for mapping/remapping between XYZ and UV(0) spaces based on surface's parametrization (`point_xyz_to_uv`, `point_uv_to_xyz`, `line_uv_to_xyz`, `polyline_uv_to_xyz`, `mesh_uv_to_xyz`)
- Add `is_scalable` to `compas.robots.Joint`.

### Changed

- Fix exception in `Plane.transform`.
- Fix installer to remove old symlinks.
- Fix RPC proxy server.

## [0.4.22] 2019-03-05

### Added

- Add pretty print option to JSON formatter.
- Add remeshing based on `triangle`.
- Add compatibility with ETO forms to `compas_rhino` edge modifiers.

## [0.4.21] 2019-03-04

### Changed

- Fix import in `compas_rhino` vertex modifiers.

## [0.4.20] 2019-03-04

### Removed

- Remove `download_image_from_remote` utility function.

## [0.4.12] 2019-03-04

### Changed

- Small fixes on Rhino forms support.

## [0.4.11] 2019-03-03

### Added

- New function to join network edges into polylines: `network_polylines`.
- New mesh functions: `mesh_offset`, `mesh_thicken`, `mesh_weld` and `meshes_join_and_weld`.
- New mesh functions: `face_skewness`, `face_aspect_ratio`, `face_curvature` and `vertex_curvature`.
- New functions to get disconnected elements of  `Mesh`: `mesh_disconnected_vertices`, `mesh_disconnected_faces`, `mesh_explode`.
- New functions to get disconnected elements of  `Network`: `network_disconnected_vertices`, `network_disconnected_edges`, `network_explode`.
- Add statistics utility functions: `average`, `variance`, `standard_deviation`.
- Add `binomial_coefficient` function.
- Add option to create `Network` and `Mesh` from dictionaries of vertices and faces.
- Add `face_adjacency_vertices` to `Mesh`
- Add optional prefix to the rhino name attribute processor
- Add `mesh_move_vertices` to `compas_rhino`.
- Add support for relative mesh references in URDF.

### Changed

- Fix mesh centroid and mesh normal calculation.
- Refactor of drawing functions in `compas_blender`.
- Fix material creation in `compas_blender`.
- New default for subdivision: `catmullclark`.

## [0.4.9] 2019-02-10

### Added

- New class methods for `Polyhedron`: `from_platonicsolid` and `from_vertices_and_faces`.
- Constrained and conforming Delaunay triangulations based on Triangle.
- Predicate-based filtering of vertices and edges.
- `mesh.geometry`for geometry-specific functions.
- `trimesh_face_circle` in `mesh.geometry`.

### Changed

- Fix exception in `angle_vectors_signed` if vectors aligned
- Fix exception in `Polyline.point`
- Update Rhino installation merging Win32 and Mac implementations and defaulting the bootstrapper to the active python even if no CONDA environment is active during install.

### Removed

- Bound mesh operations.

## [0.4.8] 2019-01-28

### Added

- Curve tangent at parameter.
- Box shape.
- Numpy-based mesh transformations.
- Option to share axes among plotters.
