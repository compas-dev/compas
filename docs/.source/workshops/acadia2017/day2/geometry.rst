.. _acadia2017_day2_geometry:

********************************************************************************
Geometry
********************************************************************************

Introduction
======================================

The *compas* framework contains an extensive set of python geometry functions 
and algorithms without any external dependencies. Code using the geometry 
package can run in any Python or IronPython environment. Hence, any algorithm
or program using the geometry package can easily be integrated in different
applications (e.g.: Rhino, Blender, Maya, ...)

The full geometry reference can be found here:

* :mod:`compas.geometry`

.. note::

    Besides many basic geometry functions such as:

    * :mod:`compas.geometry.add_vectors`
    * :mod:`compas.geometry.subtract_vectors`
    * :mod:`compas.geometry.intersection_line_plane`
    * :mod:`compas.geometry.closest_point_on_polyline`
    * :mod:`compas.geometry.is_point_in_triangle`
    * ...

    The geometry package also includes geometry 
    algorithms such as:

    * :mod:`compas.geometry.planarize_faces`
    * :mod:`compas.geometry.smooth_centroid`
    * :mod:`compas.geometry.smooth_area`
    * :mod:`compas.geometry.discrete_coons_patch`
    * ...   


Object-Oriented Interface vs Functions
======================================

The geometry package features an object-oriented interface:

.. plot::
    :include-source:

    from compas.geometry import Vector

    u = Vector(1.0, 0.0, 0.0)
    v = Vector(0.0, 1.0, 0.0)

    r = u + v

    print(r)
    print(r.length)


The same vector calculations can be computed using functions and 
lists (or tuples) as vectors:

.. plot::
    :include-source:

    from compas.geometry import add_vectors
    from compas.geometry import length_vector

    u = (1.0, 0.0, 0.0)
    v = (0.0, 1.0, 0.0)

    r = add_vectors(u, v)

    print(r)
    print(length_vector(r))


Exercise: 
---------

Create a set of 10.000 random vectors with the origin (1. ,2. ,3.) and compute their
resultant. Compare the preformance of an object-based and function-based method.  

.. seealso::

    * :meth:`compas.geometry.Vector.from_start_end`
    * :meth:`compas.geometry.Vector.from_start_end`

    * :func:`compas.geometry.vector_from_points`
    * :func:`compas.geometry.add_vectors`
    * :func:`compas.geometry.sum_vectors`


Solution:

.. plot::
    :include-source:


    from random import random as rnd
    import time

    from compas.geometry import Vector

    from compas.geometry import add_vectors
    from compas.geometry import sum_vectors
    from compas.geometry import vector_from_points


    # create random points
    points = [(rnd(), rnd(), rnd()) for _ in range(10000)]
    # define origin
    origin = [1., 2., 3.]


    # Object-based method
    tic = time.time()
    #-------------------------
    vecs = [Vector.from_start_end(origin, pt) for pt in points]
    res = Vector(0., 0., 0.)
    for v in vecs:
        res += v
    #-------------------------
    toc = time.time()
    print('{0} seconds to compute for object-based method'.format(toc - tic))
    print(res)
    print('------------------')


    # Function-based method A
    tic = time.time()
    #-------------------------
    vecs = [vector_from_points(origin, pt) for pt in points]
    res = [0., 0., 0.]
    for v in vecs:
        res = add_vectors(res, v)
    #-------------------------
    toc = time.time()
    print('{0} seconds to compute for function-based method A'.format(toc - tic))
    print(res)
    print('------------------')


    # Function-based method B
    tic = time.time()
    #-------------------------
    vecs = [vector_from_points(origin, pt) for pt in points]
    res = sum_vectors(vecs)
    #-------------------------
    toc = time.time()
    print('{0} seconds to compute for function-based method B'.format(toc - tic))
    print(res)
    print('------------------')


Translational Surfaces for Gridshells
======================================

Using translational surfaces for the design of gridshells allows to explore freeform
spaces that can be built from planar (glass) panels. Jörg Schlaich together with Hans 
Schober developed several geometric design methods for various gridshells built in the 
last decades.

.. figure:: /_images/sbp.jpg
    :figclass: figure
    :class: figure-img img-fluid

    Cabot Circus Bristol and Deutsches Historisches Museum (Photo: SBP)


.. note::

    The following examples are made to be visualised in Rhino. Please check if you 
    have the right IronPython version installed.

    Open the script editor in Rhino (Command: _EditPythonScript) and run:

     .. code-block:: python

        import sys
        print(sys.version_info)

    Make sure to have version 2.7.5 installed!


The following example shows the generation of a simple tanslation surface based on a
given profile and rail curve. 

