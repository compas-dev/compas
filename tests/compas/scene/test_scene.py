import pytest  # noqa: F401

import compas
from compas.scene import context
from compas.scene import register
from compas.scene import SceneObject
from compas.scene import SceneObjectNotRegisteredError
from compas.data import Data


if not compas.IPY:

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


if not compas.IPY:

    def test_sceneobject_auto_context_discovery(mocker):
        register_fake_context()

        item = FakeItem()
        sceneobject = SceneObject(item)

        assert isinstance(sceneobject, FakeSceneObject)

    # def test_sceneobject_auto_context_discovery_viewer(mocker):
    #     mocker.patch("compas.scene.context.is_viewer_open", return_value=True)
    #     context.ITEM_SCENEOBJECT["Viewer"] = {FakeItem: FakeSceneObject}

    #     item = FakeSubItem()
    #     sceneobject = SceneObject(item)

    #     assert isinstance(sceneobject, FakeSceneObject)

    # def test_sceneobject_auto_context_discovery_viewer_priority(mocker):
    #     mocker.patch("compas.scene.context.is_viewer_open", return_value=True)

    #     class FakeViewerSceneObject(FakeSceneObject):
    #         pass

    #     class FakePlotterSceneObject(FakeSceneObject):
    #         pass

    #     context.ITEM_SCENEOBJECT["Viewer"] = {FakeItem: FakeViewerSceneObject}
    #     context.ITEM_SCENEOBJECT["Plotter"] = {FakeItem: FakePlotterSceneObject}

    #     item = FakeSubItem()
    #     sceneobject = SceneObject(item)

    #     assert isinstance(sceneobject, FakeViewerSceneObject)

    def test_sceneobject_auto_context_discovery_no_context(mocker):
        # mocker.patch("compas.scene.context.is_viewer_open", return_value=False)
        mocker.patch("compas.scene.context.compas.is_grasshopper", return_value=False)
        mocker.patch("compas.scene.context.compas.is_rhino", return_value=False)

        with pytest.raises(SceneObjectNotRegisteredError):
            item = FakeSubItem()
            _ = SceneObject(item)
