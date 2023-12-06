import pytest  # noqa: F401

import compas
from compas.scene import SceneObject
from compas.scene import NoSceneObjectContextError


if not compas.IPY:

    @pytest.fixture(autouse=True)
    def reset_sceneobjects():
        # before each test
        yield
        # after each test, reset scene objects
        SceneObject.ITEM_SCENEOBJECT.clear()
        SceneObject._SceneObject__SCENEOBJECTS_REGISTERED = False  # type: ignore


def register_fake_context():
    SceneObject.register(FakeItem, FakeSceneObject, context="fake")


class FakeSceneObject(SceneObject):
    def draw(self):
        pass


class FakeSubSceneObject(SceneObject):
    def draw(self):
        pass


class FakeItem(object):
    pass


class FakeSubItem(FakeItem):
    pass


def test_get_sceneobject_cls_with_orderly_registration():
    SceneObject.register(FakeItem, FakeSceneObject, context="fake")
    SceneObject.register(FakeSubItem, FakeSubSceneObject, context="fake")
    item = FakeItem()
    sceneobject = SceneObject(item, context="fake")
    assert isinstance(sceneobject, FakeSceneObject)

    item = FakeSubItem()
    sceneobject = SceneObject(item, context="fake")
    assert isinstance(sceneobject, FakeSubSceneObject)


def test_get_sceneobject_cls_with_out_of_order_registration():
    SceneObject.register(FakeSubItem, FakeSubSceneObject, context="fake")
    SceneObject.register(FakeItem, FakeSceneObject, context="fake")
    item = FakeItem()
    sceneobject = SceneObject(item, context="fake")
    assert isinstance(sceneobject, FakeSceneObject)

    item = FakeSubItem()
    sceneobject = SceneObject(item, context="fake")
    assert isinstance(sceneobject, FakeSubSceneObject)


if not compas.IPY:

    def test_sceneobject_auto_context_discovery(mocker):
        mocker.patch("compas.scene.SceneObject.register_scene_objects")
        SceneObject.register_scene_objects.side_effect = register_fake_context
        SceneObject._SceneObject__SCENEOBJECTS_REGISTERED = False  # type: ignore

        item = FakeItem()
        sceneobject = SceneObject(item)

        assert isinstance(sceneobject, FakeSceneObject)

    def test_sceneobject_auto_context_discovery_viewer(mocker):
        mocker.patch("compas.scene.sceneobject.is_viewer_open", return_value=True)
        SceneObject.ITEM_SCENEOBJECT["Viewer"] = {FakeItem: FakeSceneObject}

        item = FakeSubItem()
        sceneobject = SceneObject(item)

        assert isinstance(sceneobject, FakeSceneObject)

    def test_sceneobject_auto_context_discovery_viewer_priority(mocker):
        mocker.patch("compas.scene.sceneobject.is_viewer_open", return_value=True)

        class FakeViewerSceneObject(FakeSceneObject):
            pass

        class FakePlotterSceneObject(FakeSceneObject):
            pass

        SceneObject.ITEM_SCENEOBJECT["Viewer"] = {FakeItem: FakeViewerSceneObject}
        SceneObject.ITEM_SCENEOBJECT["Plotter"] = {FakeItem: FakePlotterSceneObject}

        item = FakeSubItem()
        sceneobject = SceneObject(item)

        assert isinstance(sceneobject, FakeViewerSceneObject)

    def test_sceneobject_auto_context_discovery_no_context(mocker):
        mocker.patch("compas.scene.sceneobject.is_viewer_open", return_value=False)
        mocker.patch("compas.scene.sceneobject.compas.is_grasshopper", return_value=False)
        mocker.patch("compas.scene.sceneobject.compas.is_rhino", return_value=False)

        with pytest.raises(NoSceneObjectContextError):
            item = FakeSubItem()
            _ = SceneObject(item)
