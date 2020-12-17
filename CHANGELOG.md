# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.19.2] 2020-12-17

### Added

### Changed

* Changed `compas._os.prepare_environment` to prepend environment paths (fixes problem with RPC on windows).

### Removed


## [0.19.1] 2020-12-10

### Added

### Changed

* Fix bug in `compas.datastructures.AttributesView`.

### Removed


## [0.19.0] 2020-12-09

### Added

* Added `is_osx`.

### Changed

* Fix default namespace handling in URDF documents.
* Allow custom/unknown attributes in URDF `Dynamics` element.
* Moved os functions from `compas` to `compas._os`.
* Fixed bug in `is_linux`.
* Changed `is_windows` to work for CPython and IronPython.
* Changed `compas._os` functions to use `is_windows`, `is_mono`, `is_osx`.
* Changed IronPython checks to `compas.IPY` instead of `compas.is_ironpython`.
* Fixed data serialisation in `compas.datastructures.HalfFace`.

### Removed

* Removed all implementations of `draw_collection`.


## [0.18.1] 2020-12-01

### Added

* Added URDF and XML writers.
* Added `compas.robots.RobotModel.to_urdf_file`.
* Added `compas.files.URDF.from_robot`.

### Changed

* Changed implementation of `Mesh.vertices_on_boundaries` to account for special cases.
* Changed `Mesh.edges_on_boundaries` corresponding to `Mesh.vertices_on_boundaries`.
* Changed `Mesh.faces_on_boundaries` corresponding to `Mesh.vertices_on_boundaries`.
* Changed `Mesh.vertices_on_boundary` to return vertices of longest boundary.
* Changed `Mesh.edges_on_boundary` to return edges of longest boundary.
* Changed `Mesh.faces_on_boundary` to return faces of longest boundary.
* Fixed default value for `compas.robots.Axis`.
* Changed surface to mesh conversion to include cleanup and filter functions, and use the outer loop of all brep faces.

### Removed


## [0.18.0] 2020-11-24

### Added

* Added `remap_values` to `compas_utilities`.
* Added `compas.datastructures.mesh_slice_plane`.
* Added `compas.json_dump`, `compas.json_dumps`, `compas.json_load`, `compas.json_loads`.

### Changed

* Fixed bug in `compas.datastructures.Network.delete_node`.
* Fixed bug in `compas.datastructures.Network.delete_edge`.
* Fixed bug in select functions for individual objects in `compas_rhino.utilities`.
* Fixed bug in `compas.datastructures.mesh_merge_faces`.
* changed base of `compas.geometry.Transformation` to `compas.base.Base`.

### Removed

* Removed `compas.datastructures.mesh_cut_by_plane`.

## [0.17.3] 2020-11-20

### Added

### Changed

* Fixed bug in `compas.geometry.is_coplanar`.
* Fixed bug in `compas.datastructures.mesh_merg_faces`.
* Fixed bug in `compas.robots.RobotModel.add_link`.
* Fixed bug in `compas.datastructures.Volmesh.cell_to_mesh`.

### Removed


## [0.17.2] 2020-11-04

### Added

### Changed

* Fixed bug in `__getstate__`, `__setstate__` of `compas.base.Base`.
* Fixed bug in `compas_rhino.artists.MeshArtist` and `compas_rhino.artists.NetworkArtist`.
* Changed length and force constraints of DR to optional parameters.
* Removed `ABCMeta` from the list of base classes of several objects in compas.

### Removed


## [0.17.1] 2020-10-28

### Added

* Added `compas_rhino.artists.BoxArtist.draw_collection`.
* Added option to show/hide vertices, edges, and faces in `compas_rhino.artists.CapsuleArtist.draw`.
* Added option to show/hide vertices, edges, and faces in `compas_rhino.artists.ConeArtist.draw`.
* Added option to show/hide vertices, edges, and faces in `compas_rhino.artists.CylinderArtist.draw`.
* Added option to show/hide vertices, edges, and faces in `compas_rhino.artists.PolyhedronArtist.draw`.
* Added option to show/hide vertices, edges, and faces in `compas_rhino.artists.SphereArtist.draw`.
* Added option to show/hide vertices, edges, and faces in `compas_rhino.artists.TorusArtist.draw`.
* Added option to show/hide vertices, edges, and faces in `compas_rhino.artists.PolygonArtist.draw`.
* Added option to show/hide vertices, edges, and faces in `compas_rhino.artists.PolylineArtist.draw`.
* Added option to show/hide vertices, edges, and faces in `compas_rhino.artists.VectorArtist.draw`.

### Changed

* Changed implementation of `compas_rhino.artists.BoxArtist.draw`.
* Fixed bug in `compas.geometry.Capsule`.
* Fixed bug in `compas.geometry.Cone`.
* Changed `compas_rhino.draw_mesh` to support Ngons if available.
* Fixed bug in polyhedron data.

### Removed

* Removed `compas_rhino.artists.PointArtist.draw_collection`.
* Removed `compas_rhino.artists.CircleArtist.draw_collection`.
* Removed `compas_rhino.artists.LineArtist.draw_collection`.

## [0.16.9] 2020-10-21

### Added

* Added binary STL writer.
* Added constructor `from_euler_angles` to `compas.geometry.Transformation`.
* Added method for adding objects from a list to `compas_plotters.GeometryPlotter`.
* Added `compas_rhino.artists.BoxArtist`.
* Added `compas_rhino.artists.CapsuleArtist`.
* Added `compas.geometry.Polyhedron.from_halfspaces` and `compas.geometry.Polyhedron.from_planes`.
* Added `compas.geometry.is_point_behind_plane` and `compas.geometry.is_point_in_polyhedron`.
* Added `centroid` and `bounding_box` properties to `compas.geometry.Pointcloud`.
* Added `edges` property to `compas.geometry.Box`.
* Added `edges` property to `compas.geometry.Polyhedron`.
* Added `compas.datastructures.network_smooth_centroid`.

