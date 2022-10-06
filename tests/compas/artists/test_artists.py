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
