# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added
* Implemented `to_points` method in `compas.datastructures.Mesh`, which before raised a `NotImplementedError`.
* Implemented `compute_aabb` method in `compas.datastructures.Datastructure`, which before raised a `NotImplementedError`. Made use of the `compas.geometry.bbox.bounding_box` function.
* Implemented `compute_obb` method in `compas.datastructures.Datastructure`, which before raised a `NotImplementedError`. Made use of the `compas.geometry.bbox_numpy.oriented_bounding_box_numpy` function.
* Added `vertices_to_points` method in `compas.datastructures.CellNetwork`.
* Added `to_points` method in `compas.datastructures.VolMesh`.
* Added test function `test_vertices_to_points`in `test_cell_network.py`.
* Added test function `test_to_points` in `test_graph.py`.
* Added test function `test_to_points` in `test_volmesh.py`.
* Added test functions `test_to_points`, `test_compute_aabb`, and `test_compute_obb` in `test_mesh.py`.
* Added `to_step` method to `RhinoBrep`.

### Changed

### Removed


## [2.13.0] 2025-06-04

### Added

* Added `compas.scene.Scene.add_group()` for adding group.
* Added `compas.scene.Group.add_from_list()` for adding a list of items to a group.
* Added implementation for `compas.geometry.SphericalSurface.isocurve_u`.
* Added implementation for `compas.geometry.SphericalSurface.isocurve_v`.
* Added implementation for `compas.geometry.CylindricalSurface.isocurve_u`.
* Added implementation for `compas.geometry.CylindricalSurface.isocurve_v`.

### Changed

* Fixed error in `circle_to_compas` from Rhino.
* Fixed Rhino to Rhino brep serialization.
* Upated `compas.scene.Group.add()` to pass on group kwargs as default for child items.
* Fixed bug in context detection, which wrongly defaults to `Viewer` instead of `None`.
* Fixed bug in calculation of `compas.geometry.Polyhedron.edges` if geometry is computed using numpy.
* Fixed bug in `Grpah.from_pointcloud` which uses degree parameter wrongly.

### Removed


## [2.12.0] 2025-05-28

### Added

* Added `inheritance` field to `__jsondump__` of `compas.datastructures.Datastructure` to allow for deserialization to closest available superclass of custom datastructures.

### Changed

### Removed


## [2.11.0] 2025-04-22

### Added

* Added `Group` to `compas.scene`.
* Added `compas.geometry.Brep.cap_planar_holes`.
* Added `compas_rhino.geometry.RhinoBrep.cap_planar_holes`.
* Added `compas.geometry.angle_vectors_projected`.
* Added `compas.geometry.Brep.from_curves`.
* Added `compas_rhino.geometry.RhinoBrep.from_curves`.
* Added missing property `centroid` in `compas_rhino.geometry.RhinoBrep`.
* Added missing property `curves` in `compas_rhino.geometry.RhinoBrep`.
* Added missing property `is_closed` in `compas_rhino.geometry.RhinoBrep`.
* Added missing property `is_compound` in `compas_rhino.geometry.RhinoBrep`.
* Added missing property `is_compoundsolid` in `compas_rhino.geometry.RhinoBrep`.
* Added missing property `is_orientable` in `compas_rhino.geometry.RhinoBrep`.
* Added missing property `is_surface` in `compas_rhino.geometry.RhinoBrep`.
* Added missing property `is_valid` in `compas_rhino.geometry.RhinoBrep`.
* Added missing property `orientation` in `compas_rhino.geometry.RhinoBrep`.
* Added missing property `surfaces` in `compas_rhino.geometry.RhinoBrep`.
* Added implementation for `Brep.from_sweep` in `compas_rhino.geometry.RhinoBrep`.
* Added implementation for `Brep.from_cone` in `compas_rhino.geometry.RhinoBrep`.
* Added implementation for `Brep.from_plane` in `compas_rhino.geometry.RhinoBrep`.
* Added implementation for `Brep.from_brepfaces` in `compas_rhino.geometry.RhinoBrep`.
* Added implementation for `Brep.from_breps` in `compas_rhino.geometry.RhinoBrep`.
* Added implementation for `Brep.from_torus` in `compas_rhino.geometry.RhinoBrep`.
* Added implementation for `Brep.from_polygons` in `compas_rhino.geometry.RhinoBrep`.
* Added implementation for `Brep.from_pipe` in `compas_rhino.geometry.RhinoBrep`.
* Added implementation for `Brep.from_iges` in `compas_rhino.geometry.RhinoBrep`.

### Changed

* Changed `SceneObject.frame` to read-only result of `Frame.from_transformation(SceneObject.worldtransformation)`, representing the local coordinate system of the scene object in world coordinates.
* Changed `SceneObject.worldtransformation` to the multiplication of all transformations from the scene object to the root of the scene tree, there will no longer be an additional transformation in relation to the object's frame.
* Fixed call to `astar_shortest_path` in `Graph.shortest_path`.
* Fixed a bug when printing an empty `Tree`.
* Fixed a bug in `Group` for IronPython where the decoding declaration was missing.
* Fixed a bug where a `Group` without name could not be added to the scene.

### Removed


## [2.10.0] 2025-03-03

### Added

* Added `flip` to `compas.geometry.Brep`.
* Added implementation of `flip` to `compas_rhino.geometry.RhinoBrep`.

### Changed

* Fixed unexpected behavior for method `Plane.is_parallel` for opposite normals.

### Removed


## [2.9.1] 2025-02-06

### Added

* Added method `frame_at` to `compas.geometry.BrepFace`.
* Added method `frame_at` to `compas_rhino.geometry.RhinoBrepFace`.
* Added property `is_reversed` to `compas.geometry.BrepFace`.
* Added property `is_reversed` to `compas_rhino.geometry.RhinoBrepFace`.

### Changed

* Fixed publish to YAK via CI workflow.
* Added selector for `test` and `prod` to CI workflow.
* Fixed `AttributeError` in `compas.data.DataEncoder.default` due to `np.float_` no longer being available in `numpy>=2`.

### Removed


## [2.9.0] 2025-02-04

### Added

* Added `DevTools` with support for automatic reloading of local python modules.
* Added implementation for `compas_rhino.geometry.RhinoBrep.from_step`.
* Added CPython implementations of GH components for Rhino8.
* Added import to new `yakerize` task from `compas_invocations2`.
* Added import to new `publish_yak` task from `compas_invocations2`.

### Changed

* Moved `unload_modules` to be a static method of `DevTools`. The `unload_modules` function is an alias to this. 
* Fixed unexpected behavior in `compas.geometry.bbox_numpy.minimum_area_rectangle_xy`.
* Changed `requirements.txt` to allow `numpy>=2`.
* Fixed bug in `compas.geometry.Polygon.points` setter by removing duplicate points if they exist.
* Fixed bug in `compas.geometry.Polygon.plane` by aligning the normal of the bestfit plane with the approximate normal of the polygon faces.
* Changed the order of face vertices in `compas.geometry.Surface.to_vertices_and_faces` to a counter clockwise cycling direction and outward facing normals for curved surfaces.
* Deprecated the `-v8.0` flag in `compas_rhino.install`. Install to Rhino8 by following: https://compas.dev/compas/latest/userguide/cad.rhino8.html.
* Fixed `Info` Grasshopper component for cpython to handle non-bootstrapped environments.

### Removed


## [2.8.1] 2025-01-15

### Added

### Changed

* Fixed `NotImplementedError` when calling `compas_rhino.conversions.surface_to_compas` on NURBS Surface.
* Fixed `NotImplementedError` when calling `compas_rhino.conversions.surface_to_compas` on Surface.
* Changed point comparison (`compas.geometry.Point.__eq__`) to use `TOL.is_allclose` instead of raw coordinate comparison.
* Changed vector comparison (`compas.geometry.Vector.__eq__`) to use `TOL.is_allclose` instead of raw coordinate comparison.
* Fixed bug in frame comparison (`compas.geometry.Frame.__eq__`).
* Fixed bug in `compas.geometry.oriented_bounding_box_numpy`.
* Fixed cannot copy `Line` using `deepcopy`.

### Removed


## [2.8.0] 2024-12-13

### Added

* Added implementation of `RhinoBrep.fillet()` and `RhinoBrep.filleted()` to `compas_rhino`.
* Added `Frame.invert` and `Frame.inverted`.
* Added `Frame.flip` and `Frame.flipped` as alias for invert and inverted.
* Added `Vector.flip` and `Vector.flipped` as alias for invert and inverted.

### Changed

* Fixed `native_edge` property of `RhinoBrepEdge`.
* Expose the parameters `radius` and `nmax` from `compas.topology._face_adjacency` to `compas.topology.face_adjacency` and further propagate them to `unify_cycles` and `Mesh.unify_cycles`.
* Modify `face_adjacency` to avoid using `compas.topology._face_adjacency` by default when there are more than 100 faces, unless one of the parameters `radius`, `nmax` is passed.
* Changed `unify_cycles` to use the first face in the list as root if no root is provided.

### Removed


## [2.7.0] 2024-11-28

### Added

* Added attribute `start_vertex` to `compas.geometry.BrepTrim`.
* Added attribute `end_vertex` to `compas.geometry.BrepTrim`.
* Added attribute `vertices` to `compas.geometry.BrepTrim`.
* Added attribute `start_vertex` to `compas_rhino.geometry.RhinoBrepTrim`.
* Added attribute `start_vertex` to `compas_rhino.geometry.RhinoBrepTrim`.
* Added attribute `vertices` to `compas_rhino.geometry.RhinoBrepTrim`.

### Changed

* Fixed `PluginNotInstalledError` when using `Brep.from_boolean_*` in Rhino.
* Added support for `Polyline` as input for `compas_rhino.Brep.from_extrusion`.

### Removed


## [2.6.1] 2024-11-09

### Added

### Changed

* Fixed bug in `compas_rhino.scene.RhinoMeshObject.clear()`.

### Removed


## [2.6.0] 2024-11-08

### Added

* Added key conversion map to `compas.colors.ColorDict` to avoid serialisation problems with tuple keys when used in combination with edges.
* Added `Scene.find_all_by_itemtype`.

### Changed

* Fixed bug in `VolMesh.delete_cell`.
* Fixed `NoneType` error when calling `compas.geometry.Sphere.edges`.
* Fixed bug in `VolMesh.vertex_halffaces`.
* Fixed bug in `VolMesh.vertex_cells`.
* Fixed bug in `VolMesh.is_halfface_on_boundary`.

### Removed

* Removed `VolMesh.halfface_adjacent_halfface` because of general nonsensicalness, and because it is (and probably always has been) completely broken.


## [2.5.0] 2024-10-25

### Added

* Added instructions for creating new data types to the dev guide.
* Added `compact=False`, `minimal=False` to `compas.data.Data.to_json()` to `compas.data.Data.to_jsonstring()`.
* Added `copy_guid=False` to `compas.data.Data.copy()`. If true, the copy has the same guid as the original.
* Added implementation of `Brep.from_loft()` to `compas_rhino`.

### Changed

