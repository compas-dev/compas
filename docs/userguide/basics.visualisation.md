# Visualisation

COMPAS (data) objects can be visualised by placing them into a "scene".

```python
>>> from compas.scene import Scene
>>> from compas.geometry import Box
>>> box = Box(1)
>>> scene = Scene()
>>> scene.add(box)
>>> scene.draw()
```

## Scene Objects

When a COMPAS object is added to a scene, a scene object is created automatically, corresponding to the type of COMPAS object.

```python
>>> sceneobj = scene.add(box)
>>> sceneobj
BoxObject
```

The scene object holds a reference to the COMPAS data object, and stores its visualisation settings and transformation matrix.
Multiple scene objects can be created for the same COMPAS data object, each with different visualisation settings and transformations.

```python
>>> sceneobj1 = scene.add(box)
>>> sceneobj2 = scene.add(box)
>>> sceneobj1 is sceneobj2
False
>>> sceneobj1.data is sceneobj2.data
True
```

## Visualisation Settings

Scene objects have visualisation settings that can be changed by setting the corresponding attributes.
All scene objects have a color attribute.

```python
>>> sceneobj = scene.add(box)
>>> sceneobj.color
Color(0.0, 0.0, 0.0, alpha=1.0)
```

Color attributes can be set using a COMPAS Color object, or a tuple of RGB values, with the color components specified as floats in the range 0.0-1.0 or as integers in the range 0-255.

!!! note

    For more information about working with colors in COMPAS, see [Colors](basics.colors.md).

```python
>>> sceneobj.color = (255, 0, 0)
>>> sceneobj.color
Color(1.0, 0.0, 0.0, alpha=1.0)
```

Visualisation settings can be changed by modifying the corresponding attributes of the scene object, or by providing values for the attributes to the `Scene.add` method.

```python
>>> sceneobj = scene.add(box, color=(0, 255, 0))
>>> sceneobj.color
Color(0.0, 1.0, 0.0, alpha=1.0)
```

Some objects have additional color attributes, for more precise control over the visualisation.
For example, meshes can have different colors for the vertices, the edges, and the faces.
And the colors of vertices, edges, and faces can be specified individually, per element.

## Scene Hierarchy

Scene objects are organised in a hierarchy, with the scene as the root node.
The hierarchy is represented by a COMPAS Tree data structure.
All scene objects are nodes in the tree.
The scene tree has an implicit root node, which is the scene itself.

```python
>>> scene = Scene()
>>> scene.root
SceneObject
```

By default, every scene object is added as a direct child of the scene.

```python
>>> sceneobj = scene.add(box)
>>> sceneobj.parent
SceneObject
>>> scene.children()
[BoxObject]
```

To use a different scene object as the parent, the parent attribute of the scene object can be set to the desired parent.

```python
>>> from compas.geometry import Point
>>> point = Point(1, 2, 3)
>>> pointobj = scene.add(point)
>>> boxobj = scene.add(box, parent=pointobj)
>>> boxobj.parent
PointObject
```

## Object Frame And Transformation

Every scene object can have a reference "frame" that represents its local coordinate system relative to the frame of its hierarchical parent.
In addition, an object can also have a local "transformation" which orientates this object from its frame.
The final transformation of an object relative to the world coordinate system is the aggregated multiplication of all its hierarchical ancestors' frames, together with its own local frame and transformation. This property can be accessed through the read-only attribute `worldtransformation`.

```python
>>> from compas.geometry import Translation
>>> from compas.geometry import Box
>>> from compas.geometry import Frame
>>> sceneobj1 = scene.add(Box())
>>> sceneobj1.frame = Frame(point=[1.0, 0.0, 0.0], xaxis=[1.0, 0.0, 0.0], yaxis=[0.0, 1.0, 0.0])
>>> sceneobj1.transformation = Translation.from_vector([10.0, 0.0, 0.0])
>>> sceneobj1.worldtransformation
Transformation([[1.0, 0.0, 0.0, 11.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]], check=False)
```

## Scene Context

Depending on where the code is executed, the "scene" will detect the current visualisation context.
If the code is executed in Rhino, the scene context will be automatically set as "Rhino".

```python
>>> from compas.scene import Scene
>>> from compas.geometry import Box
>>> scene = Scene()
>>> scene.context
Rhino
```

For every context, the appropriate scene object implementations will be used automatically.

```python
>>> box = Box.from_width_height_depth(1, 1, 1)
>>> scene.add(box)
<compas_rhino.scene.BoxObject>
```

Users can also set the scene context manually:

```python
>>> scene = Scene(context="MyContextName")
>>> scene.context
MyContextName
```

The currently supported contexts are: "Viewer", "Rhino", "Grasshopper", "Blender" and None.
For working with different contexts please refer to the [CAD sections](cad.rhino.md).
