# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.17.9] 2023-11-10

### Added

### Changed

### Removed


## [1.17.8] 2023-10-06

### Added

### Changed

* Pinned `jsonschema` version to >=4.17, <4.18 to avoid Rust toolchain

### Removed


## [1.17.7] 2023-09-29

### Added

### Changed

* Fixed `SyntaxError` when importing COMPAS in GHPython.

### Removed


## [1.17.6] 2023-09-12

### Added

* Added `create_id` to `compas_ghpython.utilities`. (moved from `compas_fab`)

### Changed

* Fixed bug that caused a new-line at the end of the `compas.HERE` constant in IronPython for Mac.
* Fixed Grasshopper `draw_polylines` method to return `PolylineCurve` instead of `Polyline` because the latter shows as only points.
* Fixed uninstall post-process.
* Fixed `area_polygon` that was, in some cases, returning a negative area
* Fixed support for `System.Decimal` data type on json serialization.
* Fixed `AttributeError` in Plotter's `PolylineArtist` and `SegementArtist`.
* Fixed wrong key type when de-serializing `Graph` with integer keys leading to node not found.
* Fixed bug in `VolMeshArtist.draw_cells` for Rhino, Blender and Grasshopper.
* Fixed bug in the `is_polygon_in_polygon_xy` that was not correctly generating all the edges of the second polygon before checking for intersections.

### Removed


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
* Fixed bug in`compas_ghpython.components`that ignored input list of `.ghuser` objects to uninstall.
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