### Changed

* Fixed bug in handling of keys in edge attribute functions of `compas.datastructures.Halfedge`.
* Fixed bug in `compas.geometry.Polygon.lines`.
* Fixed bug in `compas.geometry.Polyline.lines`.
* Changed `compas.geometry.Shape.to_vertices_and_faces` to `abstractmethod`.
* Fixed bug in magic methods of `compas.geometry.Box`.
* Fixed bug in `compas.geometry.Box.contains`.
* Fixed bug in `delete_vertex` and `delete_face` in `compas.datastructures.Halfedge`.
* Fixed bug in `delete_node` of `compas.datastructures.Graph`.
* Fixed bug in `summary` method of `compas.datastructures.Graph` and `compas.datastructures.Halfedge`.

### Removed


## [0.16.8] 2020-10-14

### Added

* Added `RobotModelArtist` to `compas_rhino`, `compas_ghpython` and `compas_blender`.
* Added `ToolModel`.
* Added `compas.geometry.Pointcloud`.
* Added `compas.utilities.grouper`.
* Added `PolygonArtist`, `PolylineArtist` to `GeometryPlotter`.

### Changed

* `Mesh` takes name of `Shape` in `Mesh.from_shape`.
* Fixed `zoom_extents` of `GeometryPlotter`.

### Removed

* Removed `SegmentArtist` from `compas_plotters`.

## [0.16.7] 2020-10-06

### Added

* Added functionality to the RPC service to automatically reload modules if a change is detected.

### Changed

### Removed


## [0.16.6] 2020-09-30

### Added

* Added `compas_plotters.geometryplotter.GeometryPlotter` for COMPAS geometry objects.

### Changed

* Changed `compas.base.Base.dtype` to property.
* Changed JSON schema to draft 7.
* Changed version processing to `distutils.version.LooseVersion`.

### Removed


## [0.16.5] 2020-09-26

### Added

* Added tests for halfedge data schemas.

### Changed

* Fixed RGB color processing in `compas.utilities.color_to_colordict`.
* Fixed Blender object and dat amanagement to avoid `malloc` problems.
* Updated Blender data structure artists.
* Changed Blender unused data clearing to also clear collections.
* Fixed JSON data validation of base COMPAS object.

### Removed


## [0.16.4] 2020-09-24

### Added

### Changed

* Fixed bug in `compas.geometry.Box.vertices`.

### Removed


## [0.16.3] 2020-09-23

### Added

* Added abstract `DATASCHEMA` to `compas.base.Base`.
* Added abstract `JSONSCHEMA` to `compas.base.Base`.
* Added `validate_data` to `compas.base.Base`.
* Added `validate_json` to `compas.base.Base`.
* Added implementation of `DATASCHEMA` to `compas.datastructures.Halfedge`.
* Added implementation of `JSONSCHEMA` to `compas.datastructures.Halfedge`.
* Added `NodeAttributeView`.
* Added implementation of `DATASCHEMA` to `compas.datastructures.Graph`.
* Added implementation of `JSONSCHEMA` to `compas.datastructures.Graph`.
* Added `compas.rpc.Proxy.restart_server`.
* Added `compas_rhino.objects.NetworkObject`.
* Added constructors `from_matrix` and `from_rotation` to `compas.geometry.Quaternion`.
* Added `draw_collection` methods to Grasshopper artists.

### Changed

* Updated naming conventions in `compas.datastructures.HalfFace` and `compas.datastructures.VolMesh`
* Moved `compas.datastructures.Datastructure` to `compas.datastructures.datastructure`.
* Changed base class of `compas.datastructures.Datastructure` to `compas.base.Base`.
* Changed `from_json` to `to_json` of meshes to use encoders and decoders.
* Moved `MutableMapping` to `compas.datastructures._mutablemapping`.
* Moved attribute views to `compas.datastructure.attributes`.

### Removed

* Removed `from_json`, `to_json`, `to_data`, `copy`, `transformed` from primitives, defaulting to the base implementation in `compas.geometry.Primitive`.
* Removed `from_json`, `to_json`, `to_data`, `copy`, `__str__`, from datastructures, defaulting to the base implementation in `compas.datastructure.Datastructure`.

## [0.16.2] 2020-08-06

### Added

* Added plugin system based on decorators: `compas.plugins.pluggable` & `compas.plugins.plugin`.
* Added `compas_rhino` implementation of the boolean operation pluggable interfaces (union/difference/intersection).
* Added `compas.datastructures.Mesh.transform_numpy`.
* Added `PluginNotInstalledError`.
* Added `compas.geometry.booleans`.
* Added tolerance parameter to angle functions.
* Added support for Rhino 7 in install/uninstall routines.
* Added install/uninstall for Rhino plugins (with support for Rhino 7).
* Added base class for all COMPAS objects `compas.base.Base`.
* Added base class for all Rhino objects representing COMPAS objects `compas_rhino.objects.Object`.
* Added mesh object representing COMPAS meshes in Rhino `compas_rhino.objects.MeshObject`.
* Added the methods `to_data` and `from_data` to `compas.robots.RobotModel`.

### Changed

