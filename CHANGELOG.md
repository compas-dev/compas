# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

### Changed

### Removed


## [0.13.1] 2019-12-17

### Added

### Changed

### Removed


## [0.13.0] 2019-12-16

### Added

- Added DOI to bibtex entry.
- Added conversion for old mesh JSON data.

### Changed

- Indirectly changed mesh serialisation to JSON (by changing key conversion and moving conversion into JSON methods).
- Moved conversion of int keys of mesh data to strings for json serialisation to from/to json.
- Moved from/to methods for mesh into mesh definition.
- Subdivision algorithms use fast mesh copy.

### Removed

- Support for non-integer vertex and face identifiers in mesh.

## [0.12.4] 2019-12-11

### Added

### Changed

### Removed

## [0.12.3] 2019-12-11

### Added
- Added `mesh_subdivide_frames` to `compas.datastructures.subdivision`

### Changed

### Removed

## [0.12.2] 2019-12-11

### Added

- Added `intersection_segment_polyline` to `compas.geometry.intersections`
- Added `intersection_segment_polyline_xy` to `compas.geometry.intersections`
- Added `from_sides_and_radius` to `compas.geometry.Polygon`

### Changed

- Reworked docstrings of methods in `compas.geometry.queries`
- Set default `tol` to `1e-6` in `compas.geometry.queries`

### Removed

## [[0.12.1] 2019-12-10] 2019-12-10

### Added

- Added inherited methods to class docs.
- Added data structure mixins to the docs.
- Added `data` and `from_data` to `compas.geometry.Polyhedron`
- Added explicit support for collections to `compas_blender`

### Changed

- Bottom face of cylinder shape should be flipped.
- Face reading mechanism of OFF reader.
- `compas.geometry.Box` is now centred at origin by default.

### Removed

- Removed `compas.remote` because it does not provide an advatage over `compas.rpc`.

## [[0.11.4] 2019-11-26] 2019-11-26

### Added

- Added `compas_rhino.etoforms.ImageForm`.
- Added `doc8` as dev requirement.

### Changed

- Changed `compas_rhino.install_plugin` to use only the plugin name, w/o the GUID.
- Changed `iterable_like` to prevent exhausting generators passed as targets.

### Removed

- Removed `compas_rhino.ui.Controller`.
- Removed `compas_rhino.ui.Button`.

## [[0.11.2] 2019-11-19] 2019-11-19

### Added

- Added factory methods for `compas_rhino.artists._Artist`

### Changed

- Set `compas_rhino.artists.FrameArtist` layer clear to false by default.
- Wrapped internals of RPC dispatch method in try-except to catch any import problems and report back on the client side.
- Stopping of HTTP server (`compas.remote`) is now handled properly through separate thread.
- Fixed mutable init parameters of `RobotModel`
- Fixed bug in `mesh_quads_to_triangles` that caused face data to be deleted even when not necessary.
- Switched to `compas.geometry.KDTree` as fallback for `scipy.spatial.cKDTree` instead of Rhino `RTree` because it currently fails.

### Removed

## [0.11.0] 2019-11-09

### Added

- Added `iterable_like` to `compas.utilities.itertools_`
- Added `compas.geometry.icp_numpy` for pointcloud alignment using ICP.
- Added RPC command-line utility: `$ compas_rpc {start|stop} [port]`
- Added `__version__` to `compas_plotters`.
- Added `compas_plotters` to `.bumpversion.cfg`.
- Added `Colormap` to `compas.utilities`.
- Added `is_line_line_colinear()` to `compas.geometry`
- Added link to Github wiki for devguide.
- Added pointcloud alignment example to docs.
- Show git hash on `compas.__version__` if installed from git.
- Added `autopep8` to dev requirements.
- Added methods `add_joint` and `add_link` to `RobotModel` 
- Added support for geometric primitives to JSON data encoder and decoder.
- Added support for `data` to all geometric primitives.

### Changed

- Docs are only deployed to github pages for tagged commits.
- Fixing printing issue with `compas.geometry.Quarternion` in ironPython.
- Fixed a missing import in `compas.geometry.Polygon`.
- Removed unused imports in `compas.geometry.Polyline`.
- Adjusted `compas.geometry.Quarternion.conjugate()` to in-place change, added `compas.geometry.Quarternion.conjugated()` instead which returns a new quarternion object.
- Fixed `rotation` property of `Transformation`.
- Simplified plugin installation (use plugin name only, without GUID).
- Bind RPC server to `0.0.0.0` instead of `localhost`.
- Fixed different argument naming between Rhino5 and Rhino6 of `rs.LayerVisible()` in `compas_rhino.utilities.objects`.

