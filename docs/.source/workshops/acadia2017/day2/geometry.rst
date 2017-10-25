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

Create a set of 1.000 random vectors with the origin (1. ,2. ,3.) and compute their
resultant. Compare the preformance of an object-based and function-based method.  

.. seealso::

	* :method:`compas.geometry.objects.vector.from_start_end`
	* :method:`compas.geometry.objects.vector.from_start_end`

	* :func:`compas.geometry.constructors.vector_from_points`
	* :func:`compas.geometry.basic.add_vectors`
	* :func:`compas.geometry.basic.sum_vectors`


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

.. figure:: /_images/sbp_bristol.jpg
    :figclass: figure
    :class: figure-img img-fluid

Cabot Circus Bristol (Photo: SBP)


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

* :download:`mesh-smoothing.3dm </../../examples/mesh-smoothing.3dm>`

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


The following example shows the generation of a simple tanslation surface based on a
given profile and rail curve. 