* Restructure and reorganize volmesh datastructure
* Fixed scaling bug in `compas.geometry.Sphere`
* Fixed bug in `compas.datastructures.Mesh.add_vertex`.
* Fixed performance issue affecting IronPython when iterating over vertices and their attributes.
* Changed return value of drawing functions of `compas_rhino.artists.MeshArtist` to list of GUID.
* Changed return value of drawing functions of `compas_rhino.artists.NetworkArtist` to list of GUID.
* Moved "inspectors" to `compas_rhino.objects`.
* Moved "modifiers" to `compas_rhino.objects`.
* Connection attempts can now be set for `compas.Proxy.start_server` using the
  attribute `Proxy.max_conn_attempts`.
* `Scale.from_factors` can now be created from anchor frame.
* Changed vertex reading of PLY files to include all property information.

### Removed

* Removed CGAL based boolean implementations.
* Removed artist mixins from `compas_rhino`.
* Removed `clear_` functions from `compas_rhino.artists.MeshArtist`.
* Removed `clear_` functions from `compas_rhino.artists.NetworkArtist`.
* Removed `to_data`, `from_data` from `compas_rhino.artists`.
* Removed `compas_rhino.artists.BoxArtist` stub.
* Removed references to "edge" dict from `compas.datastructures.VolMesh`.

## [0.16.1] 2020-06-08

### Added

### Changed

* Fixed scaling bug in `compas.geometry.Sphere`

### Removed

## [0.16.0] 2020-06-05

### Added

* Added `compas_rhino.geometry.RhinoVector`.
* Added basic mesh cutting (`compas.datastructures.Mesh.cut()`).
* Added `compas.datastructures.Mesh.join(other)`.
* Added `compas.geometry.argmin` and `compas.geometry.argmax`.
* Added STL witer.
* Added `compas.datastructures.Mesh.to_stl`.
* Added `unweld` option to obj writing.

### Changed

* Fixed bug in `FaceAttributeView.__get_item__`: access to default was tried before attrs.
* Fixed bug in `EdgeAttributeView.__get_item__`: access to default was tried before attrs.
* Changed `VertexAttributeView.__get_item__` to follow access logic of `FaceAttributeView`.
* Fixed bug in `draw_edges` in `compas_rhino`'s `EdgeArtist`.
* Fixed bug in `draw_edges` in `compas_ghpython`'s `EdgeArtist`.
* Fixed bug in ``compas_rhino.geometry.RhinoSurface.brep_to_compas``.
* Fixed bug in ``compas.geometry.Box.from_bounding_box``
* Fixed bug in ``compas.geometry.Box.from_width_height_depth``
* Fixed inconsistencies in ``compas.geometry._transformations``.
* Renamed ``compas.geometry.Frame.to_local_coords`` to ``compas.geometry.Frame.to_local_coordinates``
* Renamed ``compas.geometry.Frame.to_world_coords`` to ``compas.geometry.Frame.to_world_coordinates``
* Renamed ``compas.geometry.Transformation.change_basis`` to ``compas.geometry.Transformation.from_change_of_basis``
* Renamed ``compas.geometry.matrix_change_basis`` to ``compas.geometry.matrix_from_change_of_basis``
* Renamed ``compas.geometry.Projection.orthogonal`` to ``compas.geometry.Projection.from_plane`` and changed input params
* Renamed ``compas.geometry.Projection.parallel`` to ``compas.geometry.Projection.from_plane_and_direction`` and changed input params
* Renamed ``compas.geometry.Projection.perspective`` to ``compas.geometry.Projection.from_plane_and_point`` and changed input params
* Changed constructor of all ``compas.geometry.Transformation`` and derivatives. Preferred way of creating any ``compas.geometry.Transformation`` is with the classmethods ``from_*``
* Changed params (point, normal) into plane for ``compas.geometry.matrix_from_parallel_projection``, ``compas.geometry.matrix_from_orthogonal_projection`` and ``compas.geometry.matrix_from_perspective_projection``

### Removed

## [0.15.6] 2020-04-27

### Added

* Extended glTF support.
* Added classmethod `from_geometry` to `RhinoMesh`
* Added `intersection_sphere_line`
* Added `intersection_plane_circle`
* Added `tangent_points_to_circle_xy`
* Added basic OBJ file writing.
* Added `Mesh.to_obj`.

### Changed

* Fixed bug in `Box.from_bounding_box`.
* Updated Blender installation docs for latest release.
* Fixed `robot.forward_kinematics()` when requested for base link.
* Fixed bug in `to_compas` conversion of Rhino meshes.
* Fixed bug where `compas.geometry.Primitive` derived classes cannot be serialized by jsonpickle.

### Removed

## [0.15.5] 2020-03-29

### Added

* Added classmethod `from_geometry` to `RhinoMesh`.
* Added conversion to polygons to `BaseMesh`.
* Re-added length, divide, space methods of `RhinoCurve`.
* Added basic OFF file writing.
* Added basic PLY file writing.
* Added `Mesh.to_ply`.
* Added `Mesh.to_off`.

### Changed

* Fixed object naming in artists of `compas_ghpython`.
* Resizing of Rhino property form.
* Fixed orientation of `RhinoSurface` discretisation.
* Check for existence of object in Rhino purge functions.
* Fixed bug in mesh boundary functions.

### Removed


## [0.15.4] 2020-03-05

### Added

* Added algorithm for pulling points onto mesh.
* Added base ellipse class to geometry primitives.
* Added circle artist to plotters.
* Added mesh artist to plotters.
* Added ellipse artist to plotters.
* Added support for robot mimicking joints.

### Changed

