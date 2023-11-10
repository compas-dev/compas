import pytest  # noqa: F401

import compas
from compas.scene import SceneObject
from compas.scene.sceneobject import NoArtistContextError


if not compas.IPY:

    @pytest.fixture(autouse=True)
    def reset_artists():
        # before each test
        yield
        # after each test, reset artists
        SceneObject.ITEM_ARTIST.clear()
        SceneObject._Artist__ARTISTS_REGISTERED = False  # type: ignore


def register_fake_context():
    SceneObject.register(FakeItem, FakeArtist, context="fake")


class FakeArtist(SceneObject):
    def draw(self):
        pass


class FakeSubArtist(SceneObject):
    def draw(self):
        pass


class FakeItem(object):
    pass


class FakeSubItem(FakeItem):
    pass


def test_get_artist_cls_with_orderly_registration():
    SceneObject.register(FakeItem, FakeArtist, context="fake")
    SceneObject.register(FakeSubItem, FakeSubArtist, context="fake")
    item = FakeItem()
    artist = SceneObject(item, context="fake")
    assert isinstance(artist, FakeArtist)

    item = FakeSubItem()
    artist = SceneObject(item, context="fake")
    assert isinstance(artist, FakeSubArtist)


def test_get_artist_cls_with_out_of_order_registration():
    SceneObject.register(FakeSubItem, FakeSubArtist, context="fake")
    SceneObject.register(FakeItem, FakeArtist, context="fake")
    item = FakeItem()
    artist = SceneObject(item, context="fake")
    assert isinstance(artist, FakeArtist)

    item = FakeSubItem()
    artist = SceneObject(item, context="fake")
    assert isinstance(artist, FakeSubArtist)


if not compas.IPY:

    def test_artist_auto_context_discovery(mocker):
        mocker.patch("compas.artists.Artist.register_artists")
        SceneObject.register_artists.side_effect = register_fake_context
        SceneObject._Artist__ARTISTS_REGISTERED = False  # type: ignore

        item = FakeItem()
        artist = SceneObject(item)

        assert isinstance(artist, FakeArtist)

    def test_artist_auto_context_discovery_viewer(mocker):
        mocker.patch("compas.artists.artist.is_viewer_open", return_value=True)
        SceneObject.ITEM_ARTIST["Viewer"] = {FakeItem: FakeArtist}

        item = FakeSubItem()
        artist = SceneObject(item)

        assert isinstance(artist, FakeArtist)

    def test_artist_auto_context_discovery_viewer_priority(mocker):
        mocker.patch("compas.artists.artist.is_viewer_open", return_value=True)

        class FakeViewerArtist(FakeArtist):
            pass

        class FakePlotterArtist(FakeArtist):
            pass

        SceneObject.ITEM_ARTIST["Viewer"] = {FakeItem: FakeViewerArtist}
        SceneObject.ITEM_ARTIST["Plotter"] = {FakeItem: FakePlotterArtist}

        item = FakeSubItem()
        artist = SceneObject(item)

        assert isinstance(artist, FakeViewerArtist)

    def test_artist_auto_context_discovery_no_context(mocker):
        mocker.patch("compas.artists.artist.is_viewer_open", return_value=False)
        mocker.patch("compas.artists.artist.compas.is_grasshopper", return_value=False)
        mocker.patch("compas.artists.artist.compas.is_rhino", return_value=False)

        with pytest.raises(NoArtistContextError):
            item = FakeSubItem()
            _ = SceneObject(item)
