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
            mocker.patch("compas.scene.context.compas.is_grasshopper", return_value=False)
            mocker.patch("compas.scene.context.compas.is_rhino", return_value=False)

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