* Fixed bugs in `compas_rhino.artists.NetworkArtist`.
* Add conda executable path to `compas_bootstrapper.py`.

### Removed


## [0.15.3] 2020-02-26

### Added

* Added optional class parameter to `RhinoMesh.to_compas`.
* Added max int key to serialisation of graph.

### Changed

* Changed name of base mesh implementation to `BaseMesh`.
* Changed name of base network implementation to `BaseNetwork`.
* Fixed bug in face finding function.

### Removed

* Removed optional requirements from setup file.
* Removed parameters from default polyhedron constructor.

## [0.15.2] 2020-02-20

### Added

### Changed

### Removed

## [0.15.1] 2020-02-16

### Added

* Added glTF support.
* Added graph and halfedge data structures.
* Added Rhino line geometry.
* Added Rhino plane geometry.

### Changed

* Fixed `compas_hpc` import problem.
* Split up topology part from geometry part for network and mesh.
* Split up network and mesh naming conventions.
* Reworked network face cycle finding.
* Updated mesh from lines.
* Updated network plotter in correspondance with network.
* Integrated mixin functionality and removed mixins.

### Removed

* Removed parallelisation from network algorithms.
* Removed numba based dr implementations.

## [0.15.0] 2020-01-24

### Added

* Added `to_compas` to `compas_rhino.geometry.RhinoPoint`.
* Added `to_compas` to `compas_rhino.geometry.RhinoLine`.
* Added `to_compas` to `compas_rhino.geometry.RhinoCurve`.
* Added `to_compas` to `compas_rhino.geometry.RhinoMesh`.
* Added `brep_to_compas` to `compas_rhino.geometry.RhinoSurface`.
* Added `uv_to_compas` to `compas_rhino.geometry.RhinoSurface`.
* Added `heightfield_to_compas` to `compas_rhino.geometry.RhinoSurface`.
* Added `compas.datastructures.mesh_pull_points_numpy`.

### Changed

* Moved `compas_rhino.conduits` into `compas_rhino.artists`.
* Fixed bug in `compas.datastructures.Mesh.edges_where`.
* Fixed bug in `compas.datastructures.Mesh.faces_where`.
* Fixed bug in `compas.datastructures.Mesh.edge_attributes`.
* Fixed bug in `compas.datastructures.Mesh.face_attributes`.
* Fixed bug in `compas.datastructures.Mesh.edges`.
* Fixed bug in `compas.datastructures.Mesh.faces`.
* Fixed bug in `compas.datastructures.Mesh.offset`.

### Removed

* Removed deprecated `compas.geometry.xforms`.
* Removed deprecated `compas_rhino.helpers`.
* Removed `compas_rhino.constructors`.

## [0.14.0] 2020-01-21

### Added

* Added `compas.datastructures.mesh.Mesh.any_vertex`.
* Added `compas.datastructures.mesh.Mesh.any_face`.
* Added `compas.datastructures.mesh.Mesh.any_edge`.
* Added `compas.datastructures.mesh.Mesh.vertex_attribute`.
* Added `compas.datastructures.mesh.Mesh.vertex_attributes`.
* Added `compas.datastructures.mesh.Mesh.vertices_attribute`.
* Added `compas.datastructures.mesh.Mesh.vertices_attributes`.
* Added `compas.datastructures.mesh.Mesh.edge_attribute`.
* Added `compas.datastructures.mesh.Mesh.edge_attributes`.
* Added `compas.datastructures.mesh.Mesh.edges_attribute`.
* Added `compas.datastructures.mesh.Mesh.edges_attributes`.
* Added `compas.datastructures.mesh.Mesh.face_attribute`.
* Added `compas.datastructures.mesh.Mesh.face_attributes`.
* Added `compas.datastructures.mesh.Mesh.faces_attribute`.
* Added `compas.datastructures.mesh.Mesh.faces_attributes`.
* Added mutable attribute view for mesh vertex/face/edge attributes.

### Changed

* Default Mesh vertex, face, edge attributes are no longer copied and stored explicitly per vertex, face, edge, repesctively.
* Updating default attributes now only changes the corresponding default attribute dict.
* Updated `mesh_quads_to_triangles` to copy only customised face attributes onto newly created faces.
* Fixed bug in `compas.geometry.is_point_in_circle`.
* Fixed bug in `compas.geometry.is_polygon_convex`.
* Fixed bug in `compas.geometry.Polygon.is_convex`.
* Renamed `compas.datastructures.Mesh.has_vertex` to `compas.datastructures.Mesh.is_vertex`.
* Renamed `compas.datastructures.Mesh.has_face` to `compas.datastructures.Mesh.is_face`.
* Split `compas.datastructures.Mesh.has_edge` into `compas.datastructures.Mesh.is_edge` and `compas.datastructures.Mesh.is_halfedge`.

### Removed

