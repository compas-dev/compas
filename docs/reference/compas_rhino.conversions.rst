********************************************************************************
compas_rhino.conversions
********************************************************************************

.. currentmodule:: compas_rhino.conversions

.. rst-class:: lead

Conversions between Rhino geometry objects (:mod:`Rhino.Geometry`) and COMPAS geometry objects (:mod:`compas.geometry`).

Exceptions
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ConversionError


To Rhino
========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    arc_to_rhino
    box_to_rhino
    brep_to_rhino
    capsule_to_rhino_brep
    circle_to_rhino
    circle_to_rhino_curve
    cone_to_rhino
    cone_to_rhino_brep
    curve_to_rhino
    cylinder_to_rhino
    cylinder_to_rhino_brep
    ellipse_to_rhino
    ellipse_to_rhino_curve
    frame_to_rhino
    frame_to_rhino_plane
    line_to_rhino
    line_to_rhino_curve
    mesh_to_rhino
    plane_to_rhino
    point_to_rhino
    polygon_to_rhino
    polyhedron_to_rhino
    polyline_to_rhino
    polyline_to_rhino_curve
    sphere_to_rhino
    surface_to_rhino
    torus_to_rhino
    torus_to_rhino_brep
    transformation_to_rhino
    transformation_matrix_to_rhino
    vertices_and_faces_to_rhino
    vector_to_rhino


To COMPAS
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    arc_to_compas
    box_to_compas
    brep_to_compas_box
    brep_to_compas_cone
    brep_to_compas_cylinder
    brep_to_compas_sphere
    circle_to_compas
    cone_to_compas
    curve_to_compas_circle
    curve_to_compas_ellipse
    curve_to_compas_line
    curve_to_compas_polyline
    cylinder_to_compas
    ellipse_to_compas
    extrusion_to_compas_box
    extrusion_to_compas_cylinder
    extrusion_to_compas_torus
    line_to_compas
    mesh_to_compas
    plane_to_compas
    plane_to_compas_frame
    point_to_compas
    polygon_to_compas
    polyline_to_compas
    sphere_to_compas
    surface_to_compas
    surface_to_compas_data
    surface_to_compas_mesh
    surface_to_compas_quadmesh
    vector_to_compas