* Fixed `RuntimeError` when using `compas_rhino.unload_modules` in CPython`.
* Fixed bug in `Box.scaled` causing a `TypeError` due to incorrect parameter forwarding.
* Changed argument names of `Box.scale()` to `x`, `y`, `z`, instead of `factor` and made `y` and `z` optional to keep positional arguments backwards compatible.
* Fixed import errors in `compas_rhino.conduits` for Rhino 8.
* Fixed doctest failures.
* Fixed bug in serialization when `compas.datastructures.attributes.AttributeView` is used.
* Fixed bug in the serialisation of empty scenes.
* Fixed bug in serialisation process due to `name` attribute appearing in json representation after copy even if not present before copy.

### Removed


## [2.4.3] 2024-10-04

### Added

### Changed

* Fixed support for `compas_gpython` in Rhino 8 Grasshopper CPython components.
* Changed installation instructions for Rhino 8 in the user guide.
* Fixed `Graph.from_edges` always returning `None`.

### Removed

* Removed deprecated module `compas_ghpython.utilities`. For drawing functions, use `compas_ghpython.drawing` directly.

## [2.4.2] 2024-09-17

### Added

* Added `compas.scene.Scene.find_by_name` to find the first scene object with the given name.
* Added `compas.scene.Scene.find_by_itemtype` to find the first scene object with a data item of the given type.

### Changed

* Fixed args for `SceneObject` on Grasshopper `Draw` component.
* Replaced use of `Rhino.Geometry.VertexColors.SetColors` with a for loop and `SetColor` in `compas_ghpyton` since the former requires a `System.Array`.
* Fixed `Mesh.face_circle`.

### Removed


## [2.4.1] 2024-08-25

### Added

### Changed

* Changed supported Blender versions to latest LTS versions (3.3, 3.6, 4.2).
* Fixed bug in `compas_rhino.conversions.cone_to_compas`.
* Fixed bug in `compas_rhino.conversions.cylinder_to_compas`.
* Fixed bug in `compas_rhino.scene.RhinoMeshObject.draw_vertexnormals` (scale not used).
* Fixed bug in `compas_rhino.scene.RhinoMeshObject.draw_facenormals` (scale not used).
* Changed scene object registration to stop printing messages.

### Removed

## [2.4.0] 2024-08-22

### Added

* Added `compas.scene.Scene.redraw`.
* Added `compas.scene.Scene.context_objects` representing all objects drawn in the visualisation context by the scene.
* Added `compas.scene.Scene.clear_context` with optional `guids` to clear some or all objects from the visualisation context.
* Added `clear_scene` and `clear_context` parameters to `compas.scene.Scene.clear` to differentiate between removing objects from the scene internally or removing corresponding objects from the viz context, or both (default).
* Added `compas_rhino.conversions.extrusion_to_compas_box` as direct conversion of extrusion breps.

### Changed

* Changed the `__str__` of `compas.geometry.Frame`, `compas.geometry.Plane`, `compas.geometry.Polygon`, `compas.geometry.Polyhedron`, `compas.geometry.Quaternion` to use a limited number of decimals (determined by `Tolerance.PRECISION`). Note: `__repr__` will instead maintain full precision.
* Changed the `__str__` of `compas.geometry.Pointcloud` to print total number of points instead of the long list of points. Note: `__repr__` will still print all the points with full precision.
* Fixed bug in `Pointcloud.from_box()`.
* Changed `compas.scene.MeshObject` to not use vertex coordinate caching because it is too fragile.
* Changed `compas_rhino.scene.RhinoMeshObject` to keep track of element-guid pairs in dicts.
* Changed `compas.scene.Scene._guids` to a default value of `[]`.
* Fixed bug due to missing import in `compas_rhino.scene.graphobject`.
* Changed `compas_rhino.scene.RhinoMeshObject.draw_vertexnormals` to use the same selection of vertices as `draw_vertices`.
* Changed `compas_rhino.scene.RhinoMeshObject.draw_vertexnormals` to use the corresponding vertex color if no color is specified.
* Changed `compas_rhino.scene.RhinoMeshObject.draw_facenormals` to use the same selection of vertices as `draw_faces`.
* Changed `compas_rhino.scene.RhinoMeshObject.draw_facenormals` to use the corresponding face color if no color is specified.

### Removed


## [2.3.0] 2024-07-06

### Added

* Added code coverage report uploads to codecov.io.
* Added `compas.geometry.surfaces.surface.Surface.from_native`.
* Added `compas.geometry.surfaces.nurbs.NurbsSurface.from_plane`.
* Added `compas.geometry.surfaces.nurbs.NurbsSurface.from_cylinder`.
* Added `compas.geometry.surfaces.nurbs.NurbsSurface.from_extrusion`.
* Added `compas.geometry.surfaces.nurbs.NurbsSurface.from_frame`.
* Added `compas.geometry.surfaces.nurbs.NurbsSurface.from_interpolation`.
* Added `compas.geometry.surfaces.nurbs.NurbsSurface.from_revolution`.
* Added `compas.geometry.surfaces.nurbs.NurbsSurface.from_sphere`.
* Added `compas.geometry.surfaces.nurbs.NurbsSurface.from_torus`.
* Added `compas_rhino.geometry.surfaces.surface_from_native`.
* Added `compas_rhino.geometry.surfaces.nurbssurface_from_native`.
* Added `compas_rhino.geometry.surfaces.nurbssurface_from_cylinder`.
* Added `compas_rhino.geometry.surfaces.nurbssurface_from_fill`.
* Added `compas_rhino.geometry.surfaces.nurbssurface_from_torus`.
* Added `compas_rhino.geometry.surfaces.nurbs.NurbsSurface.from_corners`.
* Added `compas_rhino.geometry.surfaces.nurbs.NurbsSurface.from_cylinder`.
* Added `compas_rhino.geometry.surfaces.nurbs.NurbsSurface.from_frame`.
* Added `compas_rhino.geometry.surfaces.nurbs.NurbsSurface.from_sphere`.
* Added `compas_rhino.geometry.surfaces.nurbs.NurbsSurface.from_torus`.
* Added `compas.geometry.curves.curve.Curve.from_native`.
* Added `compas_rhino.geometry.curves.curve.Curve.from_native`.
* Added `compas_rhino.geometry.curves.nurbs.NurbsCurve.from_native`.
* Added `compas_rhino.conversions.breps.brep_to_compas_mesh`.
* Added `compas_rhino.conversions.docobjects.brepobject_to_compas`.
* Added `compas_rhino.conversions.docobjects.curveobject_to_compas`.
* Added `compas_rhino.conversions.docobjects.meshobject_to_compas`.
* Added `compas_rhino.conversions.docobjects.pointobject_to_compas`.
* Added `compas.datastructures.HashTree` and `compas.datastructures.HashNode`.

### Changed

* Fixed bug in `compas.geometry.curves.curve.Curve.reversed` by adding missing parenthesis.
* Fixed all doctests so we can run `invoke test --doctest`.
* Changed `compas.geometry.surfaces.surface.Surface.__new__` to prevent instantiation of `Surface` directly.
* Changed `compas.geometry.surfaces.nurbs.NurbsSurface.__new__` to prevent instantiation of `NurbsSurface` directly.
* Fixed bug in `compas.geometry.surfaces.nurbs.NurbsSurface.__data__`.
* Changed `compas.geometry.surfaces.nurbs.new_nurbssurface_from_...` to `nurbssurface_from_...`.
* Changed `compas.geometry.curves.curve.Curve.__new__` to prevent instantiation of `Curve` directly.
* Changed `compas.geometry.curves.nurbs.new_nurbscurve_from_...` to `nurbscurve_from_...`.
* Changed `compas.geometry.curves.nurbs.NurbsCurve.__new__` to prevent instantiation of `NurbsCurve` directly.
* Changed `compas_rhino.geometry.curves.new_nurbscurve_from_...` to `nurbscurve_from_...`.
* Fixed `compas_ghpython` Grasshopper components not included in published pakcage.
* Changed `compas.colors.Color.coerce` to take color as is, if it is already an instance of `compas.colors.Color`.
* Changed `compas_rhino.conversions.surfaces.surface_to_compas` to work only with surface geometry.
* Changed `compas_rhino.conversions.curves.curve_to_compas_line` to work only with geometry.
* Changed `compas_rhino.conversions.curves.curve_to_compas_circle` to work only with geometry.
* Changed `compas_rhino.conversions.curves.curve_to_compas_ellipse` to work only with geometry.
* Changed `compas_rhino.conversions.curves.curve_to_compas_polyline` to work only with geometry.
* Changed `compas_rhino.objects.get_point_coordinates` to deprecated (removed in v2.3).
* Changed `compas_rhino.objects.get_line_coordinates` to deprecated (removed in v2.3).
* Changed `compas_rhino.objects.get_polyline_coordinates` to deprecated (removed in v2.3).
* Changed `compas_rhino.objects.get_polygon_coordinates` to deprecated (removed in v2.3).
* Fixed a bug in `worldtransformation` of `compas.scene.SceneObject` to include the object's own frame.

### Removed

* Removed pluggable `compas.geometry.surfaces.surface.new_surface`.
* Removed pluggable `compas.geometry.surfaces.surface.new_surface_from_plane`.
* Removed `compas.geometry.surfaces.surface.Surface.from_plane`.
* Removed `compas.geometry.surfaces.surface.ConicalSurface.__new__`.
* Removed `compas.geometry.surfaces.surface.CylindricalSurface.__new__`.
* Removed `compas.geometry.surfaces.surface.PlanarSurface.__new__`.
* Removed `compas.geometry.surfaces.surface.SphericalSurface.__new__`.
* Removed `compas.geometry.surfaces.surface.ToroidalSurface.__new__`.
* Removed `compas.geometry.surfaces.nurbs.NurbsSurface.__init__`.
* Removed `compas_rhino.geometry.surfaces.new_surface`.
* Removed `compas_rhino.geometry.surfaces.new_nurbssurface`.
* Removed `compas_rhino.geometry.surfaces.nurbs.NurbsSurface.__from_data__`.
* Removed `compas_rhino.geometry.surfaces.surface.Surface.from_corners`.
* Removed `compas_rhino.geometry.surfaces.surface.Surface.from_cylinder`.
* Removed `compas_rhino.geometry.surfaces.surface.Surface.from_frame`.
* Removed `compas_rhino.geometry.surfaces.surface.Surface.from_sphere`.
* Removed `compas_rhino.geometry.surfaces.surface.Surface.from_torus`.
* Removed `compas.geometry.curves.arc.Arc.__new__`.
* Removed `compas.geometry.curves.bezier.Bezier.__new__`.
* Removed `compas.geometry.curves.conic.Conic.__new__`.
* Removed `compas.geometry.curves.polyline.Polyline.__new__`.
* Removed `compas.geometry.curves.curve.new_curve`.
* Removed `compas.geometry.curves.curve.new_nurbscurve`.
* Removed `compas_rhino.geometry.curves.new_curve`.
* Removed `compas_rhino.geometry.curves.new_nurbscurve`.
* Removed `compas_rhino.conversions.surfaces.data_to_rhino_surface`.
* Removed `compas_rhino.conversions.surfaces.surface_to_compas_data`.
* Removed `compas_rhino.conversions.surfaces.surface_to_compas_quadmesh`.
* Removed `compas_rhino.conversions.curves.curve_to_compas_data`.

## [2.2.1] 2024-06-25

### Added

### Changed

* Fixed error in `compas_ghpython` causing `Scene` to fail in Grasshopper.

### Removed

## [2.2.0] 2024-06-24

### Added

* Added `maxiter` parameter to `compas.geometry.icp_numpy`.
* Added `resolution_u` and `resolution_v` to `compas.geometry.Shape` to control discretisation resolution.
* Added `vertices`, `edges`, `faces`, `triangles` to `compas.geometry.Shape`.
* Added `points`, `lines`, `polygons` to `compas.geometry.Shape`.
* Added abstract `compute_vertices`, `compute_edges`, `compute_faces`, `compute_triangles` to `compas.geometry.Shape`.
* Added implementation of `compute_vertices`, `compute_edges`, `compute_faces` to `compas.geometry.Box`.
* Added implementation of `compute_vertices`, `compute_edges`, `compute_faces` to `compas.geometry.Capsule`.
* Added implementation of `compute_vertices`, `compute_edges`, `compute_faces` to `compas.geometry.Cone`.
* Added implementation of `compute_vertices`, `compute_edges`, `compute_faces` to `compas.geometry.Cylinder`.
* Added implementation of `compute_vertices`, `compute_edges`, `compute_faces` to `compas.geometry.Sphere`.
* Added implementation of `compute_vertices`, `compute_edges`, `compute_faces` to `compas.geometry.Torus`.
* Added `compas_blender.scene.ShapeObject`.
* Added `compas.geometry.vector.__radd__`.
* Added `compas.geometry.vector.__rsub__`.
* Added `compas.geometry.vector.__rmul__`.
* Added `compas.geometry.vector.__rtruediv__`.
* Added `VolMesh.cell_lines`, `VolMesh.cell_polygons`.
* Added `VolMesh.vertex_edges`.
* Added `VolMesh.from_meshes`.
* Added `VolMesh.from_polyhedrons`.

### Changed

* Changed `compas_ghpython/utilities/drawing.py` to remove `System` dependency.
* Fixed bug in `compas.geometry.ic_numpy`, which was caused by returning only the last transformation of the iteration process.
* Changed `compas.geometry.Geometry.scaled` to use `compas.geometry.Geometry.scale` on a copy.
* Changed `compas.geometry.Geometry.translated` to use `compas.geometry.Geometry.translate` on a copy.
* Changed `compas.geometry.Geometry.rotated` to use `compas.geometry.Geometry.rotate` on a copy.
* Changed `VolMesh._plane` back to point to a cell for every triplet of vertices.
* Fixed `VolMesh.add_halfface`, `VolMesh.add_cell`, `VolMesh.vertex_halffaces`, `VolMesh.vertex_cells`, `VolMesh.edge_halffaces`, `VolMesh.halfface_cell`, `VolMesh.halfface_opposite_cell`, `VolMesh.halfface_opposite_halfface`, `VolMesh.cell_neighbors`.
* Changed ordering of `Volmesh.edges()` to be deterministic.
* Changed ordering and direction of `Volmesh.vertex_edges()` to be deterministic.
* Changed check for empty vertices and faces to use `is None` to add support for `numpy` arrays.
* Changed order of `u` and `v` of `compas.geometry.SphericalSurface` to the match the excpected parametrisation.
* Changed `compas.geometry.Shape.to_vertices_and_faces` to use `Shape.vertices` and `Shape.faces` or `Shape.triangles`.
* Changed default of `compas.scene.descriptors.color.ColorAttribute` to `None` to support native coloring in CAD contexts.
* Changed `compas.colors.ColorDict.__data__` and `compas.colors.ColorDict.__from_data__` to properly support serialisation.
* Moved `compas_blender.utilities.drawing` to `compas_blender.drawing` with backward compatible imports and deprecation warning.
* Moved `compas_ghpython.utilities.drawing` to `compas_ghpython.drawing` with backward compatible imports and deprecation warning.
* Moved `compas_rhino.utilities.drawing` to `compas_rhino.drawing` with backward compatible imports and deprecation warning.
* Changed `draw_nodes` and `draw_edges` of `compas_blender.scene.GraphObject`, `compas_ghpython.scene.GraphObject`, and `compas_rhino.scene.GraphObject` to use only attributes instead of parameters.
* Changed `draw_vertices`, `draw_edges` and `draw_faces` of `compas_blender.scene.MeshObject`, `compas_ghpython.scene.MeshObject`, and `compas_rhino.scene.MeshObject` to use only attributes instead of parameters.
* Changed `draw_vertices`, `draw_edges` and `draw_faces` of `compas_blender.scene.VolMeshObject`, `compas_ghpython.scene.VolMeshObject`, and `compas_rhino.scene.VolMeshObject` to use only attributes instead of parameters.
* Changed registration of `Capsule`, `Cone`, `Cylinder`, `Sphere`, `Torus` to `ShapeObject` in `compas_blender.scene`.
* Updated `compas.geometry.vector.__mul__` to allow element-wise multiplication with another vector.
* Updated `compas.geometry.vector.__truediv__` to allow element-wise division with another vector.
* Fixed bug in registration `shapely` boolean plugins.
* Temporarily restrict `numpy` to versions lower than `2.x`.

### Removed

* Removed `System` dependency in `compas_ghpython/utilities/drawing.py`.
* Removed GH plugin for `compas.scene.clear` since it clashed with the Rhino version.

## [2.1.1] 2024-05-14

### Added

* Added `compas.geometry.Line.point_from_start` and `compas.geometry.Line.point_from_end`.
* Added `compas.geometry.Line.flip` and `compas.geometry.Line.flipped`.
* Added an `compas.geometry.Frame.interpolate_frame(s)` method
* Added `compas.colors.Color.contrast`.
* Added `compas.geometry.Brep.from_plane`.
* Added `compas.tolerance.Tolerance.angulardeflection`.
* Added `compas.tolerance.Tolerance.update_from_dict`.
* Added `compas.scene.SceneObject.scene` attribute.
* Added `compas.datastructures.CellNetwork.is_faces_closed`
* Added `compas.datastructures.CellNetwork.delete_edge`
* Added `compas.datastructures.CellNetwork.delete_cell`
* Added `compas.datastructures.CellNetwork.delete_face`
* Added `compas.datastructures.CellNetwork.cells_to_graph`
* Added `compas.datastructures.CellNetwork.face_plane`
* Added `compas.datastructures.CellNetwork.cell_volume`
* Added `compas.datastructures.CellNetwork.cell_neighbors`

### Changed

* Changed and update the `compas_view2` examples into `compas_viewer`.
* Changed and updated the `compas_view2` examples into `compas_viewer`.
* Changed `compas.scene.Scene` to inherent from `compas.datastructrues.Tree`.
* Changed `compas.scene.SceneObject` to inherent from `compas.datastructrues.TreeNode`.
* Changed `compas.geoemetry._core.predicates_3` bug fix in `is_coplanar` while loop when there are 4 points.
* Changed to implementation of `Mesh.unify_cycles` to use the corresponding function of `compas.topology.orientation`.
* Fixed bug in `compas.topology.orientation.unify_cycles`.
* Fixed bug in `Mesh.thickened`.
* Fixed various bugs in `compas.geometry.Quaternion`.
* Changed repo config to `pyproject.toml`.
* Fixed broken import in `copas.geometry.trimesh_smoothing_numpy`.
* Changed `RhinoBrep.trimmed` to return single result or raise `BrepTrimmingError` instead of returning a list.
* Changed order of imports according to `isort` and changed line length to `179`.
* Changed use of `compas.geometry.allclose` to `compas.tolerance.TOL.is_allclose`.
* Changed use of `compas.geometry.close` to `compas.tolerance.TOL.is_close`.
* Changed imports of itertools to `compas.itertools` instead of `compas.utilities`.
* Changed `compas.tolerance.Tolerance` to a singleton, to ensure having only library-wide tolerance values.
* Updated `compas_rhino.conversions.point_to_compas` to allow for `Rhino.Geometry.Point` as input.
* Changed `compas.datastructures.Tree.print_hierarchy` to `compas.datastructures.Tree.__str__`.
* Changed `compas.scene.SceneObject.__init__` to accept `item` as kwarg.
* Fixed `compas.geometry.bbox_numpy.minimum_volume_box` to avoid `numpy.linalg.LinAlgError`.

### Removed

* Removed `compas.scene.SceneObjectNode`, functionalities merged into `compas.scene.SceneObject`.
* Removed `compas.scene.SceneTree`, functionalities merged into `compas.scene.Scene`.
* Removed default implementation of `compas.geometry.trimesh_geodistance` since nonexistent.
* Removed `compas.utilities.geometric_key` and replaced it by `compas.tolerance.TOL.geometric_key`.
* Removed `compas.utilities.geometric_key_xy` and replaced it by `compas.tolerance.TOL.geometric_key_xy`.
* Removed indexed attribute access from all geometry classes except `Point`, `Vector`, `Line`, `Polygon`, `Polyline`.
* Removed `compas.datastructures.Tree.print_hierarchy`.

## [2.1.0] 2024-03-01

### Added

* Added optional argument `cap_ends` to `Brep.from_extrusion()`.
* Added implementation in `RhinoBrep.from_extrusion()`.
* Added `max_depth` to `compas.datastructures.Tree.print_hierarchy()`.
* Added `compas.datastructures.Tree.to_graph()`.

### Changed

* Changed `compas.datastructures.TreeNode` to skip serialising `attributes`, `name` and `children` if being empty.
* Changed `compas.datastructures.TreeNode.__repr__` to omit `name` if `None`.
* Fix bug in `compas_rhino.geometry.NurbsCurve.from_parameters` and `compas_rhino.geometry.NurbsCurve.from_points` related to the value of the parameter `degree`.
* Changed `compas.scene.descriptors.ColorDictAttribute` to accept a `compas.colors.ColorDict` as value.
* Changed `compas_rhino.scene.RhinoMeshObject.draw` to preprocess vertex and face color dicts into lists.
* Changed `compas_rhino.conversions.vertices_and_faces_to_rhino` to handle vertex color information correctly.
* Changed `compas_rhino.conversions.average_color` return type `compas.colors.Color` instead of tuple.

### Removed

## [2.0.4] 2024-02-12

### Added

### Changed

* Fixed bug in `compas_rhino.scene`.

### Removed

## [2.0.3] 2024-02-09

### Added

* Added `compas.linalg`.
* Added `compas.matrices`.
* Added `compas.itertools`.
* Added `compas_rhino.scene.helpers`.
* Added `compas.scene.SceneObject.contrastcolor`.

### Changed

* Fixed bug in `compas.geometry.oriented_bounding_box_numpy` to support points in plane.
* Changed `compas_rhino.scene.RhinoSceneObject` to pass on positional arguments.
* Changed `compas_rhino.scene.RhinoBoxObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoBrepObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoCapsuleObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoCircleObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoConeObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoCurveObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoCylinderObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoEllipseObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoFrameObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoGraphObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoLineObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoMeshObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoPlaneObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoPointObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoPolygonObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoPolyhedronObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoPolylineObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoSphereObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoSurfaceObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoTorusObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoVectorObject.draw` to use attributes only.
* Changed `compas_rhino.scene.RhinoVolMeshObject.draw` to use attributes only.

### Removed

* Removed `compas.geometry.linalg`.
* Removed `compas.topology.matrices`.
* Removed `compas.utilities.itertools`.

## [2.0.2] 2024-02-06

### Added

* Added Blender paths for Windows.
* Added `compas_rhino.print_python_path`.
* Added `compas_blender.print_python_path`.

### Changed

* Fixed bug in `compas.tolerange.Tolerance.format_number()` related to IronPython environment.

### Removed


## [2.0.1] 2024-02-01

### Added

* Added pluggable `compas.geometry.surfaces.nurbs.new_nurbssurface_from_native`.
* Added `compas.geometry.NurbsSurface.from_native`.
* Added plugin `compas_rhino.geometry.surfaces.new_nurbssurface_from_plane`.

### Changed

* Fixed bug in `compas_blender.clear`.
* Fixed bug in `compas_rhino.conversions.surface_to_compas`.
* Fixed bug in `compas_rhino.conversions.surface_to_compas_mesh`.
* Fixed bug in `compas_rhino.conversions.surface_to_compas_quadmesh`.
* Fixed bug in plugin `compas_rhino.geometry.curves.new_nurbscurve_from_native`.
* Fixed bug in plugin `compas_rhino.geometry.surfaces.new_nurbssurface_from_native`.

### Removed

* Removed plugin `compas_rhino.geometry.surfaces.new_surface_from_plane`.


## [2.0.0] 2024-01-31

### Added

* Added `group` attribute to `compas_rhino.scene.RhinoSceneObject`.
* Added `_guid_mesh`, `_guids_vertices`, `_guids_edges`, `_guids_faces`, `_guids_vertexlabels`, `_guids_edgelables`, `_guids_facelabels`, `_guids_vertexnormals`, `_guids_facenormals`, `_guids_spheres`, `_guids_pipes`, `disjoint` attributes to `compas_rhino.scene.MeshObject`.
* Added `_guids_nodes`, `_guids_edges`, `_guids_nodelabels`, `_guids_edgelables`, `_guids_spheres`, `_guids_pipes` attributes to `compas_rhino.scene.GraphObject`.
* Added `_guids_vertices`, `_guids_edges`, `_guids_faces`, `_guids_cells`, `_guids_vertexlabels`, `_guids_edgelables`, `_guids_facelabels`, `_guids_celllabels`, `disjoint` attributes to `compas_rhino.scene.MeshObject`.
* Added test for `compas.scene.Scene` serialisation.

### Changed

* Changed `compas.scene.Mesh`'s `show_vertices`, `show_edges`, `show_faces` to optionally accept a sequence of keys.
* Changed `compas.scene.Graph`'s `show_nodes`, `show_edges` to optionally accept a sequence of keys.
* Changed `compas.scene.VolMesh`'s `show_vertices`, `show_edges`, `show_faces`, `show_cells` to optionally accept a sequence of keys.
* Fixed missing implementation of `Sphere.base`.
* Fixed bug in `intersection_sphere_sphere`.

### Removed

* Removed kwargs from `compas_rhino.scene.MeshObject.draw`.
* Removed kwargs from `compas_rhino.scene.GraphObject.draw`.
* Removed kwargs from `compas_rhino.scene.VolMeshObject.draw`.

## [2.0.0-beta.4] 2024-01-26

### Added

* Added `compas_rhino.objects`.
* Added `compas_rhino.layers`.
* Added `compas_rhino.install_with_pip`.
* Added `before_draw` pluggable to `compas.scene.Scene.draw`.
* Added `after_draw` pluggable to `compas.scene.Scene.draw`.
* Added description in tutorial about `compas.scene.context`.
* Added `compas_blender.data`.
* Added `compas_blender.collections`.
* Added `compas_blender.objects`.
* Added `compas_rhino.ui`.
* Added `compas_rhino.unload_modules`.
* Added `compas_ghpython.unload_modules`.
* Added `compas_ghpython.sets`.
* Added `compas_ghpython.timer`.
* Added `scale` and `scaled` to `compas.datastructures.Datastructure`.
* Added `rotate` and `rotated` to `compas.datastructures.Datastructure`.
* Added `translate` and `translated` to `compas.datastructures.Datastructure`.

### Changed

* Changed `compas.tolerance.Tolerance` into singleton.
* Changed `compas_rhino.geometry.curves.nursb.RhinoNurbsCurve` to use private data API.
* Changed `compas_rhino.geometry.surfaces.nursb.RhinoNurbsSurface` to use private data API.
* Changed `compas.scene.Scene.redraw` to `draw`.
* Fixed `register_scene_objects` not called when there is a context given in kwargs of `SceneObject`.

### Removed

* Removed `compas_blender.geometry.curves`.
* Removed `compas_rhino.utilities.objects`.
* Removed `compas_rhino.utilities.layers`.
* Removed `compas_rhino.utilities.constructors`.
* Removed `compas_rhino.utilities.document`.
* Removed `compas_rhino.utilities.geometry`.
* Removed `compas_rhino.utilities.misc`.
* Removed `compas_blender.utilities.data`.
* Removed `compas_blender.utilities.collections`.
* Removed `compas_blender.utilities.objects`.
* Removed `compas_ghpython.utilities.sets`.
* Removed `compas_ghpython.utilities.timer`.

## [2.0.0-beta.3] 2024-01-19

### Added

* Added `compas.dtastructures.Network` as alias of `compas.datastructures.Graph`.
* Added `compas.data.Data.name` and included it in serialisation in case `compas.data.Data._name is not None`.

### Changed

* Merged `compas.datastructures.Halfedge` into `compas.datastructures.Mesh`.
* Merged `compas.datastructures.Network` into `compas.datastructures.Graph`.
* Merged `compas.datastructures.Halfface` into `compas.datastructures.VolMesh`.
* Fixed `RhinoBrep` doesn't get capped after trimming.
* Changed `compas.data.Data.data` to `compas.data.Data.__data__`.
* Changed `compas.data.Data.dtype` to `compas.data.Data.__dtype__`.
* Changed `compas.data.Data.from_data` to `compas.data.Data.__from_data__`.
* Changed `compas.geometry.triangulation_earclip` face vertex index reversion when the polygon is flipped.

### Removed

* Removed `compas.datastructures.Network`.
* Removed `compas.datastructures.Halfedge`.
* Removed `compas.datastructures.Halfface`.
* Removed `compas.data.Data.attributes`.
* Removed `compas.data.Datastructure.attributes`.
* Removed `attributes` from `compas.datastructures.Assembly.data`.
* Removed `attributes` from `compas.datastructures.CellNetwork.data`.
* Removed `attributes` from `compas.datastructures.Graph.data`.
* Removed `attributes` from `compas.datastructures.Mesh.data`.
* Removed `attributes` from `compas.datastructures.Tree.data`.
* Removed `attributes` from `compas.datastructures.VolMesh.data`.
* Removed `compas.data.Data.to_data`.
* Removed `compas.rpc.XFunc`.

## [2.0.0-beta.2] 2024-01-12

### Added

* Added `viewerinstance` in `compas.scene.Scene` to support viewers context detection.
* Added `compas_rhino8` as starting point for Rhino8 support.
* Added `compas.scene.SceneObjectNode`.
* Added `compas.scene.SceneTree`.
* Added `compas.scene.SceneObject.node`.
* Added `compas.scene.SceneObject.frame`.
* Added `compas.scene.SceneObject.worldtransformation`.
* Added `compas.scene.SceneObject.parent`.
* Added `compas.scene.SceneObject.children`.
* Added `compas.scene.SceneObject.add()`.
* Added tutorial for `compas.datastructures.Tree`.
* Added Serialisation capability to `compas.scene.Scene`.
* Added `show` flag to `compas.scene.SceneObject`.
* Added `show_points` flag to `compas.scene.GeometryObject`.
* Added `show_lines` flag to `compas.scene.GeometryObject`.
* Added `show_surfaces` flag to `compas.scene.GeometryObject`.
* Added `show_vertices` flag to `compas.scene.MeshObject`.
* Added `show_edges` flag to `compas.scene.MeshObject`.
* Added `show_faces` flag to `compas.scene.MeshObject`.
* Added `show_nodes` flag to `compas.scene.NetworkObject`.
* Added `show_edges` flag to `compas.scene.NetworkObject`.
* Added `show_vertices` flag to `compas.scene.VolMeshObject`.
* Added `show_edges` flag to `compas.scene.VolMeshObject`.
* Added `show_faces` flag to `compas.scene.VolMeshObject`.
* Added `show_cells` flag to `compas.scene.VolMeshObject`.
* Added `compas.data.Data.to_jsonstring` and `compas.data.Data.from_jsonstring`.
* Added `compas.data.Data.attributes`.
* Added optional param `working_directory` to `compas.rpc.Proxy` to be able to start services defined in random locations.
* Added `compas.datastructures.Datastructure.transform` and `compas.datastructures.Datastructure.transformed`.
* Added `compas.datastructures.Datastructure.transform_numpy` and `compas.datastructures.Datastructure.transformed_numpy`.
* Added `compas.datastructures.Halfedge.flip_cycles`.
* Added `compas.datastructures.Halfedge.is_connected`, `compas.datastructures.Halfedge.connected_vertices`, `compas.datastructures.Halfedge.connected_faces`.
* Added `compas.datastructures.Mesh.join`.
* Added `compas.datastructures.Mesh.weld` and `compas.datastructures.Mesh.remove_duplicate_vertices`.
* Added `compas.datastructures.Mesh.quads_to_triangles`.
* Added `compas.datastructures.Mesh.unify_cycles`.
* Added `compas.datastructures.Mesh.aabb` and `compas.datastructures.Mesh.obb`.
* Added `compas.datastructures.Mesh.offset` and `compas.datastructures.Mesh.thickened`.
* Added `compas.datastructures.Mesh.exploded`.
* Added `compas.datastructures.Mesh.adjacency_matrix`, `compas.datastructures.Mesh.connectivity_matrix`, `compas.datastructures.Mesh.degree_matrix`, `compas.datastructures.Mesh.laplacian_matrix`.
* Added `compas.topology.vertex_adjacency_from_edges`, `compas.topology.vertex_adjacency_from_faces`, `compas.topology.edges_from_faces`, `compas.topology.faces_from_edges`.
* Added `compas.datastructures.Network.split_edge`, `compas.datastructures.Network.join_edges`.
* Added `compas.datastructures.Network.smooth`.
* Added `compas.datastructures.Network.is_crossed`, `compas.datastructures.Network.is_xy`, `compas.datastructures.Network.is_planar`, `compas.datastructures.Network.is_planar_embedding`, `compas.datastructures.Network.count_crossings`, `compas.datastructures.Network.find_crossings`, `compas.datastructures.Network.embed_in_plane`.
* Added `compas.datastructures.Network.find_cycles`.
* Added `compas.datastructures.Network.shortest_path`.
* Added `compas.datastructures.Network.transform`.
* Added `compas.datastructures.Graph.is_connected`.
* Added `compas.datastructures.Graph.adjacency_matrix`, `compas.datastructures.Graph.connectivity_matrix`, `compas.datastructures.Graph.degree_matrix`, `compas.datastructures.Graph.laplacian_matrix`.

### Changed

* Changed the `__str__` of `compas.geometry.Point` and `compas.geometry.Vector` to use a limited number of decimals (determined by `Tolerance.PRECISION`). Note: `__repr__` will instead maintain full precision.
* Changed `docs` Workflow to only be triggered on review approval in pull requests.
* Changed `draw` implementations of `compas.scene.SceneObject` to always use the `worldtransformation` of the `SceneObject`.
* Fixed typo in name `Rhino.Geometry.MeshingParameters` in `compas_rhino.geometry.RhinoBrep.to_meshes()`.
* Fixed `TypeErrorException` when serializing a `Mesh` which has been converted from Rhino.
* Fixed color conversions in `compas_rhion.conversions.mesh_to_compas`.
* Changed `SceneObject` registration to allow for `None` context.
* Changed `compas.data.Data.name` to be stored in `compas.data.Data.attributes`.
* Changed `compas.data.Data.__jsondump__` to include `compas.data.Data.attributes` if the dict is not empty.
* Changed `compas.data.Data.__jsonload__` to update `compas.data.Data.attributes` if the attribute dict is provided.
* Changed `compas.datastructures.Graph` to take additional `**kwargs`, instead of only `name=None` specifically.
* Changed `compas.datastructures.Network` to take additional `**kwargs`, instead of only `name=None` specifically.
* Changed `compas.datastructures.Halfedge` to take additional `**kwargs`, instead of only `name=None` specifically.
* Changed `compas.datastructures.Mesh` to take additional `**kwargs`, instead of only `name=None` specifically.
* Moved registration of `ping` and `remote_shutdown` of the RPC server to `compas.rpc.Server.__init__()`.
* Moved `FileWatcherService` to `compas.rpc.services.watcher` so it can be reused.
* Changed `compas.datastructures.Mesh.subdivide` to `compas.datastructures.Mesh.subdivided`.
* Moved `compas.numerical.pca_numpy` to `compas.geometry.pca_numpy`.
* Moved `compas.numerical.scalafield_contours` to `compas.geometry.scalarfield_contours`.
* Moved `compas.numerical.matrices` to `compas.topology.matrices`.
* Moved `compas.numerical.linalg` to `compas.geometry.linalg`.
* Changed `watchdog` dependency to be only required for platforms other than `emscripten`.
* Changed `compas.geometry.earclip_polygon` algorithm because the current one does not handle several cases.

### Removed

* Removed `compas_rhino.forms`. Forms will be moved to `compas_ui`.
* Removed `compas.scene.NoSceneObjectContextError`.
* Removed `compas.datastructures.Datastructure.attributes` and `compas.datastructures.Datastructure.name` (moved to `compas.data.Data`).
* Removed `attributes` from `compas.datastructures.Graph.data`.
* Removed `attributes` from `compas.datastructures.Network.data`.
* Removed `attributes` from `compas.datastructures.Halfedge.data`.
* Removed `attributes` from `compas.datastructures.Mesh.data`.
* Removed `compas.datastructures.mesh_bounding_box` and `compas.datastructures.mesh_bounding_box_xy`.
* Removed `compas.datastructures.mesh_oriented_bounding_box_numpy` and `compas.datastructures.mesh_oriented_bounding_box_xy_numpy`.
* Removed `compas.datastructures.mesh_delete_duplicate_vertices`.
* Removed `compas.datastructures.mesh_is_connected` and `compas.datastructures.mesh_connected_components`.
* Removed `compas.datastructures.mesh_isolines_numpy` and `compas.datastructures.mesh_contours_numpy`.
* Removed `compas.datastructures.trimesh_gaussian_curvature`.
* Removed `compas.datastructures.trimesh_descent`.
* Removed `compas.datastructures.mesh_disconnected_vertices`, `compas.datastructures.mesh_disconnected_faces` and `compas.datastructures.mesh_explode`.
* Removed `compas.datastructures.mesh_geodesic_distances_numpy`.
* Removed `compas.datastructures.trimesh_face_circle`.
* Removed `compas.datastructures.mesh_weld`, `compas.datastructures.meshes_join`, `compas.datastructures.meshes_join_and_weld`.
* Removed `compas.datastructures.mesh_offset` and `compas.datastructures.mesh_thicken`.
* Removed `compas.datastructures.mesh_face_adjacency` and `compas.datastructures.mesh_unify_cycles`.
* Removed `compas.datastructures.mesh_transform`, `compas.datastructures.mesh_transformed`, `compas.datastructures.mesh_transform_numpy`, `compas.datastructures.mesh_transformed_numpy`.
* Removed `compas.datastructures.mesh_quads_to_triangles`.
* Removed `compas.datastructures.volmesh_bounding_box`.
* Removed `compas.datastructures.volmesh_transform` and `compas.datastructures.volmesh_transformed`.
* Removed `compas.topology.unify_cycles_numpy` and `compas.topology.face_adjacency_numpy`.
* Removed `compas.topology.unify_cycles_rhino` and `compas.topology.face_adjacency_rhino`.
* Removed `compas.datastructures.network_is_connected`.
* Removed `compas.datastructures.network_complement`.
* Removed `compas.datastructures.network_disconnected_nodes`, `compas.datastructures.network_disconnected_edges`, `compas.datastructures.network_explode`.
* Removed `compas.datastructures.network_adjacency_matrix`, `compas.datastructures.network_connectivity_matrix`, `compas.datastructures.network_degree_matrix`, `compas.datastructures.network_laplacian_matrix`.
* Removed `compas.datastructures.network_transform`, `compas.datastructures.network_transformed`.
* Removed `compas.datastructures.network_shortest_path`.
* Removed `compas.numerical`.

## [2.0.0-beta.1] 2023-12-20

### Added

* Added `compas.geometry.Box.to_brep()`.
* Added `compas.geometry.Cone.to_brep()`.
* Added `compas.geometry.Cylinder.to_brep()`.
* Added `compas.geometry.Sphere.to_brep()`.
* Added `compas.geometry.Torus.to_brep()`.
* Added `compas.brep.Brep.from_iges()`.
* Added `compas.brep.Brep.to_iges()`.
* Added `compas.tolerance`.
* Added `compas.tolerance.Tolerance`.
* Added `compas.tolerance.Tolerance.ABSOLUTE` and `compas.tolerance.Tolerance.absolute`.
* Added `compas.tolerance.Tolerance.RELATIVE` and `compas.tolerance.Tolerance.relative`.
* Added `compas.tolerance.Tolerance.ANGULAR` and `compas.tolerance.Tolerance.angular`.
* Added `compas.tolerance.Tolerance.APPROXIMATION` and `compas.tolerance.Tolerance.approximation`.
* Added `compas.tolerance.Tolerance.PRECISION` and `compas.tolerance.Tolerance.precision`.
* Added `compas.tolerance.Tolerance.LINEARDEFLECTION` and `compas.tolerance.Tolerance.lineardeflection`.
* Added `compas.tolerance.Tolerance.is_zero`.
* Added `compas.tolerance.Tolerance.is_positive`.
* Added `compas.tolerance.Tolerance.is_negative`.
* Added `compas.tolerance.Tolerance.is_between`.
* Added `compas.tolerance.Tolerance.is_angle_zero`.
* Added `compas.tolerance.Tolerance.is_close`.
* Added `compas.tolerance.Tolerance.is_allclose`.
* Added `compas.tolerance.Tolerance.is_angles_close`.
* Added `compas.tolerance.Tolerance.geometric_key`.
* Added `compas.tolerance.Tolerance.format_number`.
* Added `compas.tolerance.Tolerance.precision_from_tolerance`.
* Added `compas.scene.Scene`.
* Added `compas.json_loadz()` and `compas.json_dumpz()` to support ZIP compressed JSON files.
* Added `compas.datastructures.assembly.delete_part()`.
* Added `compas.datastructures.assembly.delete_connection()`.
* Added `compas.geometry.Brep.from_breps()`.
* Added `compas.geometry.Brep.from_planes()`.
* Added `compas.geometry.Brep.to_iges()`.
* Added `compas.geometry.Brep.to_meshes()`.
* Added `compas.geometry.Brep.to_polygons()`.
* Added `compas.geometry.Brep.to_stl()`.
* Added `compas.geometry.Brep.heal()`.
* Added `compas.geometry.Brep.edge_faces()`.
* Added `compas.geometry.Brep.edge_loop()`.
* Added `compas.geometry.Brep.fillet()`.
* Added `compas.geometry.Brep.filleted()`.
* Added `compas.geometry.BrepFilletError`.
* Added `compas.geometry.Brep.is_shell`.
* Added `compas.geometry.Brep.contains()`.
* Added `compas.geometry.BrepFace.adjacent_faces()`.
* Added `compas_rhino.geometry.RhinoBrep.is_manifold`.
* Added `compas_rhino.geometry.RhinoBrep.contains()`.
* Added `compas_rhino.geometry.RhinoBrepFace.adjacent_faces()`.
* Added `compas_rhino.geometry.RhinoBrepFace.as_brep()`.
* Added `compas.geometry.BrepEdge.orientation`.
* Added `compas.geometry.BrepEdge.type`.
* Added `compas.geometry.BrepEdge.length`.
* Added `compas.geometry.BrepFace.type`.
* Added `compas.geometry.BrepFace.add_loop()`.
* Added `compas.geometry.BrepFace.add_loops()`.
* Added `compas.geometry.BrepFace.to_polygon()` with generic implementation.
* Added `compas.geometry.BrepFace.try_get_nurbssurface()`.
* Added `compas_rhino.geometry.RhinoBrepFace.area`.
* Added `compas_rhino.geometry.RhinoBrepFace.centroid`.
* Added `compas_rhino.geometry.RhinoBrepFace.edges`.
* Added `compas_rhino.geometry.RhinoBrepFace.is_cone`.
* Added `compas_rhino.geometry.RhinoBrepFace.is_cylinder`.
* Added `compas_rhino.geometry.RhinoBrepFace.is_torus`.
* Added `compas_rhino.geometry.RhinoBrepFace.is_sphere`.
* Added `compas_rhino.geometry.RhinoBrepFace.nurbssurface`.
* Added `compas_rhino.geometry.RhinoBrepFace.vertices`.
* Added `compas_rhino.geometry.RhinoBrepLoop.trims`.
* Added `compas_rhino.geometry.RhinoBrepEdge.length`.
* Added `compas_rhino.geometry.RhinoBrepEdge.centroid`.
* Added `compas.geometry.BrepFace.native_face`.
* Added `compas.geometry.BrepEdge.native_edge`.
* Added `compas.geometry.BrepLoop.native_loop`.
* Added `compas.geometry.BrepTrim.native_trim`.
* Added `compas.geometry.BrepVertex.native_vertex`.
* Added `compas_rhino.geometry.RhinoBrepFace.native_face`.
* Added `compas_rhino.geometry.RhinoBrepEdge.native_edge`.
* Added `compas_rhino.geometry.RhinoBrepLoop.native_loop`.
* Added `compas_rhino.geometry.RhinoBrepTrim.native_trim`.
* Added `compas_rhino.geometry.RhinoBrepVertex.native_vertex`.
* Added `color`, `opacity` attributes to `compas.scene.SceneObject`.
* Added `pointcolor`, `linecolor`, `surfacecolor`, `pointsize`, `linewidth` attributes to `compas.scene.GeometryObject`.
* Added `compas_rhino.geometry.brep.RhinoBrep.to_meshes()`.
* Added `compas_blender.`
* Added `compas.geometry.Brep.trimmed()`.
* Added `compas.geometry.RhinoBrep.slice()`.

### Changed

* Changed `compas.geometry.NurbsSurface.u_space` to `space_u`.
* Changed `compas.geometry.NurbsSurface.v_space` to `space_v`.
* Changed `compas.geometry.NurbsSurface.u_isocurve` to `isocurve_u`.
* Changed `compas.geometry.NurbsSurface.v_isocurve` to `isocurve_v`.
* Changed `compas.brep.Brep.from_step_file` to `from_step`.
* Moved `compas.brep` to `compas.geometry.brep`.
* Updated `compas-actions.docs` workflow to `v3`.
* `Artists` classes are renamed to `SceneObject` classes and now under `compas.scene`, `compas_rhino.scene`, `compas_ghpython.scene`, `compas_blender.scene`.
* Context related functions like `register`, `build`, `redraw` and `clear` are moved to `compas.scene.context` from `compas.scene.SceneObject`.
* Changed plugin selection to fall back to a default implementation if possible.
* Fixed `AttributeError` `_edges` in `compas_rhino.geometry.RhinoBrepLoop.edges`.
* Fixed `compas_rhino.geometry.RhinoBrep` serialization.
* Naming convention for `ColorDictAttributes` in `compas.scene.MeshObject`, `compas.scene.NetworkObject` and `compas.scene.VolmeshObject` is changed e.g. from `vertex_color` to `vertexcolor`.
* The building of correct type of `SceneObject` is moved backed to `__new__` of `SceneObject` itself.
* Changed `compas_blender.install` to use symlinks.
* Moved `URDF` parsing from `compas.files` to the `compas_robots` extension (`compas_robots.files.URDF`).
* Changed signature of `compas.geometry.Brep.slice()`

### Removed

* Removed `compas_rhino.geometry.RhinoBrepFace.data.setter`.
* Removed `compas_rhino.geometry.RhinoBrepEdge.data.setter`.
* Removed `compas_rhino.geometry.RhinoBrepLoop.data.setter`.
* Removed `compas_rhino.geometry.RhinoBrepTrim.data.setter`.
* Removed `compas_rhino.geometry.RhinoBrepVertex.data.setter`.
* Removed `compas.PRECISION`.
* Removed `compas.set_precision`.

## [2.0.0-alpha.2] 2023-11-07

### Added

* Added `Frame.axes`
* Added `compas.datastructures.TreeNode` and `compas.datastructures.Tree` classes.
* Added `EllipseArtist` to `compas_rhino` and `compas_ghpython`.
* Added `compas.scene.Scene`.

### Changed

* Changed `Network.is_planar` to rely on `NetworkX` instead `planarity` for planarity checking.
* Removed `planarity` from requirements.
* Fixed argument order at `compas.geometry.cone.circle`.
* Pinned `jsonschema` version to >=4.17, <4.18 to avoid Rust toolchain
* Fixed `box_to_compas` in `compas_rhino.conversions` to correctly take in the center of the box as the center point of the frame.
* Removed `cython` from requirements.
* Made X and Y axis optional in the constructor of `Frame`.
* Moved `compas.geometry.brep` to `compas.brep`.
* Changed `networkx` version to `>=3.0` to ensure support for `is_planar`.
* Moved `compas.geometry.curves.nurbs_.py` and `compas.geometry.surfaces.nurbs_.py` to `compas_nurbs`.
* Fixed `mesh_to_compas` returning an empty `Mesh` when colors and/or face normals are missing.

### Removed


## [2.0.0-alpha.1] 2023-09-20

### Added

* Added `create_id` to `compas_ghpython.utilities`. (moved from `compas_fab`)
* Added representation for features in `compas.datastructures.Part`.
* Added `split` and `split_by_length` to `compas.geometry.Polyline`.
* Added `compas.rpc.XFunc`.
* Added attribute `compas.color.Color.DATASCHEMA`.
* Added attribute `compas.data.Data.DATASCHEMA`.
* Added attribute `compas.datastructures.Graph.DATASCHEMA`.
* Added attribute `compas.datastructures.Halfedge.DATASCHEMA`.
* Added attribute `compas.datastructures.Halfface.DATASCHEMA`.
* Added attribute `compas.geometry.Arc.DATASCHEMA`.
* Added attribute `compas.geometry.Bezier.DATASCHEMA`.
* Added attribute `compas.geometry.Box.DATASCHEMA`.
* Added attribute `compas.geometry.Capsule.DATASCHEMA`.
* Added attribute `compas.geometry.Circle.DATASCHEMA`.
* Added attribute `compas.geometry.Cone.DATASCHEMA`.
* Added attribute `compas.geometry.Cylinder.DATASCHEMA`.
* Added attribute `compas.geometry.Ellipse.DATASCHEMA`.
* Added attribute `compas.geometry.Frame.DATASCHEMA`.
* Added attribute `compas.geometry.Line.DATASCHEMA`.
* Added attribute `compas.geometry.NurbsCurve.DATASCHEMA`.
* Added attribute `compas.geometry.NurbsSurface.DATASCHEMA`.
* Added attribute `compas.geometry.Plane.DATASCHEMA`.
* Added attribute `compas.geometry.Point.DATASCHEMA`.
* Added attribute `compas.geometry.Pointcloud.DATASCHEMA`.
* Added attribute `compas.geometry.Polygon.DATASCHEMA`.
* Added attribute `compas.geometry.Polyhedron.DATASCHEMA`.
* Added attribute `compas.geometry.Polyline.DATASCHEMA`.
* Added attribute `compas.geometry.Sphere.DATASCHEMA`.
* Added attribute `compas.geometry.Torus.DATASCHEMA`.
* Added attribute `compas.geometry.Quaternion.DATASCHEMA`.
* Added attribute `compas.geometry.Vector.DATASCHEMA`.
* Added implementation of property `compas.color.Color.data`.
* Added `compas.data.Data.validate_data`.
* Added `compas.data.Data.__jsondump__`.
* Added `compas.data.Data.__jsonload__`.
* Added `compas.data.schema.dataclass_dataschema`.
* Added `compas.data.schema.dataclass_typeschema`.
* Added `compas.data.schema.dataclass_jsonschema`.
* Added `compas.data.schema.compas_jsonschema`.
* Added `compas.data.schema.compas_dataclasses`.
* Added `compas.datastructures.Graph.to_jsondata`.
* Added `compas.datastructures.Graph.from_jsondata`.
* Added `compas.datastructures.Halfedge.halfedge_loop_vertices`.
* Added `compas.datastructures.Halfedge.halfedge_strip_faces`.
* Added `compas.datastructures.Mesh.vertex_point`.
* Added `compas.datastructures.Mesh.vertices_points`.
* Added `compas.datastructures.Mesh.set_vertex_point`.
* Added `compas.datastructures.Mesh.edge_start`.
* Added `compas.datastructures.Mesh.edge_end`.
* Added `compas.datastructures.Mesh.edge_line`.
* Added `compas.datastructures.Mesh.face_points`.
* Added `compas.datastructures.Mesh.face_polygon`.
* Added `compas.datastructures.Mesh.face_circle`.
* Added `compas.datastructures.Mesh.face_frame`.
* Added `compas.datastructures.Graph.node_index` and `compas.datastructures.Graph.index_node`.
* Added `compas.datastructures.Graph.edge_index` and `compas.datastructures.Graph.index_edge`.
* Added `compas.datastructures.Halfedge.vertex_index` and `compas.datastructures.Halfedge.index_vertex`.
* Added `compas.geometry.Hyperbola`.
* Added `compas.geometry.Parabola`.
* Added `compas.geometry.PlanarSurface`.
* Added `compas.geometry.CylindricalSurface`.
* Added `compas.geometry.SphericalSurface`.
* Added `compas.geometry.ConicalSurface`.
* Added `compas.geometry.ToroidalSurface`.
* Added `compas.geometry.trimesh_descent_numpy`.
* Added `compas.geometry.trimesh_gradient_numpy`.
* Added `compas.geometry.boolean_union_polygon_polygon` pluggable.
* Added `compas.geometry.boolean_intersection_polygon_polygon` pluggable.
* Added `compas.geometry.boolean_difference_polygon_polygon` pluggable.
* Added `compas.geometry.boolean_symmetric_difference_polygon_polygon` pluggable.
* Added `compas.geometry.boolean_union_polygon_polygon` Shapely-based plugin.
* Added `compas.geometry.boolean_intersection_polygon_polygon` Shapely-based plugin.
* Added `compas.geometry.boolean_difference_polygon_polygon` Shapely-based plugin.
* Added `compas.geometry.boolean_symmetric_difference_polygon_polygon` Shapely-based plugin.
* Added `compas.geometry.Pointcloud.from_ply`.
* Added `compas.geometry.Curve.to_points`.
* Added `compas.geometry.Curve.to_polyline`.
* Added `compas.geometry.Curve.to_polygon`.
* Added `compas.geometry.Surface.to_vertices_and_faces`.
* Added `compas.geometry.Surface.to_triangles`.
* Added `compas.geometry.Surface.to_quads`.
* Added `compas.geometry.Surface.to_mesh`.
* Added `compas.geometry.Curve.point_at`.
* Added `compas.geometry.Curve.tangent_at`.
* Added `compas.geometry.Curve.normal_at`.
* Added `compas.geometry.Surface.point_at`.
* Added `compas.geometry.Surface.normal_at`.
* Added `compas.geometry.Surface.frame_at`.
* Added `compas.geometry.Polyline.parameter_at`.
* Added `compas.geometry.Polyline.divide_at_corners`.
* Added `mesh_to_rhino` to `compas_rhino.conversions`.
* Added `vertices_and_faces_to_rhino` to `compas_rhino.conversions`.
* Added `polyhedron_to_rhino` to `compas_rhino.conversions`.
* Added `from_mesh` plugin to `compas_rhino.geometry.RhinoBrep`.
* Added `compas.geometry.Plane.worldYZ` and `compas.geometry.Plane.worldZX`.
* Added `compas.datastructures.CellNetwork`.
* Added `compas_rhino.conversions.brep_to_compas_box`.
* Added `compas_rhino.conversions.brep_to_compas_cone`.
* Added `compas_rhino.conversions.brep_to_compas_cylinder`.
* Added `compas_rhino.conversions.brep_to_compas_sphere`.
* Added `compas_rhino.conversions.brep_to_rhino`.
* Added `compas_rhino.conversions.capsule_to_rhino_brep`.
* Added `compas_rhino.conversions.cone_to_rhino_brep`.
* Added `compas_rhino.conversions.curve_to_rhino`.
* Added `compas_rhino.conversions.cylinder_to_rhino_brep`.
* Added `compas_rhino.conversions.extrusion_to_compas_box`.
* Added `compas_rhino.conversions.extrusion_to_rhino_cylinder`.
* Added `compas_rhino.conversions.extrusion_to_rhino_torus`.
* Added `compas_rhino.conversions.polyline_to_rhino_curve`.
* Added `compas_rhino.conversions.surface_to_compas`.
* Added `compas_rhino.conversions.surface_to_compas_mesh`.
* Added `compas_rhino.conversions.surface_to_compas_quadmesh`.
* Added `compas_rhino.conversions.surface_to_rhino`.
* Added `compas_rhino.conversions.torus_to_rhino_brep`.
* Added `compas_rhino.artists._helpers.attributes`.
* Added `compas_rhino.artists._helpers.ngon`.
* Added `compas.geometry.find_span`.
* Added `compas.geometry.construct_knotvector`.
* Added `compas.geometry.knotvector_to_knots_and_mults`.
* Added `compas.geometry.knots_and_mults_to_knotvector`.
* Added `compas.geometry.compute_basisfuncs`.
* Added `compas.geometry.compute_basisfuncsderivs`.
* Added `compas.geometry.DefaultNurbsCurve` as try-last, Python-only plugin for `compas.geometry.NurbsCurve`.
* Added `compas.geometry.DefaultNurbsSurface` as try-last, Python-only plugin for `compas.geometry.NurbsSurface`.
* Added color count to constructor functions of `compas.colors.ColorMap`.

### Changed

* Temporarily skip testing for python 3.7 due to a bug related to MacOS 13.
* Fixed bug that caused a new-line at the end of the `compas.HERE` constant in IronPython for Mac.
* Fixed unbound method usage of `.cross()` on `Plane`, `Vector` and `Frame`.
* Fixed Grasshopper `draw_polylines` method to return `PolylineCurve` instead of `Polyline` because the latter shows as only points.
* Fixed bug in the `is_polygon_in_polygon_xy` that was not correctly generating all the edges of the second polygon before checking for intersections.
* Fixed `area_polygon` that was, in some cases, returning a negative area.
* Fixed uninstall post-process.
* Fixed support for `System.Decimal` data type on json serialization.
* Fixed `offset_polygon` raising a TypeError when inputing a Polygon instead of a list of Points.
* Simplified `compas.datastructures.Part` for more generic usage.
* Changed `GLTFMesh.from_mesh` to read texture coordinates, vertex normals and colors if available and add to `GLTFMesh`
* Fixed bug in `VolMeshArtist.draw_cells` for Rhino, Blender and Grasshopper.
* Changed edge parameter of `compas.datastructures.Halfedge.edge_faces` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.Halfedge.halfedge_face` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.Halfedge.is_edge_on_boundary` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.Halfedge.halfedge_after` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.Halfedge.halfedge_before` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.trimesh_edge_cotangent` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.trimesh_edge_cotangents` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.Mesh.edge_coordinates` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.Mesh.edge_length` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.Mesh.edge_vector` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.Mesh.edge_point` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.Mesh.edge_midpoint` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.Mesh.edge_direction` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.is_collapse_legal` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.mesh_collapse_edge` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.trimesh_collapse_edge` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.mesh_insert_vertex_on_edge` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.mesh_split_edge` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.trimesh_split_edge` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed edge parameter of `compas.datastructures.trimesh_swap_edge` to 1 edge identifier (tuple of vertices) instead of two serparate vertex identifiers.
* Changed `compas.datastructures.Mesh.vertex_laplacian` to return `compas.geometry.Vector`.
* Changed `compas.datastructures.Mesh.neighborhood_centroid` to return `compas.geometry.Point`.
* Changed `compas.datastructures.Mesh.vertex_normal` to return `compas.geometry.Vector`.
* Changed `compas.datastructures.Mesh.edge_vector` to return `compas.geometry.Vector`.
* Changed `compas.datastructures.Mesh.edge_direction` to return `compas.geometry.Vector`.
* Changed `compas.datastructures.Mesh.edge_point` to return `compas.geometry.Point`.
* Changed `compas.datastructures.Mesh.edge_midpoint` to return `compas.geometry.Point`.
* Changed `compas.datastructures.Mesh.face_normal` to return `compas.geometry.Vector`.
* Changed `compas.datastructures.Mesh.face_centroid` to return `compas.geometry.Point`.
* Changed `compas.datastructures.Mesh.face_center` to return `compas.geometry.Point`.
* Changed `compas.datastructures.Mesh.face_plane` to return `compas.geometry.Plane`.
* Changed JSON validation to Draft202012.
* Changed `compas.data.Data.to_json` to include `compact=False` parameter.
* Changed `compas.data.Data.to_jsonstring` to include `compact=False` parameter.
* Changed `compas.data.json_dump` to include `compact=False` parameter.
* Changed `compas.data.json_dumps` to include `compact=False` parameter.
* Changed `compas.data.DataEncoder` and `compas.data.DataDecoder` to support `to_jsondata` and `from_jsondata`.
* Moved all API level docstrings from the `__init__.py` to the correspoding `.rst` file in the docs.
* Fixed `AttributeError` in Plotter's `PolylineArtist` and `SegementArtist`.
* Fixed wrong key type when de-serializing `Graph` with integer keys leading to node not found.
* Changed base class for `compas.geometry.Transformation` to `compas.data.Data`.
* Moved all core transformation functions to `compas.geometry._core`.
* Changed base class of `compas.geometry.Arc` to `compas.geometry.Curve.`
* Changed base class of `compas.geometry.Bezier` to `compas.geometry.Curve.`
* Changed base class of `compas.geometry.Circle` to `compas.geometry.Curve.`
* Changed base class of `compas.geometry.Ellipse` to `compas.geometry.Curve.`
* Changed base class of `compas.geometry.Line` to `compas.geometry.Curve.`
* Changed base class of `compas.geometry.Polyline` to `compas.geometry.Curve.`
* Changed `compas.geometry.oriented_bounding_box_numpy` to minimize volume.
* Fixed data interface `compas.datastructures.Assembly` and `compas.datastructures.Part`.
* Changed data property of `compas.datastructures.Graph` to contain only JSON compatible data.
* Changed data property of `compas.datastructures.Halfedge` to contain only JSON compatible data.
* Changed data property of `compas.datastructures.Halfface` to contain only JSON compatible data.
* Changed `__repr__` of `compas.geometry.Point` and `compas.geometry.Vector` to not use limited precision (`compas.PRECISION`) to ensure proper object reconstruction through `eval(repr(point))`.
* Changed `compas.datastructures.Graph.delete_edge` to delete invalid (u, u) edges and not delete edges in opposite directions (v, u)
* Fixed bug in `compas.datastructures.Mesh.insert_vertex`.
* Fixed bug in `compas.geometry.angle_vectors_signed`.
* Fixed bug in `compas.geometry.Polyline.split_at_corners` where angles were sometimes wrongly calculated.
* Changed `compas.artists.MeshArtist` default colors.
* Fixed bug in `compas.geometry.curves.Polyline` shorten and extend methods.
* Changed internal _plane storage of the `compas.datastructures.Halfface` from `_plane[u][v][w]` to `_plane[u][v][fkey]`
* Fixed `SyntaxError` when importing COMPAS in GHPython.

### Removed

* Removed all `__all__` beyond second level package.
* Removed deprecated `compas.utilities.coercing`.
* Removed deprecated `compas.utilities.encoders`.
* Removed deprecated `compas.utilities.xfunc`.
* Removed `compas.datastructures.Halfedge.get_any_vertex`.
* Removed `compas.datastructures.Halfedge.get_any_vertices`.
* Removed `compas.datastructures.Halfedge.get_any_face`.
* Removed "schemas" folder and all contained `.json` files from `compas.data`.
* Removed `compas.data.Data.jsondefinititions`.
* Removed `compas.data.Data.jsonvalidator`.
* Removed `compas.data.Data.validate_json`.
* Removed `compas.data.Data.validate_jsondata`.
* Removed `compas.data.Data.validate_jsonstring`.
* Removed `compas.data.Data.__getstate__`.
* Removed `compas.data.Data.__setstate__`.
* Removed setter of property `compas.data.Data.data` and similar setters in all data classes.
* Removed properties `compas.data.Data.DATASCHEMA` and `compas.data.Data.JSONSCHEMANAME`.
* Removed properties `compas.datastructures.Graph.DATASCHEMA` and `compas.datastructures.Graph.JSONSCHEMANAME`.
* Removed properties `compas.datastructures.Halfedge.DATASCHEMA` and `compas.datastructures.Halfedge.JSONSCHEMANAME`.
* Removed properties `compas.datastructures.Halfface.DATASCHEMA` and `compas.datastructures.Halfface.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Arc.DATASCHEMA` and `compas.geometry.Arc.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Bezier.DATASCHEMA` and `compas.geometry.Bezier.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Box.DATASCHEMA` and `compas.geometry.Box.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Capsule.DATASCHEMA` and `compas.geometry.Capsule.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Circle.DATASCHEMA` and `compas.geometry.Circle.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Cone.DATASCHEMA` and `compas.geometry.Cone.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Cylinder.DATASCHEMA` and `compas.geometry.Cylinder.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Ellipse.DATASCHEMA` and `compas.geometry.Ellipse.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Frame.DATASCHEMA` and `compas.geometry.Frame.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Line.DATASCHEMA` and `compas.geometry.Line.JSONSCHEMANAME`.
* Removed properties `compas.geometry.NurbsCurve.DATASCHEMA` and `compas.geometry.NurbsCurve.JSONSCHEMANAME`.
* Removed properties `compas.geometry.NurbsSurface.DATASCHEMA` and `compas.geometry.NurbsSurface.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Plane.DATASCHEMA` and `compas.geometry.Plane.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Point.DATASCHEMA` and `compas.geometry.Point.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Pointcloud.DATASCHEMA` and `compas.geometry.Pointcloud.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Polygon.DATASCHEMA` and `compas.geometry.Polygon.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Polyhedron.DATASCHEMA` and `compas.geometry.Polyhedron.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Polyline.DATASCHEMA` and `compas.geometry.Polyline.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Sphere.DATASCHEMA` and `compas.geometry.Sphere.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Torus.DATASCHEMA` and `compas.geometry.Torus.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Quaternion.DATASCHEMA` and `compas.geometry.Quaternion.JSONSCHEMANAME`.
* Removed properties `compas.geometry.Vector.DATASCHEMA` and `compas.geometry.Vector.JSONSCHEMANAME`.
* Removed `compas.datastructures.Graph.key_index`and `compas.datastructures.Graph.index_key`.
* Removed `compas.datastructures.Graph.uv_index`and `compas.datastructures.Graph.index_uv`.
* Removed `compas.datastructures.Halfedge.key_index` and `compas.datastructures.Halfedge.index_key`.
* Removed `compas.numerical.dr` and `compas.numerical.dr_numpy` (moved to separate `compas_dr`).
* Removed `compas.numerical.fd_numpy` to (moved to separate `compas_fd`).
* Removed `compas.numerical.topop_numpy` (moved to separate `compas_topopt`).
* Removed `compas.numerical.mma` and `compas.numerical.lma`.
* Removed `compas.numerical.descent`, `compas.numerical.devo`, and `compas.numerical.ga`.
* Removed `compas.numerical.utilities`.
* Removed class attribute `CONTEXT` from `compas.artists.Artist`.
* Removed class attribute `AVAILABLE_CONTEXTS` form `compas.artists.Artist`.
* Removed `compas.geometry.Primitive`.
* Removed classmethod `compas.color.Color.from_data`.
* Removed `validate_data` from `compas.data.validators`.
* Removed `json_validate` from `compas.data.json`.
* Removed `compas_rhino.conversions.Box`.
* Removed `compas_rhino.conversions.Circle`.
* Removed `compas_rhino.conversions.Cone`.
* Removed `compas_rhino.conversions.Curve`.
* Removed `compas_rhino.conversions.Cylinder`.
* Removed `compas_rhino.conversions.Ellipse`.
* Removed `compas_rhino.conversions.Line`.
* Removed `compas_rhino.conversions.Mesh`.
* Removed `compas_rhino.conversions.Plane`.
* Removed `compas_rhino.conversions.Point`.
* Removed `compas_rhino.conversions.Polyline`.
* Removed `compas_rhino.conversions.Vector`.
* Removed `compas_rhino.artists.NetworkArtist.draw_nodelabels`.
* Removed `compas_rhino.artists.NetworkArtist.draw_edgelabels`.
* Removed `compas_rhino.artists.MeshArtist.draw_vertexlabels`.
* Removed `compas_rhino.artists.MeshArtist.draw_edgelabels`.
* Removed `compas_rhino.artists.MeshArtist.draw_facelabels`.
* Removed `compas_rhino.artists.VolMeshArtist.draw_vertexlabels`.
* Removed `compas_rhino.artists.VolMeshArtist.draw_edgelabels`.
* Removed `compas_rhino.artists.VolMeshArtist.draw_facelabels`.
* Removed `compas_rhino.artists.VolMeshArtist.draw_celllabels`.
* Removed `compas.robots`, replaced with `compas_robots` package.
* Removed `compas.artists.robotmodelartist`.
* Removed `compas_blender.artists.robotmodelartist`.
* Removed `compas_ghpython.artists.robotmodelartist`.
* Removed `compas_rhino.artists.robotmodelartist`.

## [1.17.5] 2023-02-16

### Added

* Added conversion function `frame_to_rhino_plane` to `compas_rhino.conversions`.
* Added `RhinoSurface.from_frame` to `compas_rhino.geometry`.
* Added representation for trims with `compas.geometry.BrepTrim`.
* Added `Arc` to `compas.geometry`.
* Added `Arc` conversion functions to `compas_rhino.conversions`.
* Added `from_sphere` alternative constructor to `RhinoBrep`.
* Added support for singular trims to `RhinoBrep`.

### Changed

* Patched [CVE-2007-4559](https://github.com/advisories/GHSA-gw9q-c7gh-j9vm) vulnerability.
* Updated workflows to v2.
* Fixed attribute error in `compas_rhino.conversions.ellipse_to_compas`.
* Changed deepcopy of `RhinoBrep` to use the native `Rhino.Geometry` mechanism.
* The normal of the cutting plane is no longer flipped in `compas_rhino.geometry.RhinoBrep`.
* Planar holes caused by `RhinoBrep.trim` are now automatically capped.
* Fixed `Polygon` constructor to not modify the input list of points.
* Fixed serialization of sphere and cylinder Breps in `RhinoBrep`.
* Fixed serialization of some trimmed shapes in `RhinoBrep`.
* Freeze black version to 22.12.0.
* Fixed `is_point_in_circle_xy` second argument to access the origin of the plane of the circle.
* Changed `compas.datastructures.Graph.data` to contain unprocessed `node` and `edge` dicts.
* Changed `compas.datastructures.Halfedge.data` to contain unprocessed `vertex`, `face`, `facedata`, and `edgedata` dicts.
* Changed `compas.datastructures.Halfface.data` to contain unprocessed `vertex`, `cell`, `edge_data`, `face_data`, and `cell_data` dicts.
* Changed `compas.geometry.Arc.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Bezier.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Box.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Capsule.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Circle.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Cone.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Cylinder.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Ellipse.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Frame.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Line.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.NurbsCurve.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.NurbsSurface.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Plane.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Pointcloud.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Polygon.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Polyhedron.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Polyline.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Sphere.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Torus.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.
* Changed `compas.geometry.Quaternion.data` to contain unprocessed COMPAS geometry objects, instead of their data dicts.