* Removed `compas.datastructures.mesh.Mesh.get_any_vertex`.
* Removed `compas.datastructures.mesh.Mesh.get_any_face`.
* Removed `compas.datastructures.mesh.Mesh.get_any_edge`.
* Removed `compas.datastructures.mesh.Mesh.get_vertex_attribute`.
* Removed `compas.datastructures.mesh.Mesh.get_vertex_attributes`.
* Removed `compas.datastructures.mesh.Mesh.get_vertices_attribute`.
* Removed `compas.datastructures.mesh.Mesh.get_vertices_attributes`.
* Removed `compas.datastructures.mesh.Mesh.get_edge_attribute`.
* Removed `compas.datastructures.mesh.Mesh.get_edge_attributes`.
* Removed `compas.datastructures.mesh.Mesh.get_edges_attribute`.
* Removed `compas.datastructures.mesh.Mesh.get_edges_attributes`.
* Removed `compas.datastructures.mesh.Mesh.get_face_attribute`.
* Removed `compas.datastructures.mesh.Mesh.get_face_attributes`.
* Removed `compas.datastructures.mesh.Mesh.get_faces_attribute`.
* Removed `compas.datastructures.mesh.Mesh.get_faces_attributes`.
* Removed `compas.datastructures.mesh.Mesh.set_vertex_attribute`.
* Removed `compas.datastructures.mesh.Mesh.set_vertex_attributes`.
* Removed `compas.datastructures.mesh.Mesh.set_vertices_attribute`.
* Removed `compas.datastructures.mesh.Mesh.set_vertices_attributes`.
* Removed `compas.datastructures.mesh.Mesh.set_edge_attribute`.
* Removed `compas.datastructures.mesh.Mesh.set_edge_attributes`.
* Removed `compas.datastructures.mesh.Mesh.set_edges_attribute`.
* Removed `compas.datastructures.mesh.Mesh.set_edges_attributes`.
* Removed `compas.datastructures.mesh.Mesh.set_face_attribute`.
* Removed `compas.datastructures.mesh.Mesh.set_face_attributes`.
* Removed `compas.datastructures.mesh.Mesh.set_faces_attribute`.
* Removed `compas.datastructures.mesh.Mesh.set_faces_attributes`.
* Removed `print` statement from curvature module.

## [0.13.3] 2020-01-10

### Added

* `compas_rhino.artists.ShapeArtist` as base artist for all shape artists.
* Added `layer`, `name`, `color` attributes to `compas_rhino.artists.PrimitiveArtist`.
* Added `layer`, `name` attributes to `compas_rhino.artists.ShapeArtist`.
* Added `layer`, `name` attributes to `compas_rhino.artists.MeshArtist`.
* Added `clear_layer` method to `compas_rhino.artists.PrimitiveArtist`.
* Added `clear_layer` method to `compas_rhino.artists.ShapeArtist`.
* Added `clear_layer` method to `compas_rhino.artists.MeshArtist`.

### Changed

* Renamed `compas.utilities.maps.geometric_key2` to `geometric_key_xy`.
* Fixed bug in mirror functions.
* Fixed mirroring tests.
* Moved `BaseMesh`, `matrices`, `operations` to `compas.datastructures.mesh.core`.
* Added `transform` and `transformed` (and others) to `Mesh`.

### Removed

* `compas_rhino.artists.BoxArtist`
* Removed `layer` attribute from `compas_rhino.artists.Artist`.
* Removed `clear_layer` method from `compas_rhino.artists.Artist`.

## [0.13.2] 2020-01-06

### Added

* File reading functions for ascii files in `compas.files` has moved from the individual reader classes to a new parent class, `BaseReader`.

### Changed

* Rebased `compas_rhino.artists.MeshArtist` on new-style artist `compas_rhino.artists.Artist`.
* Renamed `compas_rhino.artists.MeshArtist.defaults` to `compas_rhino.artists.MeshArtist.settings`.
* Changed usage of (nonexisting) `compas_rhino.get_object` to `compas_rhino.get_objects`.
* Integrated vertex, face, edge mixins into `compas_rhino.artists.MeshArtist`.
* Integrated vertex, edge mixins into `compas_rhino.artists.NetworkArtist`.
* Rebased `compas_rhino.artists.VolMeshArtist` on `compas_rhino.artists.MeshArtist`.

### Removed

## [0.13.0] 2019-12-16

### Added

* Added DOI to bibtex entry.
* Added conversion for old mesh JSON data.

### Changed

* Indirectly changed mesh serialisation to JSON (by changing key conversion and moving conversion into JSON methods).
* Moved conversion of int keys of mesh data to strings for json serialisation to from/to json.
* Moved from/to methods for mesh into mesh definition.
* Subdivision algorithms use fast mesh copy.

### Removed

* Support for non-integer vertex and face identifiers in mesh.

## [0.12.4] 2019-12-11

### Added

### Changed

### Removed

## [0.12.3] 2019-12-11

### Added

* Added `mesh_subdivide_frames` to `compas.datastructures.subdivision`

### Changed

### Removed

## [0.12.2] 2019-12-11

### Added

* Added `intersection_segment_polyline` to `compas.geometry.intersections`
* Added `intersection_segment_polyline_xy` to `compas.geometry.intersections`
* Added `from_sides_and_radius` to `compas.geometry.Polygon`

### Changed

* Reworked docstrings of methods in `compas.geometry.queries`
* Set default `tol` to `1e-6` in `compas.geometry.queries`

### Removed

## [[0.12.1] 2019-12-10] 2019-12-10

### Added

* Added inherited methods to class docs.
* Added data structure mixins to the docs.
* Added `data` and `from_data` to `compas.geometry.Polyhedron`
* Added explicit support for collections to `compas_blender`

### Changed

* Bottom face of cylinder shape should be flipped.
* Face reading mechanism of OFF reader.
* `compas.geometry.Box` is now centred at origin by default.

### Removed

* Removed `compas.remote` because it does not provide an advatage over `compas.rpc`.

## [[0.11.4] 2019-11-26] 2019-11-26

### Added

* Added `compas_rhino.etoforms.ImageForm`.
* Added `doc8` as dev requirement.

### Changed

* Changed `compas_rhino.install_plugin` to use only the plugin name, w/o the GUID.
* Changed `iterable_like` to prevent exhausting generators passed as targets.

### Removed

