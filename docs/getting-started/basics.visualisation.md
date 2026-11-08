# Visualisation

COMPAS (data) objects can be visualised by placing them into a "scene".

```pycon
>>> from compas.scene import Scene
>>> from compas.geometry import Box
>>> box = Box(1)
>>> scene = Scene()
>>> scene.add(box)
>>> scene.draw()
```

When a COMPAS object is added, the scene creates a stable, backend-neutral scene
object for its semantic type. Visualisation backends are provided by separate
COMPAS packages and register operations for these stable objects.

## Scene Objects

When a COMPAS object is added to a scene, a scene object is created automatically, corresponding to the type of COMPAS object.

```pycon
>>> sceneobj = scene.add(box)
>>> type(sceneobj).__name__
'ShapeObject'
```

The scene object holds a reference to the COMPAS data object, and stores its visualisation settings and transformation matrix.
Multiple scene objects can be created for the same COMPAS data object, each with different visualisation settings and transformations.

Core provides stable semantic scene-object types for data whose visualisation
needs additional backend-neutral settings:

- `ShapeObject` and `SurfaceObject` store the `u` and `v` discretization
  counts used to display analytic shapes and parametric surfaces.
- `FrameObject` and `PlaneObject` store their display `size`.
- `VectorObject` stores the vector's display `anchor`.
- `MeshObject` stores `hide_coplanaredges` and `use_vertexcolors` in addition
  to its vertex, edge, and face settings.

These settings describe durable presentation intent. A visualisation backend
decides how to draw them; changing the backend does not change the scene-object
type or its stored settings.

For a `FrameObject`, the inherited `geometry` property is the represented
[`Frame`][compas.geometry.Frame]. Its inherited `frame` property has the same
meaning as on every `SceneObject`: it is the world-placement frame derived from
the scene hierarchy. The two frames therefore serve different purposes.

```pycon
>>> sceneobj1 = scene.add(box)
>>> sceneobj2 = scene.add(box)
>>> sceneobj1 is sceneobj2
False
>>> sceneobj1.item is sceneobj2.item
True
```

## Visualiation Settings

Scene objects have visualisation settings that can be changed by setting the corresponding attributes.
All scene objects have a color attribute.

```pycon
>>> sceneobj = scene.add(box)
>>> sceneobj.color
Color(1.0, 1.0, 1.0, alpha=1.0)
```

Color attributes can be set using a COMPAS Color object, or a tuple of RGB values, with the color components specified as floats in the range 0.0-1.0 or as integers in the range 0-255.

!!! note

    For more information about working with colors in COMPAS, see `basics.colors`.

```pycon
>>> sceneobj.color = (255, 0, 0)
>>> sceneobj.color
Color(1.0, 0.0, 0.0, alpha=1.0)
```

Visualisation settings can be changed by modifying the corresponding attributes of the scene object, or by providing values or the attributes to the [`Scene.add`][compas.scene.Scene.add] method.

```pycon
>>> sceneobj = scene.add(box, color=(0, 255, 0))
>>> sceneobj.color
Color(0.0, 1.0, 0.0, alpha=1.0)
```

Some objects have additional color attributes, for more precise control over the visualisation.
For example, meshes can have different colors for the vertices, the edges, and the faces.
And the colors of vertices, edges, and faces can be specified individually, per element.
See the section about mesh visualisation for more information.

### Editable Attributes

Stable scene-object classes declare which of their attributes may be exposed by
an object editor. The resolved mapping contains only attribute names and
optional data-side update callbacks. Visualisation packages decide how to
construct controls and refresh their views.

```pycon
>>> attributes = type(sceneobj).editable_attributes()
>>> "show_surfaces" in attributes
True
>>> sceneobj.update_editable_attribute("opacity", 0.5)
>>> sceneobj.opacity
0.5
```

The declarations compose through the scene-object class hierarchy. A `None`
callback uses ordinary attribute assignment. A declaration may instead provide
an atomic, synchronous data-update callback when assignment alone is not
sufficient. Update callbacks never draw, rebuild render data, or refresh a user
interface.

Durable editable attributes are declared once as scene state:

```python
from compas.scene import SceneObject
from compas.scene import SceneStateField


class CustomObject(SceneObject):
    __scene_state_namespace__ = "example.CustomObject"
    __scene_state_fields__ = (SceneStateField("quality", int, required=False, editable=True),)
```

The separate `__editable_attributes__` mapping is reserved for editable
attributes that are not durable scene state. Derived callback overrides retain
the inherited attribute position, while new attributes append in declaration
order. Use
[`SceneObject.update_editable_attribute`][compas.scene.SceneObject.update_editable_attribute]
to apply the default assignment or the declared data-update callback.

Editability does not add presentation metadata to
[`SceneStateField`][compas.scene.SceneStateField] and is not serialized. A
durable scene-state field is not editable unless it explicitly sets
`editable=True`.