### Removed

## [1.17.4] 2022-12-06

### Added

* Added option for per-vertex color specification to `compas_rhino.utilities.drawing.draw_mesh`.

### Changed

* Fixed strange point values in RhinoNurbsCurve caused by conversion `ControlPoint` to COMPAS instead of `ControlPoint.Location`.
* Fixed flipped order of NURBS point count values when creating RhinoNurbsSurface from parameters.
* Changed serialization format and reconstruction procedure of `RhinoBrep`.

### Removed

* Removed Python 3.6 from build workflows as it reached end-of-life at the end of 2021.

## [1.17.3] 2022-11-09

### Added

* Added `compas_rhino.INSTALLATION_ARGUMENTS`.

### Changed

* Fixed bug in Rhino installation due to redefinition of command line arguments in `compas_ghpython.components.get_version_from_args`.

### Removed

## [1.17.2] 2022-11-07

### Added

### Changed

* Changed `compas._os._polyfill_symlinks` to use junction (/J) instead of symbolic link (/D).

### Removed

## [1.17.1] 2022-11-06

### Added

* Added `compas_rhino.geometry.RhinoCurve.offset`.
* Added `compas.geometry.Surface.from_plane`.
* Added `compas.geometry.surfaces.surface.new_surface_from_plane` pluggable.
* Added `compas_rhino.geometry.surfaces.new_surface_from_plane` plugin.
* Added `compas_rhino.geometry.RhinoSurface.intersections_with_curve`.