* Removed `compas_rhino.ui.Controller`.
* Removed `compas_rhino.ui.Button`.

## [[0.11.2] 2019-11-19] 2019-11-19

### Added

* Added factory methods for `compas_rhino.artists._Artist`

### Changed

* Set `compas_rhino.artists.FrameArtist` layer clear to false by default.
* Wrapped internals of RPC dispatch method in try-except to catch any import problems and report back on the client side.
* Stopping of HTTP server (`compas.remote`) is now handled properly through separate thread.
* Fixed mutable init parameters of `RobotModel`
* Fixed bug in `mesh_quads_to_triangles` that caused face data to be deleted even when not necessary.
* Switched to `compas.geometry.KDTree` as fallback for `scipy.spatial.cKDTree` instead of Rhino `RTree` because it currently fails.

### Removed

## [0.11.0] 2019-11-09

### Added

* Added `iterable_like` to `compas.utilities.itertools_`
* Added `compas.geometry.icp_numpy` for pointcloud alignment using ICP.
* Added RPC command-line utility: `$ compas_rpc {start|stop} [--port PORT]`
* Added `__version__` to `compas_plotters`.
* Added `compas_plotters` to `.bumpversion.cfg`.
* Added `Colormap` to `compas.utilities`.
* Added `is_line_line_colinear()` to `compas.geometry`
* Added link to Github wiki for devguide.
* Added pointcloud alignment example to docs.
* Show git hash on `compas.__version__` if installed from git.
* Added `autopep8` to dev requirements.
* Added methods `add_joint` and `add_link` to `RobotModel`
* Added support for geometric primitives to JSON data encoder and decoder.
* Added support for `data` to all geometric primitives.

### Changed

* Docs are only deployed to github pages for tagged commits.
* Fixing printing issue with `compas.geometry.Quarternion` in ironPython.
* Fixed a missing import in `compas.geometry.Polygon`.
* Removed unused imports in `compas.geometry.Polyline`.
* Adjusted `compas.geometry.Quarternion.conjugate()` to in-place change, added `compas.geometry.Quarternion.conjugated()` instead which returns a new quarternion object.
* Fixed `rotation` property of `Transformation`.
* Simplified plugin installation (use plugin name only, without GUID).
* Bind RPC server to `0.0.0.0` instead of `localhost`.
* Fixed different argument naming between Rhino5 and Rhino6 of `rs.LayerVisible()` in `compas_rhino.utilities.objects`.

### Removed

## [0.10.0] 2019-10-28

### Added

* Added method for computing the determinant of the matrix of a transformation `compas.geometry.Transformation.determinant`.
* Added method for transposing (the matrix of) a transformation in-place `compas.geometry.Transformation.transpose`.
* Added method creating a transposed copy of a transformation `compas.geometry.Transformation.transposed`.
* Added method for invertig (the matrix of) a transformation in-place `compas.geometry.Transformation.invert`.
* Added `compas.geometry.Transformation.inverted` as an alias for `compas.geometry.Transformation.inverse`.
* Added method creating a copy of a transformation instance with a given transformation concatenated `compas.geometry.Transformation.concatenated`.
* Added method `to_vertices_and_faces` to all the classes inheriting from `compas.geometry.Shape` to create a `Mesh` representation of them.

### Changed

* Changed `compas.geometry.Transformation.inverse` to return an inverted copy of the transformation.
* Changed `compas.geometry.Transformation.decompose` to `compas.geometry.Transformation.decomposed`.
* Changed `compas.geometry.Transformation.concatenate` to add another transformation to the transformation instance.

### Removed

## [0.9.1] 2019-10-28

### Added

* Added `compas.geometry.Point.transform_collection` and `compas.geometry.Point.transformed_collection`.
* Added `compas.geometry.Vector.transform_collection` and `compas.geometry.Vector.transformed_collection`.
* Added `compas.geometry.Line.transform_collection` and `compas.geometry.Line.transformed_collection`.
* Added support for new Python plugin location for Rhino 6.0 on Mac.
* Added `compas.geometry.bestfit_frame_numpy`

### Changed

* Fixed transformation of start and end point of `compas.geometry.Line` to update the point objects in place.
* Fixed return value of `compas.numerical.pca_numpy` to return mean not as nested list.

### Removed

## [0.9.0] 2019-10-21

### Added

* Added `matrix_change_basis`, `Transformation.change_basis`
* Added `matrix_from_frame_to_frame`
* Added non-numpy versions of `global_coords`, `local_coords`
* Added static method `Frame.local_to_local_coords`
* Added `__getitem__`, `__setitem__` and `__eq__` to `Quaternion`
* Added `Vector.scaled` and `Vector.unitized`
* Added `transform_frames` and respective helper functions `dehomogenize_and_unflatten_frames`, `homogenize_and_flatten_frames`
* Added `transform_frames_numpy` and respective helper functions `dehomogenize_and_unflatten_frames_numpy`, `homogenize_and_flatten_frames_numpy`

### Changed

* Renamed `global_coords_numpy` and `local_coords_numpy` to `local_to_world_coords_numpy` and `world_to_local_coords_numpy`.
* Changed parameters `origin` `uvw` of `local_to_world_coords_numpy` and `world_to_local_coords_numpy` to `frame`.
* Fixed some returns of `Frame` and `Rotation` to use `Vector` or `Quaternion`
* Renamed methods `Frame.represent_point/vector/frame_in_global_coordinates` and `Frame.represent_point/vector/frame_in_local_coordinates` to `Frame.to_local_coords` and `Frame.to_world_coords`.

### Removed

## [0.8.1] 2019-10-01

