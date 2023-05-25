import pytest  # noqa: F401

import compas
from compas.artists import Artist


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
        mocker.patch("compas.artists.artist.register_artists")
        compas.artists.artist.register_artists.side_effect = register_fake_context

        item = FakeItem()
        artist = Artist(item)

        assert Artist.CONTEXT == "fake"
        assert isinstance(artist, FakeArtist)

    def register_fake_context():
        Artist.register(FakeItem, FakeArtist, context="fake")
        return ["fake"]
