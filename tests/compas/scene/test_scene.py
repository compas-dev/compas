import compas

if not compas.IPY:
    import pytest  # noqa: F401
    from compas.scene import context
    from compas.scene import register
    from compas.scene import Scene
    from compas.scene import SceneObject
    from compas.scene import SceneObjectNotRegisteredError
    from compas.data import Data
    from compas.geometry import Box
    from compas.geometry import Frame
    from compas.geometry import Translation
    from compas.scene import Group

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
        sceneobject = SceneObject(item, context="fake")
        assert isinstance(sceneobject, FakeSceneObject)

        item = FakeSubItem()
        sceneobject = SceneObject(item, context="fake")
        assert isinstance(sceneobject, FakeSubSceneObject)

    def test_get_sceneobject_cls_with_out_of_order_registration():
        register(FakeSubItem, FakeSubSceneObject, context="fake")
        register(FakeItem, FakeSceneObject, context="fake")
        item = FakeItem()
        sceneobject = SceneObject(item, context="fake")
        assert isinstance(sceneobject, FakeSceneObject)

        item = FakeSubItem()
        sceneobject = SceneObject(item, context="fake")
        assert isinstance(sceneobject, FakeSubSceneObject)

        def test_sceneobject_auto_context_discovery(mocker):
            register_fake_context()

            item = FakeItem()
            sceneobject = SceneObject(item)

            assert isinstance(sceneobject, FakeSceneObject)

        def test_sceneobject_auto_context_discovery_no_context(mocker):
            mocker.patch("compas.scene.context.compas.is_grasshopper", return_value=False)
            mocker.patch("compas.scene.context.compas.is_rhino", return_value=False)

            with pytest.raises(SceneObjectNotRegisteredError):
                item = FakeSubItem()
                _ = SceneObject(item)

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

    def test_group_creation():
        scene = Scene()
        group = scene.add_group("TestGroup")
        assert isinstance(group, Group)
        assert group.name == "TestGroup"
        assert group.parent == scene.root

    def test_group_add_item():
        scene = Scene()
        group = scene.add_group("TestGroup")
        box = Box()
        box_obj = group.add(box)
        assert isinstance(box_obj, SceneObject)
        assert box_obj.parent is group
        assert box_obj.item is box

    def test_group_add_from_list():
        scene = Scene()
        group = scene.add_group("TestGroup")
        boxes = [Box() for _ in range(3)]
        box_objs = group.add_from_list(boxes)
        assert len(box_objs) == 3
        for box_obj in box_objs:
            assert isinstance(box_obj, SceneObject)
            assert box_obj.parent is group

    def test_group_kwargs_inheritance():
        scene = Scene()
        group = scene.add_group("TestGroup", show=False)
        box = Box()
        box_obj = group.add(box)
        assert not box_obj.show  # Should inherit show=False from group

    def test_group_hierarchy():
        scene = Scene()
        parent_group = scene.add_group("ParentGroup")
        child_group = parent_group.add(Group("ChildGroup"))
        box = Box()
        box_obj = child_group.add(box)

        assert box_obj.parent is child_group
        assert child_group.parent is parent_group
        assert parent_group.parent is scene.root
