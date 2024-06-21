import compas

if not compas.IPY:
    import pytest  # noqa: F401
    from compas.scene import context
    from compas.scene import register
    from compas.scene import SceneObject
    from compas.scene import SceneObjectNotRegisteredError
    from compas.data import Data

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