### Changed

* Fixed bug in `compas_rhino.geometry.RhinoCurve.frame_at`.
* Changed implementation of `compas.datastructures.mesh_planarize_faces` to include edge midpoints.

### Removed

## [1.17.0] 2022-10-07

### Added

* Added gltf extensions: `KHR_materials_transmission`, `KHR_materials_specular`, `KHR_materials_ior`, `KHR_materials_clearcoat`, `KHR_Texture_Transform`, `KHR_materials_pbrSpecularGlossiness`
* Added `GLTFContent.check_extensions_texture_recursively`
* Added `GLTFContent.get_node_by_name`, `GLTFContent.get_material_index_by_name`
* Added `GLTFContent.add_material`, `GLTFContent.add_texture`, `GLTFContent.add_image`
* Added pluggable `Brep` support with `compas.geometry.brep`.
* Added Rhino `Brep` plugin in `compas_rhino.geometry.brep`.
* Added boolean operations to the `compas_rhino` `Brep` backend.
* Added boolean operation operator overloads in `compas.geometry.Brep`
* Added `format` task using `black` formatter.
* Added a `test_intersection_circle_circle_xy` in the `test_intersections`
* Added split operation to `compas_rhino.geometry.Brep`.
* Added a `RhinoArtist` in `compas_rhino`.
* Added a `RhinoArtist` in `compas_ghpython`.