### Added

### Changed

* Fixed unguarded import of `numpy` based transformations in mesh package.

### Removed

## [0.8.0] 2019-10-01

### Added

* Added test section for `compas.geometry.transformations`
* Added `tol` parameter to `queries.is_colinear`
* Added compas rhino installer for Rhino Mac 6.0 `compas_rhino.__init__`.
* Added oriented bounding box for meshes `compas.datastructures.mesh_oriented_bounding_box_numpy`.
* Added full testing functions for `compas.datastructures.mesh`
* Added `draw_mesh` to `compas_ghpython.artists.MeshArtist`

### Changed

* Generate sphinx documentation from markdown files in repo root for top level sections.
* Merged `compas.geometry.xforms` into `compas.geometry.transformations`
* Fixed `AttributeError: 'Mesh' object has no attribute 'neighbors'`
* Fixed Key error with `Mesh.boundary()`
* Extended `offset_polygon` and `offset_polyline` to handle colinear segments
* Fixed unsorted mesh vertex coordinates `xyz` in `compas_viewers.viewer.MeshView`
* Changed stderr parameter from STDOUT to PIPE in `compas.rpc.Proxy` for Rhino Mac 6.0.
* Fixed import of `delaunay_from_points` in `Mesh.from_points`.
* More control over drawing of text labels in Rhino.
* Extension of `face_vertex_descendant` and `face_vertex_ancestor` in `Mesh`.
* Changed the name and meaning of the parameter `oriented` in the function `Mesh.edges_on_boundary`.
* Add `axis` and `origin` defaults to `compas.robots.Joint`
* Unified vertices and face import order for .obj files with python2 and 3
* Changed python interpreter selection (e.g. RPC calls) to fallback to `python` if `pythonw` is not present on the system
* Fixed `compas_ghpython.artists.MeshArtist` to support ngons.
* Deprecate the method `draw` of `compas_ghpython.artists.MeshArtist` in favor of `draw_mesh`.
* Fix icosahedron generation
* Examples in docs/rhino updated to work with current codebase
* Callbacks tutorial updated to work with current codebase
* Base geometric primitives on `compas.geometry.Primitive` and `compas.geometry.Shape`
* Separated `numpy` based tranformations into separate module.

### Removed

* Removed `compas_viewers` to separate repo.
* Removed `compas_hpc` to separate repo.

## [0.7.2] 2019-08-09

### Added

* Added `compas_rhino.geometry.RhinoGeometry` to the docs.
* Added `compas.remote.services`.
* Added `compas.remote.services.network.py` service for handling requests for a browser-based network viewer.
* Possibility to call forward_kinematics on `compas.robots.RobotModel`
* Added `compas.set_precision` function for the setting the global precision used by COMPAS as a floating point number.

### Changed

* Fix mesh genus in `compas.datastructures`.
* Fixed missing import in `compas_rhino.geometry`.
* Removed circular imports from `compas_rhino.geometry`.
* Fix duplicate hfkeys in `compas.datastructures.volmesh.halffaces_on_boundary`.
* Moved `compas.remote.service.py` to `compas.remote.services.default.py`.
* Removed processing of face keys from data getter and setter in `compas.datastructures.Network`.
* Using `SimpleHTTPRequestHandler` instead of `BaseHTTPRequestHandler` to provide basic support for serving files via `GET`.
* Mesh mapping on surface without creating new mesh to keep attributes in `compas_rhino.geometry.surface.py`.
* Moving functionality from `compas_fab.artists.BaseRobotArtist` to `compas.robots.RobotModel`
* Fix exception of null-area polygon of centroid polygon in `compas.geometry.average.py`.
* Fix loss of precision during mesh welding in `compas.datastructures.mesh_weld`.

### Removed

## [0.7.1] 2019-06-29

### Added

### Changed

* Include `compas_plotters` and `compas_viewers` in the build instructions.
* Moved import of `subprocess` to Windows-specific situations.
* Fixed document functions failing when document name is `None`.
* Downgraded `numpy` requirements.
* Loosened `scipy` requirements.
* Default Python to `pythonw`.

### Removed

## [0.7.0] 2019-06-27

### Added

* Added filter shorthand for selecting OBJ, JSON files in Rhino.
* Added `compas_plotters`
* Added `compas_viewers`
* Added `compas_rhino.draw_circles` and the equivalent Artist method
* Add class functions to `compas.datastructures.VolMesh`.
* Added `face_neighborhood` class function to `compas.datastructures.Mesh`.
* Added `get_face_attributes_all` to `compas.datastructures._mixins.attributes`.
* Added `get_faces_attributes_all` to `compas.datastructures._mixins.attributes`.
* Added `compas.remote` package for making HTTP based Remote Procedure Calls.

### Changed

* Restructure halffaces as lists in `compas.datastructures.VolMesh`.
* Correctly handle `python-net` module presence during IronPython imports.
* Switched to `compas.IPY` check instead of `try-except` for preventing non IronPython friendly imports.
* Changed installation of compas packages to Rhino to support non-admin user accounts on Windows.
* Copy facedata in `mesh_quads_to_triangles`
* Added non-imported service for `compas.remote` for starting the subprocess that runs the server.

### Removed

* Removed `compas.plotters`
* Removed `compas.viewers`

## [0.6.2] 2019-04-30

### Added

### Changed

* Based mesh drawing for Rhino on RhinoCommon rather than Rhinoscriptsyntax.
* Fixed mesh drawing for Rhino 6

### Removed

## [0.6.1] 2019-04-29

### Added

### Changed