### Data, Scene State, and Extensions

Every scene object is a [`Data`][compas.data.Data] object. COMPAS serialization
wraps it in an envelope containing its data type, GUID, optional name, and the
payload returned by `SceneObject.__data__`. The represented geometry or
datastructure is another independent `Data` object; the scene object stores
only its GUID in the `item` field.

The scene-object payload has two state layers:

- Common state such as `transformation`, `color`, `opacity`, and `show` is
  stored directly in the payload.
- Type-specific state declared by `SceneStateField` is stored under the
  declaring class's namespace in the `extensions` mapping.

For example, a shape scene object may serialize geometry display settings and
shape resolution separately:

```python
from compas.colors import Color


payload = {
    "item": "<represented-data-guid>",
    "transformation": None,
    "color": Color.white(),
    "opacity": 1.0,
    "show": True,
    "extensions": {
        "compas.scene.GeometryObject": {
            "show_points": False,
            "show_lines": True,
        },
        "compas.scene.ShapeObject": {
            "u": 16,
            "v": 16,
        },
    },
}
```

Namespaces let subclasses and external packages add durable state without
widening the common scene-object payload. Unknown namespaced values are
preserved during a round trip for forward compatibility. Runtime item
bindings, editable-attribute callbacks, Viewer controls, selection, and render
resources are not stored in `extensions` or elsewhere in the serialized scene.

## Scene Hierarchy

Scene objects are organised in a hierarchy under an ordinary root group. A
[`SceneNode`][compas.scene.SceneNode] contains only an object GUID and child
nodes. Presentation state and the referenced data GUID belong to the stable
[`SceneObject`][compas.scene.SceneObject]. Each scene object has exactly one
node in a scene.

```pycon
>>> scene = Scene()
>>> scene.root.name
'ROOT'
```

By default, every scene object is added as a direct child of the scene.

```pycon
>>> sceneobj = scene.add(box)
>>> sceneobj.parent is scene.root
True
>>> list(scene.root.children) == [sceneobj]
True
```

## Saving Scenes and Data

A serialized scene contains its hierarchy, presentation state, and references
to data objects by GUID. It does not embed or own those data objects. Serialize
the data separately when it should outlive the current Python process.

After loading a scene, its objects and hierarchy can be inspected immediately.
Bind the independently loaded data explicitly before accessing an object's
`item` or drawing it.

```pycon
>>> description = scene.to_jsonstring()
>>> loaded_scene = Scene.from_jsonstring(description)
>>> loaded_scene.find_by_name(sceneobj.name).item_guid == box.guid
True
>>> loaded_scene.bind(box)
>>> loaded_scene.find_by_name(sceneobj.name).item is box
True
```

Use [`Scene.bind_many`][compas.scene.Scene.bind_many] when restoring several
referenced data objects at once. Bindings are runtime references: binding does
not copy the object or add it to the serialized scene description.

To use a different scene object as the parent, pass it to `Scene.add`.

```pycon
>>> from compas.geometry import Point
>>> point = Point(1, 2, 3)
>>> pointobj = scene.add(point)
>>> boxobj = scene.add(box, parent=pointobj)
>>> type(boxobj.parent).__name__
'GeometryObject'
```

## Object transformations

Every scene object stores an optional local `transformation` relative to its
parent. A value of `None` represents the identity transformation. The
`worldtransformation` property composes the local transformations of the object
and its ancestors from the hierarchy root to the object.

```pycon
>>> from compas.geometry import Box
>>> from compas.geometry import Translation
>>> parent = scene.add_group(
...     "Assembly",
...     transformation=Translation.from_vector([10.0, 0.0, 0.0]),
... )
>>> child = scene.add(
...     Box(1.0),
...     parent=parent,
...     transformation=Translation.from_vector([0.0, 2.0, 0.0]),
... )
>>> child.worldtransformation == Translation.from_vector([10.0, 2.0, 0.0])
True
```

Assigning `worldtransformation` converts the requested world transformation to
the corresponding local transformation through the inverse parent world
transformation. The parent remains unchanged.

```pycon
>>> child.worldtransformation = Translation.from_vector([20.0, 3.0, 0.0])
>>> child.transformation == Translation.from_vector([10.0, 3.0, 0.0])
True
>>> parent.transformation == Translation.from_vector([10.0, 0.0, 0.0])
True
```

`frame` is the frame represented by the current world transformation. Assigning
a frame is therefore another way to set `worldtransformation`; it is not a
separate local frame stored alongside `transformation`.

## Scene Context

Visualisation packages register `draw` and `clear` operations for stable scene
object types. Selecting another context changes operation lookup; it never
replaces the scene objects or changes their Python types. Users can select a
registered context explicitly:

```pycon
>>> scene = Scene(context="MyContextName")
>>> scene.context
MyContextName
```

Consult the documentation of the installed visualisation package for its
context name and supported object types.