### Changed

* Based all gltf data classes on `BaseGLTFDataClass`
* Fixed `Color.__get___` AttributeError.
* Fixed  `RhinoSurface.curvature_at` not returning a Vector, but a Rhino SurfaceCurvature class object
* Fixed `cylinder_to_rhino` conversion to match `compas.geometry.Cylinder` location.
* Changed identification of cylinder brep face to non-zero in `compas_rhino.conversions.cylinder.Cylinder`.
* Changed linter to `black`.
* Automatically trigger `invoke format` during `invoke release`.
* Fixed bug in `intersections.intersection_circle_circle_xy` where the Circle's Plane was accessed instead of the centre.
* Fixed bug in `_core.tangent` where the Circle's Plane was accessed instead of the centre.
* Fixed the `test_tangent` to work with a properly defined circle
* `RhinoBrep` serialization works now with surface types other than NURBS.
* Fixed bug in finding halfedge before a given halfedge if that halfedge is on the boundary (`Mesh.halfedge_before`).
* Renamed `Brep.from_brep` to `Brep.from_native`.

### Removed

## [1.16.0] 2022-06-20

### Added

* Added `Polyline.extend`, `Polyline.extended`, `Polyline.shorten`,  `Polyline.shortened`.
* Added `Data.sha256` for computing a hash value of data objects, for example for comparisons during version control.
* Added optional `path` parameter to `compas.rpc.Proxy` to allow for non-package calls.
* Added Grasshopper component to call RPC functions.
* Added alternative installation procedure for Blender on Windows.
* Added `Mesh.to_lines` method and tests.
* Added `Data.guid` to JSON serialization.
* Added `Data.guid` to pickle state.
* Added `Assembly.find_by_key` to locate parts by key.
* Added `clear_edges` and `clear_nodes` to `NetworkArtist` for ghpython.
* Added `ToString` method to `Data` to ensure that Rhino/Grasshopper correctly casts objects to string.