* Fixed bug in RPC. The services cannot have a `pass` statement as class body.

### Removed

## [0.6.0] 2019-04-29

### Added

* Added `center` property getter to `compas.geometry.Cirle` primitive
* Add `astar_shortest_path` to `compas.topology.traversal`.

### Changed

* Updated configuration instructions for Blender.
* Changed naming convention for drawing functions from `xdraw_` to `draw_`.
* Changed mesh drawing in Rhino to use separate mesh vertices per face. This makes the mesh look more "as expected" in *Shaded* view.

### Removed

* Removed support for Python 3.5.x by setting the minimum requirements for Numpy and Scipy to `1.16` and `1.2`, respectively.

## [0.5.2] 2019-04-12

### Added

* Added `draw_polylines` to `compas_rhino.artists.Artist`.
* Added `color` argument to `compas_rhino.artists.MeshArtist.draw_mesh`.
* Added named colors to `compas.utilities.colors.py`.

### Changed

* Fix `mesh_uv_to_xyz` in `RhinoSurface`.
* Fix 'mesh_weld' and 'meshes_join_and_weld' against consecutive duplicates in face vertices.
* Fix setting of environment variables in `System.Diagnostics.Process`-based subprocess for `XFunc` and `RPC`.
* Fix `XFunc` on RhinoMac.
* Fix `trimesh_subdivide_loop` from `compas.datastructures`.
* Changed Numpy and Scipy version requirements to allow for Python 3.5.x.

### Removed

* Removed `mixing.py` from `compas.utilities`.
* Removed `singleton.py` from `compas.utilities`.
* Removed `xscript.py` from `compas.utilities`.
* Removed `sorting.py` from `compas.utilities`.
* Removed `names.py` from `compas.utilities`.
* Removed `xfunc.py` from `compas_rhino.utilities`, use `compas.utilities.XFunc` instead.

## [0.5.1] 2019-03-25

### Added

### Changed

* Fix `XFunc` and `RPC` environment activation.
* Fix exception on Rhino Mac.
* Fix missing import on `compas_rhino.geometry`.
* Fix `compas.geometry.offset_polygon`.
* Fix installation for Rhino, related to implicit import of `matplotlib`.

### Removed

## [0.5.0] 2019-03-15

### Added

* Add `Circle` and `Sphere` primitives to `compas.geometry`.
* Add functions to `Plane` and `Box` primitives.
* Add functions to `compas_rhino` curve: `length` and `is_closed`.
* Add functions to `compas_rhino` surface: `kinks`, `closest_point`, `closest_point_on_boundaries`, and functions for mapping/remapping between XYZ and UV(0) spaces based on surface's parametrization (`point_xyz_to_uv`, `point_uv_to_xyz`, `line_uv_to_xyz`, `polyline_uv_to_xyz`, `mesh_uv_to_xyz`)
* Add `is_scalable` to `compas.robots.Joint`.

### Changed

* Fix exception in `Plane.transform`.
* Fix installer to remove old symlinks.
* Fix RPC proxy server.

## [0.4.22] 2019-03-05

### Added

* Add pretty print option to JSON formatter.
* Add remeshing based on `triangle`.
* Add compatibility with ETO forms to `compas_rhino` edge modifiers.

## [0.4.21] 2019-03-04

### Changed

* Fix import in `compas_rhino` vertex modifiers.

## [0.4.20] 2019-03-04

### Removed

* Remove `download_image_from_remote` utility function.

## [0.4.12] 2019-03-04

### Changed

* Small fixes on Rhino forms support.

## [0.4.11] 2019-03-03

### Added

* New function to join network edges into polylines: `network_polylines`.
* New mesh functions: `mesh_offset`, `mesh_thicken`, `mesh_weld` and `meshes_join_and_weld`.
* New mesh functions: `face_skewness`, `face_aspect_ratio`, `face_curvature` and `vertex_curvature`.
* New functions to get disconnected elements of  `Mesh`: `mesh_disconnected_vertices`, `mesh_disconnected_faces`, `mesh_explode`.
* New functions to get disconnected elements of  `Network`: `network_disconnected_vertices`, `network_disconnected_edges`, `network_explode`.
* Add statistics utility functions: `average`, `variance`, `standard_deviation`.
* Add `binomial_coefficient` function.
* Add option to create `Network` and `Mesh` from dictionaries of vertices and faces.
* Add `face_adjacency_vertices` to `Mesh`
* Add optional prefix to the rhino name attribute processor
* Add `mesh_move_vertices` to `compas_rhino`.
* Add support for relative mesh references in URDF.

### Changed

* Fix mesh centroid and mesh normal calculation.
* Refactor of drawing functions in `compas_blender`.
* Fix material creation in `compas_blender`.
* New default for subdivision: `catmullclark`.

## [0.4.9] 2019-02-10

### Added

* New class methods for `Polyhedron`: `from_platonicsolid` and `from_vertices_and_faces`.
* Constrained and conforming Delaunay triangulations based on Triangle.
* Predicate-based filtering of vertices and edges.
* `mesh.geometry`for geometry-specific functions.
* `trimesh_face_circle` in `mesh.geometry`.

### Changed

* Fix exception in `angle_vectors_signed` if vectors aligned
* Fix exception in `Polyline.point`
* Update Rhino installation merging Win32 and Mac implementations and defaulting the bootstrapper to the active python even if no CONDA environment is active during install.

### Removed

* Bound mesh operations.

## [0.4.8] 2019-01-28

### Added

* Curve tangent at parameter.
* Box shape.
* Numpy-based mesh transformations.
* Option to share axes among plotters.
