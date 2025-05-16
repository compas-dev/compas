import compas

if not compas.IPY:
    import pytest  # noqa: F401
    from compas.scene import context
    from compas.scene import register
    from compas.scene import Scene
    from compas.scene import SceneObject
    from compas.scene import SceneObjectFactory
    from compas.scene import SceneObjectNotRegisteredError
    from compas.data import Data
    from compas.geometry import Box
    from compas.geometry import Frame
    from compas.geometry import Translation
    from compas.scene import get_sceneobject_cls
    from compas.datastructures import Tree

    @pytest.fixture(autouse=True)
    def reset_sceneobjects_registration():
        # before each test
        yield
        # after each test, reset scene objects
        context.ITEM_SCENEOBJECT.clear()

    def register_fake_context():
        register(FakeItem, FakeSceneObject, context="fake")

    class FakeSceneObject(SceneObject):
        def draw(self):
            pass

        def clear(self):
            pass

    class FakeSubSceneObject(SceneObject):
        def draw(self):
            pass

        def clear(self):
            pass

    class FakeItem(Data):
        pass

    class FakeSubItem(FakeItem):
        pass

    def test_get_sceneobject_cls_with_orderly_registration():
        register(FakeItem, FakeSceneObject, context="fake")
        register(FakeSubItem, FakeSubSceneObject, context="fake")
        item = FakeItem()
        sceneobject = SceneObjectFactory(item=item, context="fake")
        assert isinstance(sceneobject, FakeSceneObject)

        item = FakeSubItem()
        sceneobject = SceneObjectFactory(item=item, context="fake")
        assert isinstance(sceneobject, FakeSubSceneObject)

    def test_get_sceneobject_cls_with_out_of_order_registration():
        register(FakeSubItem, FakeSubSceneObject, context="fake")
        register(FakeItem, FakeSceneObject, context="fake")
        item = FakeItem()
        sceneobject = SceneObjectFactory(item=item, context="fake")
        assert isinstance(sceneobject, FakeSceneObject)

        item = FakeSubItem()
        sceneobject = SceneObjectFactory(item=item, context="fake")
        assert isinstance(sceneobject, FakeSubSceneObject)

        def test_sceneobject_auto_context_discovery(mocker):
            register_fake_context()

            item = FakeItem()
            sceneobject = SceneObjectFactory(item=item)

            assert isinstance(sceneobject, FakeSceneObject)

        def test_sceneobject_auto_context_discovery_no_context(mocker):
            mocker.patch("compas.scene.scene.detect_current_context", return_value=False)
            mocker.patch("compas.scene.scene.detect_current_context", return_value=False)

            with pytest.raises(SceneObjectNotRegisteredError):
                item = FakeSubItem()
                _ = SceneObjectFactory(item=item)

    def test_sceneobject_transform():
        scene = Scene()
        sceneobj1 = scene.add(Box())
        sceneobj1.transformation = Translation.from_vector([10.0, 0.0, 0.0])
        assert sceneobj1.worldtransformation == sceneobj1.transformation
        assert sceneobj1.worldtransformation == Translation.from_vector([10.0, 0.0, 0.0])
        assert sceneobj1.frame == Frame([10.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
        assert sceneobj1.frame.to_transformation() == Translation.from_vector([10.0, 0.0, 0.0])

        sceneobj2 = scene.add(Box(), parent=sceneobj1)
        sceneobj2.transformation = Translation.from_vector([10.0, 10.0, 0.0])
        assert sceneobj2.worldtransformation == sceneobj1.transformation * sceneobj2.transformation
        assert sceneobj2.worldtransformation == Translation.from_vector([20.0, 10.0, 0.0])
        assert sceneobj2.frame == Frame([20.0, 10.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
        assert sceneobj2.frame.to_transformation() == Translation.from_vector([20.0, 10.0, 0.0])

        sceneobj3 = scene.add(Box(), parent=sceneobj2)
        sceneobj3.transformation = Translation.from_vector([10.0, 10.0, 10.0])
        assert sceneobj3.worldtransformation == sceneobj1.transformation * sceneobj2.transformation * sceneobj3.transformation
        assert sceneobj3.worldtransformation == Translation.from_vector([30.0, 20.0, 10.0])
        assert sceneobj3.frame == Frame([30.0, 20.0, 10.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
        assert sceneobj3.frame.to_transformation() == Translation.from_vector([30.0, 20.0, 10.0])

    def test_scene_clear():
        scene = Scene()
        sceneobj1 = scene.add(Box())
        sceneobj2 = scene.add(Box(), parent=sceneobj1)
        sceneobj3 = scene.add(Box(), parent=sceneobj2)  # noqa: F841

        assert len(scene.objects) == 3

        scene.clear(clear_context=False, clear_scene=True)

        assert len(scene.objects) == 0

    def test_scene_context_validation():
        # Register the fake context first
        register(FakeItem, FakeSceneObject, context="fake")

        scene = Scene(context="fake")
        item = FakeItem()

        # This should work since the context matches
        sceneobj = scene.add(item, context="fake")
        assert isinstance(sceneobj, FakeSceneObject)

        # This should raise an exception since the context doesn't match
        with pytest.raises(Exception) as excinfo:
            scene.add(item, context="different")
        assert "Object context should be the same as scene context" in str(excinfo.value)

    def test_get_sceneobject_cls_none_item():
        with pytest.raises(ValueError) as excinfo:
            get_sceneobject_cls(None)
        assert "Cannot create a scene object for None" in str(excinfo.value)

    def test_get_sceneobject_cls_auto_registration():
        # Clear the registration
        context.ITEM_SCENEOBJECT.clear()

        # This should trigger auto-registration
        item = FakeItem()
        register(FakeItem, FakeSceneObject, context="fake")
        cls = get_sceneobject_cls(item, context="fake")
        assert cls == FakeSceneObject

    def test_get_sceneobject_cls_inheritance():
        # Register base class
        register(FakeItem, FakeSceneObject, context="fake")

        # Test that subclass uses base class's scene object
        item = FakeSubItem()
        cls = get_sceneobject_cls(item, context="fake")
        assert cls == FakeSceneObject

    def test_get_sceneobject_cls_custom_type():
        item = FakeItem()
        cls = get_sceneobject_cls(item, context="fake", sceneobject_type=FakeSubSceneObject)
        assert cls == FakeSubSceneObject

    def test_get_sceneobject_cls_no_registration():
        # Clear the registration
        context.ITEM_SCENEOBJECT.clear()

        # Try to get scene object for unregistered item
        item = FakeItem()
        with pytest.raises(SceneObjectNotRegisteredError) as excinfo:
            get_sceneobject_cls(item, context="fake")
        assert "No scene object is registered for this data type" in str(excinfo.value)

    def test_scene_representation():
        # Create a scene with a hierarchy of objects
        scene = Scene(context="fake")
        register(FakeItem, FakeSceneObject, context="fake")

        # Create items and add them to the scene
        root_item = FakeItem()
        child1_item = FakeItem()
        child2_item = FakeItem()
        grandchild1_item = FakeItem()
        grandchild2_item = FakeItem()

        # Add objects to create a hierarchy
        root = scene.add(root_item)
        child1 = scene.add(child1_item, parent=root)
        scene.add(child2_item, parent=root)
        scene.add(grandchild1_item, parent=child1)
        scene.add(grandchild2_item, parent=child1)

        # Get the string representation
        scene_repr = str(scene)

        # The representation should show the hierarchy with scene objects
        expected_lines = [
            "└── Scene",
            "    └── <FakeSceneObject: FakeItem>",
            "        ├── <FakeSceneObject: FakeItem>",
            "        │   ├── <FakeSceneObject: FakeItem>",
            "        │   └── <FakeSceneObject: FakeItem>",
            "        └── <FakeSceneObject: FakeItem>",
        ]

        # Compare each line
        for expected, actual in zip(expected_lines, scene_repr.split("\n")):
            assert expected == actual

    def test_scene_initialization(mocker):
        # Mock context detection at the correct import path
        mocker.patch("compas.scene.scene.detect_current_context", return_value="fake")
        
        # Test default initialization
        scene = Scene()
        assert scene.context == "fake"
        assert scene.datastore == {}
        assert scene.objectstore == {}
        assert scene.tree is not None
        assert scene.tree.root is not None
        assert scene.tree.root.name == scene.name

        # Test initialization with custom parameters
        custom_tree = Tree()
        custom_datastore = {"test": "data"}
        custom_objectstore = {"test": "object"}
        scene = Scene(context="test", tree=custom_tree, datastore=custom_datastore, objectstore=custom_objectstore)
        assert scene.context == "test"
        assert scene.tree == custom_tree
        assert scene.datastore == custom_datastore
        assert scene.objectstore == custom_objectstore

    def test_scene_data():
        scene = Scene()
        data = scene.__data__
        assert "name" in data
        assert "attributes" in data
        assert "datastore" in data
        assert "objectstore" in data
        assert "tree" in data

    def test_scene_items():
        scene = Scene(context="fake")
        register(FakeItem, FakeSceneObject, context="fake")

        item1 = FakeItem()
        item2 = FakeItem()
        scene.add(item1)
        scene.add(item2)

        items = scene.items
        assert len(items) == 2
        assert item1 in items
        assert item2 in items

    def test_scene_context_objects(mocker):
        mocker.patch("compas.scene.scene.detect_current_context", return_value="fake")
        scene = Scene(context="fake")
        register(FakeItem, FakeSceneObject, context="fake")
        
        item = FakeItem()
        sceneobj = scene.add(item)
        
        # Mock the _guids attribute to return test guids
        sceneobj._guids = ["guid1", "guid2"]
        
        context_objects = scene.context_objects
        assert len(context_objects) == 2
        assert "guid1" in context_objects
        assert "guid2" in context_objects

    def test_scene_find_by_name():
        scene = Scene(context="fake")
        register(FakeItem, FakeSceneObject, context="fake")

        item = FakeItem()
        sceneobj = scene.add(item)
        sceneobj.name = "test_object"

        found = scene.find_by_name("test_object")
        assert found == sceneobj

        not_found = scene.find_by_name("nonexistent")
        assert not_found is None

    def test_scene_find_by_itemtype(mocker):
        mocker.patch("compas.scene.scene.detect_current_context", return_value="fake")
        scene = Scene(context="fake")
        register(FakeItem, FakeSceneObject, context="fake")
        register(FakeSubItem, FakeSubSceneObject, context="fake")
        
        # Create items and add them to the scene
        item1 = FakeItem()
        item2 = FakeSubItem()
        sceneobj1 = scene.add(item1)
        sceneobj2 = scene.add(item2)
        
        # Ensure the datastore is properly set up
        scene.datastore[str(item1.guid)] = item1
        scene.datastore[str(item2.guid)] = item2
        
        # Find objects by type
        found = scene.find_by_itemtype(FakeItem)
        assert found is not None
        assert found._item == str(item1.guid)
        
        found = scene.find_by_itemtype(FakeSubItem)
        assert found is not None
        assert found._item == str(item2.guid)
        
        not_found = scene.find_by_itemtype(str)  # type that doesn't exist in scene
        assert not_found is None

    def test_scene_find_all_by_itemtype(mocker):
        mocker.patch("compas.scene.scene.detect_current_context", return_value="fake")
        scene = Scene(context="fake")
        register(FakeItem, FakeSceneObject, context="fake")
        register(FakeSubItem, FakeSubSceneObject, context="fake")
        
        # Create items and add them to the scene
        item1 = FakeItem()
        item2 = FakeSubItem()
        item3 = FakeItem()
        sceneobj1 = scene.add(item1)
        sceneobj2 = scene.add(item2)
        sceneobj3 = scene.add(item3)
        
        # Ensure the datastore is properly set up
        scene.datastore[str(item1.guid)] = item1
        scene.datastore[str(item2.guid)] = item2
        scene.datastore[str(item3.guid)] = item3
        
        # Find all objects by type
        found = scene.find_all_by_itemtype(FakeItem)
        assert len(found) == 3
        assert all(obj._item in [str(item1.guid), str(item2.guid), str(item3.guid)] for obj in found)
        
        found = scene.find_all_by_itemtype(FakeSubItem)
        assert len(found) == 1
        assert all(obj._item == str(item2.guid) for obj in found)
        
        not_found = scene.find_all_by_itemtype(str)  # type that doesn't exist in scene
        assert len(not_found) == 0

    def test_scene_get_sceneobject_node():
        scene = Scene(context="fake")
        register(FakeItem, FakeSceneObject, context="fake")

        item = FakeItem()
        sceneobj = scene.add(item)

        # Test successful case
        node = scene.get_sceneobject_node(sceneobj)
        assert node is not None
        assert node.name == str(sceneobj.guid)

        # Test TypeError for non-SceneObject
        with pytest.raises(TypeError) as excinfo:
            scene.get_sceneobject_node("not a scene object")
        assert "SceneObject expected" in str(excinfo.value)

        # Test ValueError for SceneObject from different scene
        other_scene = Scene(context="fake")
        other_item = FakeItem()
        other_sceneobj = other_scene.add(other_item)
        with pytest.raises(ValueError) as excinfo:
            scene.get_sceneobject_node(other_sceneobj)
        assert "SceneObject not part of this scene" in str(excinfo.value)