### Changed

* Set `jinja >= 3.0` to dev dependencies to fix docs build error.
* Fixed removing of collections for `compas_plotters`.
* Fixed bug in `compas_plotters.plotter.Plotter.add_from_list`.
* Fixed bug in `compas.robots.Configuration`.
* Rebuild part index after deserialization in `Assembly`.
* Fixed bug in `compas.artists.colordict.ColorDict`.
* Change `Mesh.mesh_dual` with option of including the boundary.
* Fixed type error in `compas_rhino.conversions.box_to_rhino`.
* Moved from `autopep8` to `black`
* Fixed bug in `compas.utilities.linspace` for number series with high precision start and stop values.
* Fixed uncentered viewbox in `Plotter.zoom_extents()`
* Changed `RobotModelArtists.atteched_tool_models` to dictionary to support multiple tools.
* Locked `sphinx` to 4.5.
* Changed `GLTFExporter` such that generated gltfs can be viewed with webxr
* Fixed source directory path in `compas_ghpython.uninstall` plugin.
* Fixed bug in `compas_ghpython.components`that ignored input list of `.ghuser` objects to uninstall.
* Fixed conversion bug of transformed `Box` in `compas_rhino.conversions`

### Removed

* Removed unused `compas_rhino.objects` (moved to `compas_ui`).
* Removed unused `compas_rhino.ui` (moved to `compas_ui`).

## [1.15.1] 2022-03-28

### Added

* Added optional `triangulated` flag to `Mesh.to_vertices_and_faces`.
* Added geometry information of active meshes to the serialization/deserialization of robot model's `MeshDescriptor`.
* Added Grasshopper component to draw any COMPAS object.
* Added new icons to Grasshopper components and default to icon style.

### Changed

* Fixed bug in `normal_polygon` in `compas.geometry`.
* Fixed bug in Blender mesh conversion.
* Changed Rhino plugin installer to check for and install required plugin packages.
* Refactor robot model artists to use the same `Mesh.to_vertices_and_faces` everywhere.
* Fix debug print on Blender artist.

### Removed

## [1.15.0] 2022-03-22

### Added

* Added descriptor support to `compas.colors.Color`.
* Added descriptor protocol metaclass to `compas.artists.Artist`.
* Added `compas.artists.colordict.ColorDict` descriptor.
* Added `allclose` to doctest fixtures.
* Added `compas.colors.Color.coerce` to construct a color out og hex, RGB1, and RGB255 inputs.
* Added `compas.datastructures.Network.from_pointcloud`.
* Added `compas.datastructures.VolMesh.from_meshgrid`.
* Added `vertices_where`, `vertices_where_predicate`, `edges_where`, `edges_where_predicate` to `compas.datastructures.HalfFace`.
* Added `faces_where`, `faces_where_predicate`, `cells_where`, `cells_where_predicate` to `compas.datastructures.HalfFace`.
* Added `VolMeshArtist` to registered Blender artists.
* Added `3.1` to supported versions for Blender installer.
* Added `compas.artist.NoArtistContextError`.

### Changed

* Changed `compas.geometry.surfaces.nurbs.from_fill` to accept up to 4 curves as input.
* Changed `compas_rhino.artists.MeshArtist.draw` to draw the mesh only.
* Changed `compas_blender.artists.MeshArtist.draw` to draw the mesh only.
* Changed `compas_ghpython.artists.MeshArtist.draw` to draw the mesh only.
* Changed `compas_rhino.artists.MeshArtist.draw_vertexlabels` to use the colors of the vertex color dict.
* Changed `compas_rhino.artists.MeshArtist.draw_edgelabels` to use the colors of the edge color dict.
* Changed `compas_rhino.artists.MeshArtist.draw_facelabels` to use the colors of the face color dict.
* Changed `compas_blender.artists.MeshArtist.draw_vertexlabels` to use the colors of the vertex color dict.
* Changed `compas_blender.artists.MeshArtist.draw_edgelabels` to use the colors of the edge color dict.
* Changed `compas_blender.artists.MeshArtist.draw_facelabels` to use the colors of the face color dict.
* Changed `compas_ghpython.artists.MeshArtist.draw_vertexlabels` to use the colors of the vertex color dict.
* Changed `compas_ghpython.artists.MeshArtist.draw_edgelabels` to use the colors of the edge color dict.
* Changed `compas_ghpython.artists.MeshArtist.draw_facelabels` to use the colors of the face color dict.
* Fixed `compas_blender.uninstall`.
* Changed `planarity` to optional requirement on all platforms.
* Changed `numba` to optional requirement on all platforms.
* Changed raw github content path for `compas.get`.
* Changed `compas.datastructures.Graph.nodes_where` to accept conditions as kwargs.
* Changed `compas.datastructures.Graph.edges_where` to accept conditions as kwargs.
* Changed `compas.datastructures.Halfedge.vertices_where` to accept conditions as kwargs.
* Changed `compas.datastructures.Halfedge.edges_where` to accept conditions as kwargs.
* Changed `compas.datastructures.Halfedge.faces_where` to accept conditions as kwargs.
* Changed `compas.datastructures.Halfface.vertices_where` to accept conditions as kwargs.
* Changed `compas.datastructures.Halfface.edges_where` to accept conditions as kwargs.
* Changed `compas.datastructures.Halfface.faces_where` to accept conditions as kwargs.
* Changed `compas.datastructures.Halfface.cells_where` to accept conditions as kwargs.
* Fixed `compas_blender.artists.VolMeshArtist.draw` and `compas_blender.artists.VolMeshArtist.draw_cells`.
* Fixed `compas_ghpython.artists.VolMeshArtist.draw` and `compas_ghpython.artists.VolMeshArtist.draw_cells`.
* Fixed `compas_rhino.artists.VolMeshArtist.draw` and `compas_rhino.artists.VolMeshArtist.draw_cells`.
* Improved error messages when artist instance cannot be created.
* Fixed exception when calculating geometry of `compas.datastructures.Part` without features.
* Fixed bug in `compas_rhino.conversions.RhinoCurve.to_compas`.
* Fixed bug in `compas_rhino.conversions.RhinoSurface.to_compas`.

### Removed

* Removed `compas.numerical.drx`.

## [1.14.1] 2022-02-16

### Added

* Added doc test step in CI/CD.

### Changed

* Fixed symlink expansion for directories relative to the COMPAS installation folder, eg. `compas.DATA` when used from IronPython.
* Fixed the result of `compas.__version__` on dev installs to properly include git hash.
* Move `data` files inside the folder included in the source distribution (ie. non-dev installs).
* Fixed IronPython detection on ipy 2.7.12 and higher.

