********************************************************************************
Visualisation
********************************************************************************

COMPAS (data) objects can be visualised by placing them into a "scene".

>>> from compas.scene import Scene
>>> from compas.geometry import Box
>>> box = Box(1)
>>> scene = Scene()
>>> scene.add(box)
>>> scene.redraw()

.. When a COMPAS object is added, the scene automatically creates a corresponding scene object for the current/active visualisation context.
.. Currently, four visualisation contexts are supported: COMPAS Viewer (default), Rhino, Grasshopper, and Blender.

Scene Objects
=============

When a COMPAS object is added to a scene, a scene object is created automatically, corresponding to the type of COMPAS object.

>>> sceneobj = scene.add(box)
>>> sceneobj
BoxObject

The scene object holds a reference to the COMPAS data object, and stores its visualisation settings and transformation matrix.
Multiple scene objects can be created for the same COMPAS data object, each with different visualisation settings and transformations.

>>> sceneobj1 = scene.add(box)
>>> sceneobj2 = scene.add(box)
>>> sceneobj1 is sceneobj2
False
>>> sceneobj1.data is sceneobj2.data
True

Visualiation Settings
=====================

Scene objects have visualisation settings that can be changed by setting the corresponding attributes.
All scene objects have a color attribute.

>>> sceneobj = scene.add(box)
>>> sceneobj.color
Color(0.0, 0.0, 0.0, alpha=1.0)

Color attributes can be set using a COMPAS Color object, or a tuple of RGB values, with the color components specified as floats in the range 0.0-1.0 or as integers in the range 0-255.

.. note::

    For more information about working with colors in COMPAS, see :doc:`basics.colors`.

>>> sceneobj.color = (255, 0, 0)
>>> sceneobj.color
Color(1.0, 0.0, 0.0, alpha=1.0)

Visualisation settings can be changed by modifying the corresponding attributes of the scene object, or by providing values or the attributes to the :meth:`Scene.add` method.

>>> sceneobj = scene.add(box, color=(0, 255, 0))
>>> sceneobj.color
Color(0.0, 1.0, 0.0, alpha=1.0)

Some objects have additional color attributes, for more precise control over the visualisation.
For example, meshes can have different colors for the vertices, the edges, and the faces.
And the colors of vertices, edges, and faces can be specified individually, per element.
See the section about mesh visualisation for more information.

Object Transformation
=====================

All scene objects have a transformation matrix that can be used to transform the object in the visualisation,
independently of the geometry of the underlying data object.
The default transformation matrix is the identity matrix, which means that the visualised geometry is the same as the geometry represented by the data.

>>> sceneobj = scene.add(box)
>>> sceneobj.transformation
Transformation([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])

The transformation matrix can be set using a COMPAS Transformation object, or a 4x4 nested list of floats.

>>> from compas.geometry import Translation
>>> sceneobj.transformation = Translation.from_vector([1.0, 2.0, 3.0])
>>> sceneobj.transformation
Transformation([[1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 2.0], [0.0, 0.0, 1.0, 3.0], [0.0, 0.0, 0.0, 1.0]])

.. note::

    For more information about working with transformations in COMPAS, see :doc:`basics.geometry.transformations`.

Scene Hierarchy
===============

Scene objects are organised in a hierarchy, with the scene as the root node.
The hierarchy is represented by a COMPAS Tree data structure.
All scene objects are nodes in the tree.
The scene tree has an implicit root node, which is the scene itself.

>>> scene = Scene()
>>> scene.root
SceneObject

By default, every scene object is added as a direct child of the scene.

>>> sceneobj = scene.add(box)
>>> sceneobj.parent
SceneObject
>>> scene.children()
[BoxObject]

To use a different scene object as the parent, the parent attribute of the scene object can be set to the desired parent.

>>> from compas.geometry import Point
>>> point = Point(1, 2, 3)
>>> pointobj = scene.add(point)
>>> boxobj = scene.add(box, parent=pointobj)
>>> boxobj.parent
PointObject
