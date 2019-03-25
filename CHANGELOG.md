# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