### Removed

## [1.14.0] 2022-02-06

### Added

* Added `compas.colors.Color`.
* Added `compas.colors.ColorMap`.
* Added `compas_blender.conversions.BlenderGeometry`.
* Added `compas_blender.conversions.BlenderCurve`.
* Added `compas_blender.conversions.BlenderMesh`.
* Added option to return strip faces from `compas.datastructure.Halfedge.edge_strip`.
* Added `compas.geometry.Bezier.transform`.
* Added `compas.geometry.Curve` as base class for curves.
* Added `compas.geometry.Surface` as base class for surfaces.
* Added `compas_rhino.geometry.RhinoCurve` as Rhino plugin for basic curves.
* Added `compas_rhino.geometry.RhinoSurface` as Rhino plugin for basic surfaces.
* Added pluggable `compas.geometry.curves.curve.new_curve`.
* Added pluggable `compas.geometry.surfaces.surface.new_surface`.
* Added `compas.artists.CurveArtist`.
* Added `compas.artists.SurfaceArtist`.
* Added `compas_rhino.artists.CurveArtist`.
* Added `compas_rhino.artists.SurfaceArtist`.
* Added `compas_ghpython.artists.CurveArtist`.
* Added `compas_ghpython.artists.SurfaceArtist`.
* Added `compas_blender.artists.CurveArtist`.
* Added `compas_blender.artists.SurfaceArtist`.
* Added `compas_rhino.utilities.draw_curves`.
* Added `compas_rhino.utilities.draw_surfaces`.
* Added `compas_blender.utilities.draw_curves`.
* Added `compas_blender.utilities.draw_surfaces`.
* Added `rgba` and `rgba255` properties to `compas.colors.Color`.
* Added `from_name` method to `compas.colors.Color`.
* Added Python 3.10 support.
* Added `RobotModel.ur5` for the sake of example.

### Changed

* Fixed bug in `mesh_slice_plane()` , `Mesh.slice_plane()`.
* Changed `compas_rhino.geometry.RhinoNurbsSurface.closest_point` to fix bug of rhino_curve to rhino_surface, plus return tuple instead.
* Changed `compas_plotters.plotter.Plotter` to normal class instead of singleton.
* Moved functionality of `compas.utilities.coercion` to `compas.data`.
* Fixed bug in `compas.geometry.NurbsSurface.to_triangles()`.
* Renamed docs site folders `latest` to `stable` and `dev` to `latest`.
* Rebased `compas.geometry.NurbsCurve` on `compas.geometry.Curve`.
* Rebased `compas.geometry.NurbsSurface` on `compas.geometry.Surface`.
* Rebased `compas_rhino.geometry.RhinoNurbsCurve` on `compas.geometry.NurbsCurve` and `compas_rhino.geometry.RhinoCurve`.
* Rebased `compas_rhino.geometry.RhinoNurbsSurface` on `compas.geometry.NurbsSurface` and `compas_rhino.geometry.RhinoSurface`.
* Fixed error message for unsupported joint types.
* Fixed support for non-standard URDF attributes on limit and mesh geometry.
* Fixed data serialization for URDF materials without color.
* Removed geometric primitives (`Origin`, `Box`, `Sphere`, `Cylinder` and `Capsule`) from `compas.robots` and replaced them with the core ones from `compas.geometry`. The old names are still available but deprecated.
* Deprecated the `load_mesh` method of `compas.robots.AbstractMeshLoader` and its sub-classes in favor of `load_meshes`.
* Fixed bug in `compas_rhino.conversions.RhinoGeometry.transform`.

### Removed

* Removed `compas.geometry.Collection`.
* Removed `compas.geometry.CollectionNumpy`.
* Removed `compas.geometry.PointCollection`.
* Removed `compas.geometry.PointCollectionNumpy`.
* Removed `compas.interop`.
* Removed `numba`; `compas.numerical.drx` will be moved to a dedicated extension package.
* Removed `ezdxf` (unused).
* Removed `laspy` (unused).
* Removed `compas_rhino.artists.MeshArtist.draw_mesh`.
* Removed `compas_blender.artists.MeshArtist.draw_mesh`.

## [1.13.3] 2021-12-17

### Added

* Added `compas_plotters.artists.NetworkArtist.draw_nodelabels`.
* Added `compas_plotters.artists.NetworkArtist.draw_edgelabels`.
* Added `compas_plotters.Plotter.fontsize`.
* Added `INSTALLED_VERSION` variable to `compas_rhino.install` to interally inform rhino version context post-installation steps.
* Added `compas_rhino.geometry.RhinoNurbsSurface`.
* Added `compas_rhino.geometry.surfaces.new_nurbssurface` plugin.
* Added `compas_rhino.geometry.surfaces.new_nurbssurface_from_parameters` plugin.
* Added `compas_rhino.geometry.surfaces.new_nurbssurface_from_points` plugin.
* Added `compas_rhino.geometry.surfaces.new_nurbssurface_from_fill` plugin.
* Added `compas_rhino.geometry.surfaces.new_nurbssurface_from_step` plugin.
* Added `compas_rhino.conversions.RhinoSurface.to_compas`.

### Changed

* Fixed bug in inheritance of `compas_plotters.artists.NetworkArtist`.
* Changed `compas_plotters.artists.MeshArtist.draw_edges` to ignore edge direction for assignment of edge colors and widths.
* Changed `compas_plotters.artists.MeshArtist.draw_vertexlabels` to use `compas_plotters.Plotter.fontsize`.
* Changed `compas_plotters.artists.MeshArtist.draw_edgelabels` to use `compas_plotters.Plotter.fontsize`.
* Changed `compas_plotters.artists.MeshArtist.draw_facelabels` to use `compas_plotters.Plotter.fontsize`.
* Fixed bug in `compas_rhino.conversions.plane_to_compas_frame`.
* Changed implementation of `compas.geometry.NurbsSurface.xyz`.
* Fixed bug in `compas.geometry.NurbsSurface.to_mesh`.
* Changed `compas_rhino.geometry.RhinoNurbsSurface.from_points` to use transposed points.
* Fixed bug in `compas_rhino.conversions.RhinoSurface.to_compas_mesh`.

### Removed

## [1.13.2] 2021-12-11

### Added

* Added `compas_ghpython.fetch_ghio_lib` to simplify the loading of Grasshopper's IO library for extension developers.

### Changed

### Removed

## [1.13.1] 2021-12-11

### Added

### Changed

* Fixed bug in `Grasshopper` plugin path on Windows.
* Fixed bug in `Grasshopper` `UserObjects` uninstall.

### Removed

## [1.13.0] 2021-12-10

### Added

* Added `compas_rhino.DEFAULT_VERSION`.
* Added `clean` option to `compas_rhino.install` to remove existing symlinks if they cannot be imported from the current environment.
* Added basic implementation of `compas.datastructures.Assembly`.
* Added `compas.is_grasshopper`.
* Added `compas.GH`.
* Added `compas.artists.Artist.CONTEXT`.
* Added `compas.artists.Artist.AVAILABLE_CONTEXTS`.
* Added `compas.artists.artist.register_artists` pluggable.

### Changed

* Updated `pr-checks` workflow for checking Changelog entry.
* Fixed return value of attributes of empty `compas_rhino.geometry.RhinoNurbsCurve`.
* Fixed error in parameter list of `compas_rhino.geometry.curves.new_nurbscurve`.
* Fixed error in parameter list of `compas_rhino.geometry.curves.new_nurbscurve_from_interpolation`.
* Fixed error in parameter list of `compas_rhino.geometry.curves.new_nurbscurve_from_step`.
* Changed `compas_rhino.install` to remove broken symlinks.
* Changed `compas_rhino.install` to reinstall broken symlinks if they can be imported from the current environment.
* Changed `compas_rhino.uninstall` to remove broken symlinks.
* Changed `compas_rhino.install_plugin` to remove broken symlinks.
* Changed default Rhino version for installation to `7.0`.
* Fixed bug in `compas_ghpython` related to importing `Grasshopper` prematurely.
* Changed `compas.artists.Artist.ITEM_ARTIST` to context-based dict.
* Changed `compas_rhino.__init__.py` functions.
* Changed `compas_ghpython.__init__.py` functions.
* Renamed `compas_ghpython.get_grasshopper_plugin_path` to `compas_ghpython.get_grasshopper_managedplugin_path`.

### Removed

* Removed `compas.artists.artist.new_artist` pluggable.

## [1.12.2] 2021-11-30

### Added

### Changed

* Moved import of `subprocess` to top of file `compas._os.py`.

### Removed

## [1.12.1] 2021-11-29

### Added

### Changed

* Fixed bug in `compas_rhino.conversions.RhinoPoint.from_geometry`.
* Changed `compas_rhino.install` to remove broken symlinks.
* Changed `compas_rhino.install` to reinstall broken symlinks if they can be imported from the current environment.
* Changed `compas_rhino.uninstall` to remove broken symlinks.
* Changed `compas_rhino.install_plugin` to remove broken symlinks.

### Removed

## [1.12.0] 2021-11-17

### Added

* Added `CircleArtist`, `LineArtist`, `PointArtist`, `PolygonArtist`, `PolylineArtist`, and `VectorArtist` to `compas_blender`.
* Added `draw_circles` and `draw_planes` to `compas_blender`.
* Added `compas_rhino.geometry.curves` plugins for `compas.geometry.curves` pluggables.
* Added `compas_rhino.geometry.RhinoNurbsCurve`.
* Added `to_compas_quadmesh` to `compas_rhino.conversions.RhinoSurface`.

### Changed

* Replaced implementation of `RGBColour` and `Float` with deprecation warning in `compas.utilities.descriptors`.
* Moved all Rhino geometry and objects wrappers to `compas_rhino.conversions`.
* Fixed bug in `compas_rhino.conversions.RhinoSurface.from_geometry`.
* Changed `compas_rhino.conversions.RhinoLine.from_geometry` to accept line curves.
* Fixed bug in `compas_rhino.geometry.RhinoNurbsCurve.closest_point`.
* Modify `to_compas_mesh` in `compas_rhino.conversions.RhinoSurface` to use brep loops.

### Removed

## [1.11.1] 2021-11-09

### Added

### Changed

* Changed `compas_rhino.uninstall` to also remove broken symlinks if no specific packages are provided for un-installation.
* Changed `compas_rhino.install` to also remove broken symlinks.

### Removed

## [1.11.0] 2021-11-08

### Added

* Added halfedge loops in `compas.datastructures.Halfedge.halfedge_loop`.
* Added halfedge strips in `compas.datastructures.Halfedge.halfedge_strip`.
* Added `compas.datastructures.mesh_split_strip` and `compas.datastructures.Mesh.split_strip`.
* Added boundingbox to `compas_rhino.conduits.BaseConduit`

### Changed

* Fixed bug in combination of `compas_rhino.artists.MeshArtist.draw_mesh` and `compas_rhino.utilities.drawing.draw_mesh`.
* Fixed bug in continuous loops in `compas.datastructures.Halfedge.edge_loop`.
* Fixed bug in continuous strips in `compas.datastructures.Halfedge.edge_strip`.
* Changed abstract method `compas.artists.MeshArtist.draw_mesh` to implemented method in `compas_plotters.artists.MeshArtist.draw_mesh`.

### Removed

## [1.10.0] 2021-11-04

### Added

* Added `compas.geometry.Curve` and `compas.geometry.NurbsCurve`.
* Added `compas.geometry.Surface` and `compas.geometry.NurbsSurface`.
* Added pluggables for `compas.geometry.NurbsCurve.__new__`, `compas.geometry.NurbsCurve.from_parameters`, `compas.geometry.NurbsCurve.from_points`, `compas.geometry.NurbsCurve.from_interpolation`, `compas.geometry.NurbsCurve.from_step`.
* Added pluggables for `compas.geometry.NurbsSurface.__new__`, `compas.geometry.NurbsSurface.from_parameters`, `compas.geometry.NurbsSurface.from_points`, `compas.geometry.NurbsSurface.from_fill`, `compas.geometry.NurbsSurface.from_step`.
* Added missing implementations for abstract clear methods of `compas_rhino.artists.volmeshartist`.
* Added `compas_rhino.geometry.RhinoBox`, `compas_rhino.geometry.RhinoCircle`, `compas_rhino.geometry.RhinoCone`, `compas_rhino.geometry.RhinoCurve`, `compas_rhino.geometry.RhinoCylinder`, `compas_rhino.geometry.RhinoEllipse`, `compas_rhino.geometry.RhinoLine`, `compas_rhino.geometry.RhinoMesh`, `compas_rhino.geometry.RhinoPlane`, `compas_rhino.geometry.RhinoPoint`, `compas_rhino.geometry.RhinoPolyline`, `compas_rhino.geometry.RhinoSphere`, `compas_rhino.geometry.RhinoSurface`, `compas_rhino.geometry.RhinoVector` as wrappers for working with Rhino geometry through geometry conversions or coercion of doc objects.
* Added `compas_rhino.conversions` from COMPAS geometry to Rhino geometry and vice versa, for primitives, shapes, curves, surfaces, meshes.
* Added `compas_rhino.coercion` from Rhino doc objects to Rhino geometry compatible with COMPAS geometry.

### Changed

* Fixed bug in directions of `compas.datastructures.Mesh.from_meshgrid`.
* Fixed bug in Rhino mesh face drawing.
* Fixed bug related to legacy uninstall on Rhino for Mac.

### Removed

## [1.9.3] 2021-11-02

### Added

### Changed

* Changed default path for Rhino 7 legacy install cleanup to Rhino7.app in `compas_rhino.__init__.py`.
* Changed z-coordinate of `compas.datastructures.Mesh.from_meshgrid` to `0.0` instead of `0`.

### Removed

## [1.9.2] 2021-11-02

### Added

* Added `draw_mesh` method to `compas_ghpython.artists.MeshArtist` to match all other mesh artists.

### Changed

* Changed new artist registration to check if subclass.
* Fixed `RobotModelArtist` for blender: missing abstract method impl and handle init order.

### Removed

## [1.9.1] 2021-10-22

### Added

* Added `Plane.offset`.
* Added `is_mesh_closed` property to `compas.datastructures.mesh_slice_plane`.

### Changed

* Fixed backward compatibility problem with artists by adding back `Artist.build` and `Artist.build_as`.
* Fixed backward compatibility problem with artists by adding `compas_rhino.artists.BaseArtist` alias for `compas_rhino.artists.RhinoArtist`.

### Removed

## [1.9.0] 2021-10-21

### Added

* Added `draw_vertexlabels`, `draw_edgelabels`, `draw_facelabels`, `draw_vertexnormals`, and `draw_facenormals` to `compas_blender.artists.MeshArtist`.
* Added optional `triangulated` flag to `to_vertices_and_faces` of all shapes.
* Added `compas.geometry.Geometry` base class.
* Added `__add__`, `__sub__`, `__and__` to `compas.geometry.Shape` for boolean operations using binary operators.
* Added `is_closed` to `compas.geometry.Polyhedron`.
* Added `Plane.offset`.
* Added `compas.artists.Artist`.
* Added pluggable `compas.artists.new_artist`.
* Added plugin `compas_rhino.artists.new_artist_rhino`.
* Added plugin `compas_blender.artists.new_artist_blender`.
* Added `compas.artist.DataArtistNotRegistered`.
* Added `draw_node_labels` and `draw_edgelabels` to `compas_blender.artists.NetworkArtist`.
* Added `compas_blender.artists.RobotModelArtist.clear`.
* Added `compas_blender.geometry.booleans` as plugin for boolean pluggables.
* Added version-based installation for Blender.
* Added several shape artists to `compas_ghpython`: `BoxArtist`, `CapsuleArtist`, `ConeArtist`, `CylinderArtist`, `PolygonArtist`, `PolyhedronArtist`, `SphereArtist`, `TorusArtist` and `VectorArtist`.
* Added support for CLR generic dictionaries to the `compas.data` decoders.
* Added `Graph.node_sample`, `Graph.edge_sample`.
* Added `Halfedge.vertex_sample`, `Halfedge.edge_sample`, `Halfedge.face_sample`.
* Added `Halfface.vertex_sample`, `Halfface.edge_sample`, `Halfface.face_sample`, `Halfface.cell_sample`.
* Added `Mesh.from_meshgrid`.