### Removed

## [0.10.0] 2019-10-28

### Added

- Added method for computing the determinant of the matrix of a transformation `compas.geometry.Transformation.determinant`.
- Added method for transposing (the matrix of) a transformation in-place `compas.geometry.Transformation.transpose`.
- Added method creating a transposed copy of a transformation `compas.geometry.Transformation.transposed`.
- Added method for invertig (the matrix of) a transformation in-place `compas.geometry.Transformation.invert`.
- Added `compas.geometry.Transformation.inverted` as an alias for `compas.geometry.Transformation.inverse`.
- Added method creating a copy of a transformation instance with a given transformation concatenated `compas.geometry.Transformation.concatenated`.
- Added method `to_vertices_and_faces` to all the classes inheriting from `compas.geometry.Shape` to create a `Mesh` representation of them.

### Changed

- Changed `compas.geometry.Transformation.inverse` to return an inverted copy of the transformation.
- Changed `compas.geometry.Transformation.decompose` to `compas.geometry.Transformation.decomposed`.
- Changed `compas.geometry.Transformation.concatenate` to add another transformation to the transformation instance.

### Removed

## [0.9.1] 2019-10-28

### Added

- Added `compas.geometry.Point.transform_collection` and `compas.geometry.Point.transformed_collection`.
- Added `compas.geometry.Vector.transform_collection` and `compas.geometry.Vector.transformed_collection`.
- Added `compas.geometry.Line.transform_collection` and `compas.geometry.Line.transformed_collection`.
- Added support for new Python plugin location for Rhino 6.0 on Mac.
- Added `compas.geometry.bestfit_frame_numpy`

### Changed

- Fixed transformation of start and end point of `compas.geometry.Line` to update the point objects in place.
- Fixed return value of `compas.numerical.pca_numpy` to return mean not as nested list.

### Removed


## [0.9.0] 2019-10-21

### Added

- Added `matrix_change_basis`, `Transformation.change_basis`
- Added `matrix_from_frame_to_frame`
- Added non-numpy versions of `global_coords`, `local_coords`
- Added static method `Frame.local_to_local_coords`
- Added `__getitem__`, `__setitem__` and `__eq__` to `Quaternion`
- Added `Vector.scaled` and `Vector.unitized`
- Added `transform_frames` and respective helper functions `dehomogenize_and_unflatten_frames`, `homogenize_and_flatten_frames`
- Added `transform_frames_numpy` and respective helper functions `dehomogenize_and_unflatten_frames_numpy`, `homogenize_and_flatten_frames_numpy`

### Changed

- Renamed `global_coords_numpy` and `local_coords_numpy` to `local_to_world_coords_numpy` and `world_to_local_coords_numpy`.
- Changed parameters `origin` `uvw` of `local_to_world_coords_numpy` and `world_to_local_coords_numpy` to `frame`.
- Fixed some returns of `Frame` and `Rotation` to use `Vector` or `Quaternion`
- Renamed methods `Frame.represent_point/vector/frame_in_global_coordinates` and `Frame.represent_point/vector/frame_in_local_coordinates` to `Frame.to_local_coords` and `Frame.to_world_coords`.

### Removed

## [0.8.1] 2019-10-01

### Added

### Changed

- Fixed unguarded import of `numpy` based transformations in mesh package.

### Removed

## [0.8.0] 2019-10-01

### Added

- Added test section for `compas.geometry.transformations`
- Added `tol` parameter to `queries.is_colinear`
- Added compas rhino installer for Rhino Mac 6.0 `compas_rhino.__init__`.
- Added oriented bounding box for meshes `compas.datastructures.mesh_oriented_bounding_box_numpy`.
- Added full testing functions for `compas.datastructures.mesh`
- Added `draw_mesh` to `compas_ghpython.artists.MeshArtist`

### Changed

- Generate sphinx documentation from markdown files in repo root for top level sections.
- Merged `compas.geometry.xforms` into `compas.geometry.transformations`
- Fixed `AttributeError: 'Mesh' object has no attribute 'neighbors'`
- Fixed Key error with `Mesh.boundary()`
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
- Examples in docs/rhino updated to work with current codebase
- Callbacks tutorial updated to work with current codebase
- Base geometric primitives on `compas.geometry.Primitive` and `compas.geometry.Shape`
- Separated `numpy` based tranformations into separate module.

### Removed

- Removed `compas_viewers` to separate repo.
- Removed `compas_hpc` to separate repo.

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