.. note::

    The following examples are based on the 3dm file:

    * :download:`trans_srf.3dm </../../examples/trans_srf.3dm>`


.. figure:: /_images/trans_srf_01.jpg
    :figclass: figure
    :class: figure-img img-fluid

    See 3dm file for details 


.. code-block:: python

    import rhinoscriptsyntax as rs

    from compas.geometry import subtract_vectors
    from compas.geometry import centroid_points
    from compas.geometry import translate_points

    # Get inputs
    crv_p = rs.GetObject("Select profile", 4)
    crv_r = rs.GetObject("Select rail",4)

    div_p = 20
    div_r = 40

    # divide profile and rail curve
    pts_p = rs.DivideCurve(crv_p, div_p)
    pts_r = rs.DivideCurve(crv_r, div_r)


    # ------------------------------
    # compas geometry function

    # reference point for profile curve
    pt_ref = centroid_points([pts_p[0], pts_p[-1]])

    # create profiles along the rail curve
    pts_sets = []
    for i in range(div_r + 1):
        vec_1 = subtract_vectors(pts_r[i], pt_ref)
        points = translate_points(pts_p, vec_1)
        pts_sets.append(points)

    # create polyline point sets for each face
    polys = []
    for i in xrange(len(pts_sets)-1):
        for j in xrange(len(pts_sets[i])-1):
            p1 = pts_sets[i][j] 
            p2 = pts_sets[i + 1][j] 
            p3 = pts_sets[i + 1][j + 1] 
            p4 = pts_sets[i][j + 1]
            polys.append([p1, p2, p3, p4, p1])

    # compas geometry function
    # ------------------------------

    # draw gridshell in Rhino
    rs.EnableRedraw(False)
    for poly in polys:
        rs.AddPolyline(poly)
    rs.EnableRedraw(True)



The following example shows the generation of a tanslation surface with profile
curves aligned with the rail curve.

.. figure:: /_images/trans_srf_03.jpg
    :figclass: figure
    :class: figure-img img-fluid

    See 3dm file for details 

.. seealso::

<<<<<<< HEAD



    planes: explain!!!





=======
>>>>>>> 02764e606e7ef25e5564062260cd86eb20197fa8
    * :func:`compas.geometry.project_points_plane`

.. code-block:: python

    import rhinoscriptsyntax as rs

    from compas.geometry import subtract_vectors
    from compas.geometry import project_points_plane

    # Get inputs
    crv_p = rs.GetObject("Select profile", 4)
    crv_a = rs.GetObject("Select rail 1",4)

    div_p = 20
    div_r = 40

    # divide profile and rail curve
    pts_p = rs.DivideCurve(crv_p, div_p)
    pts_a = rs.DivideCurve(crv_a, div_r)


    # ------------------------------
    # compas geometry function

    # create planes along the rail curve
    planes = []
    for i in range(div_r):
        vec = subtract_vectors(pts_a[i + 1], pts_a[i])
        planes.append([pts_a[i], vec])

    # subsequentely project profile curve to all planes
    pts_uv = []
    pts = pts_p
    for i in range(div_r - 1):
        pts = project_points_plane(pts, planes[i])
        pts_uv.append(pts)

    # create polyline point sets for each face
    polys = []
    for u in xrange(len(pts_uv)-1):
        for v in xrange(len(pts_uv[u])-1):
            p1 = pts_uv[u][v] 
            p2 = pts_uv[u + 1][v] 
            p3 = pts_uv[u + 1][v + 1] 
            p4 = pts_uv[u][v + 1]
            polys.append([p1, p2, p3, p4, p1])

    # compas geometry function
    # ------------------------------

    # draw gridshell in Rhino
    rs.EnableRedraw(False)
    for poly in polys:
        rs.AddPolyline(poly)
    rs.EnableRedraw(True)

Exercise: 
---------

The following figure shows the generation of a tanslation surface with two profile
curves. The method geneartes planes along the two rail curves and subsequentely uses
intersections with conical extrusions to guarantee the planarity of resulting mesh.

.. figure:: /_images/trans_srf_04.jpg
    :figclass: figure
    :class: figure-img img-fluid

    See 3dm file for details 

The steps of the algorithm are:
* blabla bl lal lsldd bllbblb
  blblblbl bldlbl
  (:func:`compas.geometry.add_vectors`)
* ....

.. note::

    The following examples is also available for Grasshopper:

    * :download:`trans_srf.3dm </../../examples/trans_srf.gh>`


.. seealso::

    * :func:`compas.geometry.add_vectors`
    * :func:`compas.geometry.centroid_points`
    * :func:`compas.geometry.intersection_line_plane`
    * :func:`compas.geometry.intersection_line_line`