### Changed

* Fixed bug in `compas_blender.draw_texts`.
* Changed `compas_rhino.artists.BaseArtist` to `compas_rhino.artists.RhinoArtist`.
* Changed `compas_blender.artists.BaseArtist` to `compas_blender.artists.BlenderArtist`.
* Changed default resolution for shape discretisation to 16 for both u and v where relevant.
* Changed base class of `compas.geometry.Primitive` and `compas.geometry.Shape` to `compas.geometry.Geometry`.
* `compas_blender.artists.RobotModelArtist.collection` can be assigned as a Blender collection or a name.
* Generalized the parameter `color` of `compas_blender.draw_texts` and various label drawing methods.
* Changed `compas.IPY` to `compas.RHINO` in `orientation_rhino`.
* Changed `planarity` to `requires_extra` for pip installations.
* Fixed bug in handling of ngonal meshes in `compas_ghpython` artists / drawing functions.

### Removed

## [1.8.1] 2021-09-08

### Added

### Changed

### Removed

## [1.8.0] 2021-09-08

### Added

* Added pluggable function `trimesh_slice` in `compas_rhino`.
* Added equality comparison for pointclouds.
* Added `compas.data.is_sequence_of_uint`.
* Added general plotter for geometry objects and data structures based on the artist registration mechanism.
* Added support for multimesh files to OBJ reader/writer.
* Added support for attaching and detaching meshes in `compas.robots.RobotModelArtist` and drawing them.
* Added `reshape` in `compas.utilities`.
* Added `compas.geometry.NurbsCurve`.
* Added `compas.geometry.NurbsSurface`.
* Added `compas_rhino.conversions`.
* Added `compas_rhino.geometry.RhinoBox`.
* Added `compas_rhino.geometry.RhinoCone`.
* Added `compas_rhino.geometry.RhinoCylinder`.
* Added `compas_rhino.geometry.RhinoPolyline`.
* Added `compas_rhino.geometry.RhinoSphere`.
* Added basic implementation of `compas.datastructures.Assembly`.
* Added `meshes` method to artists of `compas.robots.RobotModel`.
* Added `FrameArtist` class to `compas_blender`.

### Changed

* `compas.robots.Axis` is now normalized upon initialization.
* Fixed a bug in `compas.numerical.dr_numpy` when using numpy array as inputs.
* Allowed for varying repository file structures in `compas.robots.GithubPackageMeshLoader`.
* Fixed data schema of `compas.geometry.Polyline`, `compas.geometry.Polygon`, `compas.geometry.Pointcloud`.
* Fixed `Configuration.from_data` to be backward-compatible with JSON data generated before `compas 1.3.0`.
* Changed `compas_rhino.drawing.draw_breps` to assume provided polygon is closed and automatically add missing corner to polycurve constructor.
* Changed conversion of edges and faces to uniques keys for the data dicts to use the string representation of a sorted tuple of identifiers.
* Added `dtype` to JSON decoding error message.
* Moved `compas.datastructures.mesh.core.halfedge.HalfEdge` to `compas.datastructures.halfedge.halfedge.HalfEdge`
* Moved `compas.datastructures.network.core.graph.Graph` to `compas.datastructures.graph.graph.Graph`.

### Removed

* Removed `compas.datastructures.mesh.core.mesh.BaseMesh`.
* Removed `compas.datastructures.BaseNetwork`.

## [1.7.1] 2021-06-14

### Added

### Changed

* Fixed bundling of ghuser components.

### Removed

## [1.7.0] 2021-06-14

### Added

### Changed

* `compas.robots.Axis` is now normalized upon initialization.
* Fixed a bug in `compas.numerical.dr_numpy` when using numpy array as inputs.
* Allowed for varying repository file structures in `compas.robots.GithubPackageMeshLoader`.
* Remove default implementation of `__str__` for data objects.

### Fixed

* Fixed `Configuration.from_data` to be backward-compatible with JSON data generated before `compas 1.3.0`.

### Removed

## [1.7.1] 2021-06-14

### Added

### Changed

* Fixed bundling of ghuser components.

### Removed

## [1.7.0] 2021-06-14

### Added

* Added pluggable function `trimesh_gaussian_curvature` in `compas_rhino`.
* Added pluggable function `trimesh_mean_curvature` in `compas_rhino`.
* Added pluggable function `trimesh_principal_curvature` in `compas_rhino`.
* Added `copy` and `deepcopy` functionality to `compas.robots.Configuration`.
* Added `compas.data.is_sequence_of_int` and `compas.data.is_sequence_of_float`.
* Added `compas.data.Data.JSONSCHEMANAME`.
* Added `kwargs` to all child classes of `compas.data.Data`.
* Added grasshopper component for drawing a frame.
* Added `draw_origin` and `draw_axes`.
* Added `compas.PY2`.

### Changed

* Allow str or int as joint type in `compas.robots.Joint` constructor.
* Moved json schemas to `compas.data`.
* Nested json schemas.
* `compas_ghpython.artists.FrameArtist.draw` now draws a Rhino Plane.
* Fixed bugs in `compas.geometry.bestfit_circle_numpy`.
* Changed directory where ghuser components are installed.
* Added ghuser components directory to those removed by the `clean` task.
* Clean up the ghuser directory before building ghuser components.
* Exposed function `draw_breps` in `compas_rhino.utilities`; example added.
* Added `join` flag to function `draw_breps` in `compas_rhino.utilities`
* Fixed bug in `compas.geometry.distance.closest_point_on_segment_xy`.
* Fixed bug in Rhino implementations of `trimesh` curvature functions.

### Removed

## [1.6.3] 2021-05-26

### Added

* Added `compas.topology.astar_lightest_path`.
* Added JSONSCHEMA definitions for primitives and transformations.
* Added schema implementation to primitives and transformations.
* Added JSONSCHEMA implementation to primitives and transformations.
* Added `compas.data.is_int3`, `compas.data.is_float3`, `compas_data.is_float4x4`.

### Changed

* Extended `compas.topology.astar_shortest_path` to work on `compas.datastructures.Mesh` and `compas.datastructures.Network`.
* Fixed `compas.data.Data.to_jsonstring`.
* Changed `compas.data.Data.data.setter` to raise `NotImplementedError`.
* Changed annotations of `compas_blender.artists.BaseArtist`.
* Fixed `__repr__` for primitives, shapes, transformations.

### Removed

* Removed duplicate cases from `compas.data.DataEncoder`.

## [1.6.2] 2021-05-12

### Added

### Changed

### Removed

## [1.6.1] 2021-05-12

### Added

### Changed

### Removed

## [1.6.0] 2021-05-12

### Added

* Added infrastructure for building Grasshopper components for compas packages.
* Added first Grasshopper component: COMPAS Info.
* Added Grasshopper components for JSON serialization.
* Added `compas_rhino.utilities.set_object_attributes`.
* Added `from_jsonstring` and `to_jsonstring`.
* Added Grasshopper component documentation.

### Changed

* Moved json dump and load to data package.
* Changed parameters and return value of `compas_rhino.utilities.get_object_attributes`.
* Removed `doctest` execution code from src.
* Removed `if __name__ == '__main__'` section from src.
* Optimized the conversion of Rhino Meshes to COMPAS meshes.
* Fix issue with GH User symlink created as directory symlink on some cases.

### Removed

## [1.5.0] 2021-04-20

### Added

* Added support for file-like objects, path strings and URLs to most of the methods previously accepting only file paths, eg. `compas.datastructures.Datastructure`, `compas.json_dump`, `compas.json_load`, etc.
* Added `pretty` parameter to `compas.json_dump` and `compas.json_dumps`.
* Added `compas.data.Data` as base object for all data objects (geometry, data structures, ...).

### Changed

* Moved `compas.utilities.DataEncoder` to `compas.data`.
* Moved `compas.utilities.DataDecoder` to `compas.data`.
* Changed base object of `compas.datastructures.Datastructure` to `compas.data.Data`.
* Changed base object of `compas.geometry.Primitive` to `compas.data.Data`.
* Renamed `Base` to `Data` for all data based classes.
* Fixed calculation of triangle normals.
* Fixed calculation of triangle areas.

### Removed

## [1.4.0] 2021-04-09

### Added

* Added Python 3.9 support.
* Added crease handling to catmull-clark subdivision scheme.
* Added `compas_ghpython.get_grasshopper_userobjects_path` to retrieve User Objects target folder.
* Added direction option for mesh thickening.
* Added check for closed meshes.
* Added 'loop' and 'frames' to schemes of `compas.datastructures.mesh.subdivision.mesh_subdivide`.

### Changed

* Fixed box scaling.
* Fixed a bug in `Polyline.divide_polyline_by_length` related to a floating point rounding error.
* Fixed bug in `RobotModel.zero_configuration`.
* Fixed bug in `compas.geometry.normals`.
* Fixed bug in `compas.datastructures.mesh.subdivision.mesh_subdivide_frames`.

### Removed

## [1.3.0] 2021-03-26

### Added

* Added a `invert` and `inverted` method `compas.geometry.Vector`.
* Added unetary `__neg__` operator for `compas.geometry.Vector`.
* Added `compas.robots.Configuration`, moved from `compas_fab`.

### Changed

* Fixed rhino packages installation to remove duplicates

### Removed

## [1.2.1] 2021-03-19

### Added

### Changed

### Removed

* Fixed API removals from 1.0.0 -> 1.2.0

## [1.2.0] 2021-03-18

### Added

* Added `divide_polyline`, `divide_polyline_by_length`, `Polyline.split_at_corners` and `Polyline.tangent_at_point_on_polyline`.
* Added the magic method `__str__` to `compas.geoemetry.Transformation`.
* Added `redraw` flag to the `compas_rhino` methods `delete_object`, `delete_objects` and `purge_objects`.
* Added the `__eq__` method for `compas.geometry.Circle` and `compas.geometry.Line`.
* Added support for Pylance through static API definitions.
* Added `halfedge_strip` method to `compas.datastructures.HalfEdge`.

### Changed

* Fixed bug where mimic joints were considered configurable.
* Fixed bug where `!=` gave incorrect results in Rhino for some compas objects.
* Fixed bug where `compas_rhino.BaseArtist.redraw` did not trigger a redraw.
* Fixed minor bugs in `compas.geometry.Polyline` and `compas.geometry.Polygon`.
* Fixed very minor bugs in `compas.geometry.Frame` and `compas.geometry.Quaternion`.
* Fixed bug in `compas_rhino.objects.MeshObject.modify`.
* Fixed bug in `compas_rhino.objects.MeshObject.modify_vertices`.
* Fixed bug in `compas_rhino.objects.MeshObject.modify_edges`.
* Fixed bug in `compas_rhino.objects.MeshObject.modify_faces`.
* Fixed bug in `compas_rhino.objects.VolMeshObject.modify`.
* Fixed bug in `compas_rhino.objects.VolMeshObject.modify_vertices`.
* Fixed bug in `compas_rhino.objects.VolMeshObject.modify_edges`.
* Fixed bug in `compas_rhino.objects.VolMeshObject.modify_faces`.
* Fixed bug in `compas_rhino.objects.NetworkObject.modify`.
* Fixed bug in `compas_rhino.objects.NetworkObject.modify_vertices`.
* Fixed bug in `compas_rhino.objects.NetworkObject.modify_edges`.
* Changed `compas_rhino.objects.inspect` to `compas_rhino.objects.inspectors`.
* Changed `compas_rhino.objects.select` to `compas_rhino.objects._select`.
* Changed `compas_rhino.objects.modify` to `compas_rhino.objects._modify`.

### Removed

## [1.1.0] 2021-02-12

### Added

* Added `RobotModel.remove_link`, `RobotModel.remove_joint`, `RobotModel.to_urdf_string`, and `RobotModel.ensure_geometry`.
* Added Blender Python-example to the documentation section: Tutorials -> Robots
* Added `compas_blender.unload_modules`.
* Added `after_rhino_install` and `after_rhino_uninstall` pluggable interfaces to extend the install/uninstall with arbitrary steps.

### Changed

* Fixed bug in parameter list of function `mesh_bounding_box` bound as method `Mesh.bounding_box`.
* Fixed bug in `RobotModel/RobotModelArtist.update` which raised an error when the geometry had not been loaded.
* Changed exception type when subdivide scheme argument is incorrect on `mesh_subdivide`.
* The `compas_rhino.artist.RobotModelArtist` functions `draw_visual` and `draw_collision` now return list of newly created Rhino object guids.
* Added ability of `RobotModel.add_link` to accept primitives in addition to meshes.
* Fixed bug regarding the computation of `Joint.current_origin`.
* Fixed bug regarding a repeated call to `RobotModel.add_joint`.
* Fixed bug in `compas_blender.RobotModelArtist.update`.
* Fixed bug in `compas.datastructures.mesh_slice_plane`.
* Fixed bug where initialising a `compas_blender.artists.Robotmodelartist` would create a new collection for each mesh and then also not put the mesh iton the created collection.
* Changed the initialisation of `compas_blender.artists.Robotmodelartist` to include a `collection`-parameter instead of a `layer`-parameter to be more consistent with Blender's nomenclature.
* Used a utility function from `compas_blender.utilities` to create the collection if none exists instead of using a new call to a bpy-method.

### Removed

## [1.0.0] 2021-01-18

### Added

* Added `compas.datastructures.mesh.trimesh_samplepoints_numpy`.

### Changed

* Fix Rhino7 Mac installation path
* Separate `compas.robots.Joint.origin` into the static parent-relative `origin` and the dynamic world-relative `current_origin`.
* Separate `compas.robots.Joint.axis` into the static parent-relative `axis` and the dynamic world-relative `current_axis`.
* Fixed support to convert back and forth between `compas.datastructures.Graph` and NetworkX `DiGraph`.

### Removed

## [0.19.3] 2020-12-17

### Added

### Changed

* Fix bug in `compas.datastructures.Network.neighborhood`.

### Removed

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
* Fixed data serialization in `compas.datastructures.HalfFace`.

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
* `compas.scene.SceneObject` will now track a list of drawn Objects/GUIDs.

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
* Added max int key to serialization of graph.

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
* Updated network plotter in correspondence with network.
* Integrated mixin functionality and removed mixins.
* Meshes are now initially hidden in `compas_blender.artists.RobotModelArtist`.
* `compas_blender.artists.RobotModelArtist.draw_visual` and `compas_blender.artists.RobotModelArtist.draw_collision` now show those meshes.
* Renamed the method `draw_geometry` of `compas.robots.base_artist.RobotModelBaseArtist` to `create_geometry`.

### Removed

* Removed parallelization from network algorithms.
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

* Indirectly changed mesh serialization to JSON (by changing key conversion and moving conversion into JSON methods).
* Moved conversion of int keys of mesh data to strings for json serialization to from/to json.
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
