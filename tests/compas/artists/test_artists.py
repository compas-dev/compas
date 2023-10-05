import pytest  # noqa: F401

import compas
from compas.artists import Artist
from compas.artists.artist import NoArtistContextError


if not compas.IPY:

    @pytest.fixture(autouse=True)
    def reset_artists():
        # before each test
        yield
        # after each test, reset artists
        Artist.ITEM_ARTIST.clear()
        Artist._Artist__ARTISTS_REGISTERED = False  # type: ignore


def register_fake_context():
    Artist.register(FakeItem, FakeArtist, context="fake")


class FakeArtist(Artist):
    def draw(self):
        pass


class FakeSubArtist(Artist):
    def draw(self):
        pass


class FakeItem(object):
    pass


class FakeSubItem(FakeItem):
    pass


def test_get_artist_cls_with_orderly_registration():
    Artist.register(FakeItem, FakeArtist, context="fake")
    Artist.register(FakeSubItem, FakeSubArtist, context="fake")
    item = FakeItem()
    artist = Artist(item, context="fake")
    assert isinstance(artist, FakeArtist)

    item = FakeSubItem()
    artist = Artist(item, context="fake")
    assert isinstance(artist, FakeSubArtist)


def test_get_artist_cls_with_out_of_order_registration():
    Artist.register(FakeSubItem, FakeSubArtist, context="fake")
    Artist.register(FakeItem, FakeArtist, context="fake")
    item = FakeItem()
    artist = Artist(item, context="fake")
    assert isinstance(artist, FakeArtist)

    item = FakeSubItem()
    artist = Artist(item, context="fake")
    assert isinstance(artist, FakeSubArtist)


if not compas.IPY:

    def test_artist_auto_context_discovery(mocker):
        mocker.patch("compas.artists.Artist.register_artists")
        Artist.register_artists.side_effect = register_fake_context
        Artist._Artist__ARTISTS_REGISTERED = False  # type: ignore

        item = FakeItem()
        artist = Artist(item)

        assert isinstance(artist, FakeArtist)

    def test_artist_auto_context_discovery_viewer(mocker):
        mocker.patch("compas.artists.artist.is_viewer_open", return_value=True)
        Artist.ITEM_ARTIST["Viewer"] = {FakeItem: FakeArtist}

        item = FakeSubItem()
        artist = Artist(item)

        assert isinstance(artist, FakeArtist)

    def test_artist_auto_context_discovery_viewer_priority(mocker):
        mocker.patch("compas.artists.artist.is_viewer_open", return_value=True)

        class FakeViewerArtist(FakeArtist):
            pass

        class FakePlotterArtist(FakeArtist):
            pass

        Artist.ITEM_ARTIST["Viewer"] = {FakeItem: FakeViewerArtist}
        Artist.ITEM_ARTIST["Plotter"] = {FakeItem: FakePlotterArtist}

        item = FakeSubItem()
        artist = Artist(item)

        assert isinstance(artist, FakeViewerArtist)

    def test_artist_auto_context_discovery_no_context(mocker):
        mocker.patch("compas.artists.artist.is_viewer_open", return_value=False)
        mocker.patch("compas.artists.artist.compas.is_grasshopper", return_value=False)
        mocker.patch("compas.artists.artist.compas.is_rhino", return_value=False)

        with pytest.raises(NoArtistContextError):
            item = FakeSubItem()
            _ = Artist(item)
