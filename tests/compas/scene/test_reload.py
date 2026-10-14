import compas

if not compas.IPY:
    import pytest
    from compas.plugins import plugin_manager
    from compas.scene import SceneObjectNotRegisteredError
    from compas.scene import get_sceneobject_cls
    from compas_rhino.devtools import DevTools

    PACKAGE = """
from compas.data import Data
from compas.plugins import plugin
from compas.scene import SceneObject
from compas.scene import register

__all_plugins__ = ["compas_reloadable"]


class Thing(Data):
    pass


class ThingObject(SceneObject):
    def draw(self):
        pass


@plugin(category="factories")
def register_scene_objects():
    register(Thing, ThingObject, context="reloadable")
"""

    @pytest.fixture
    def reloadable(tmp_path, monkeypatch):
        """Importer of a plugin package which is discoverable for the duration of the test."""
        (tmp_path / "compas_reloadable").mkdir()
        (tmp_path / "compas_reloadable" / "__init__.py").write_text(PACKAGE)
        monkeypatch.syspath_prepend(str(tmp_path))
        plugin_manager.reset()

        def import_package():
            import compas_reloadable

            return compas_reloadable

        yield import_package

        DevTools.unload_modules("compas_reloadable")

    def test_unload_modules_rediscovers_scene_objects(reloadable):
        package = reloadable()
        assert get_sceneobject_cls(package.Thing(), context="reloadable") is package.ThingObject

        DevTools.unload_modules("compas_reloadable")
        package = reloadable()
        assert get_sceneobject_cls(package.Thing(), context="reloadable") is package.ThingObject

    def test_stale_item_is_reported(reloadable):
        stale_thing = reloadable().Thing()

        DevTools.unload_modules("compas_reloadable")
        reloadable()

        with pytest.raises(SceneObjectNotRegisteredError, match="instance of a stale definition"):
            get_sceneobject_cls(stale_thing, context="reloadable")