.. code-block:: python

    import rhinoscriptsyntax as rs

    from compas.geometry import subtract_vectors
    from compas.geometry import add_vectors
    from compas.geometry import centroid_points
    from compas.geometry import intersection_line_plane
    from compas.geometry import intersection_line_line
        
    # Get inputs
    crv_p = rs.GetObject("Select profile", 4)
    crv_a = rs.GetObject("Select rail 1",4)
    crv_b = rs.GetObject("Select rail 2",4)

    div_p = 20
    div_r = 40

    # divide profile and rail curves
    pts_p = rs.DivideCurve(crv_p, div_p)
    pts_a = rs.DivideCurve(crv_a, div_r)
    pts_b = rs.DivideCurve(crv_b, div_r)

    # ------------------------------
    # compas geometry function

    # create planes along the rail curve
    planes = []
    for i in range(div_r):
        pt_mid = centroid_points([pts_a[i], pts_b[i]])
        vec_a = subtract_vectors(pts_a[i + 1], pts_a[i])
        vec_b = subtract_vectors(pts_b[i + 1], pts_b[i])
        vec_a = normalize_vector(vec_a)
        vec_b = normalize_vector(vec_b)
        vec = add_vectors(vec_a, vec_b)
        planes.append([pt_mid, vec])

    # create profiles
    pts_uv = []
    pts = pts_p
    for i in range(div_r - 1):
        ray_a = [pts_a[i], pts_a[i + 1]]
        ray_b = [pts_b[i], pts_b[i + 1]]
        pts_x = intersection_line_line(ray_a, ray_b)
        if None in pts_x:
            print("parallel!")
        pt_cent = centroid_points(pts_x)
        # computes intersection between a plane and all lines
        # from the profile curve points to the intersection point
        pts = [intersection_line_plane([pt, pt_cent], planes[i + 1]) for pt in pts]
        
        pts_uv.append(pts)

    # create polyline point sets for each face
    polys = []
    for u in xrange(len(pts_uv)-1):
        for v in xrange(len(pts_uv[u])-1):
            p1 = pts_uv[u][v] 
            p2 = pts_uv[u + 1][v] 
            p3 = pts_uv[u + 1][v + 1] 
            p4 = pts_uv[u][v + 1]
            polys.append([p1, p2, p3, p4, p1])

    # compas geometry function
    # ------------------------------

    # draw gridshell in Rhino
    rs.EnableRedraw(False)
    for poly in polys:
        rs.AddPolyline(poly)
    rs.EnableRedraw(True)




Torsion-free Elements for Gridshells
====================================

- Create a 3D coons patch.


.. code-block:: python

    import rhinoscriptsyntax as rs

    from compas.geometry import add_vectors

    from compas.datastructures.mesh import Mesh
    from compas_rhino.helpers.artists.meshartist import MeshArtist
    from compas.geometry.algorithms.interpolation import discrete_coons_patch
    from compas.datastructures import mesh_cull_duplicate_vertices



    crv_ab = rs.GetObject("Select ab",4)
    crv_bc = rs.GetObject("Select bc",4)
    crv_dc = rs.GetObject("Select cd",4)
    crv_ad = rs.GetObject("Select ad",4)

    div_a = 15
    div_b = 15

    ab, bc, dc, ad = None, None, None, None

    if crv_ab: ab = rs.DivideCurve(crv_ab, div_a)
    if crv_bc: bc = rs.DivideCurve(crv_bc, div_b)
    if crv_dc: dc = rs.DivideCurve(crv_dc, div_a)
    if crv_ad: ad = rs.DivideCurve(crv_ad, div_b)

    vertices, face_vertices = discrete_coons_patch(ab, bc, dc, ad)
    coon = Mesh.from_vertices_and_faces(vertices, face_vertices)

    artist = MeshArtist(coon, layer='MeshArtist')
    artist.draw_edges()
    artist.draw_vertices()
    artist.draw_faces()
    #artist.redraw(1.0)


    for u, v in coon.edges():
        pt_u = coon.vertex_coordinates(u)
        pt_v = coon.vertex_coordinates(v)
        vec_u = coon.vertex_normal(u)
        vec_v = coon.vertex_normal(v)
        pt_uu = add_vectors(pt_u, vec_u)
        pt_vv = add_vectors(pt_v, vec_v)
        rs.AddPolyline([pt_u,pt_v,pt_vv,pt_uu,pt_u])




- make a mesh.
- populate fins

- planarize fins
- constrain fins to a specific height


Tessellation of a freeform barrel vault
=======================================

