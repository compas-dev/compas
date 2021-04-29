from compas.utilities import memoize


def test_memoize():
    ctx = dict(calls=0)

    @memoize
    def func(arg):
        ctx['calls'] += 1

    func(444)
    func(444)
    func(444)
    assert ctx['calls'] == 1

    func(555)
    assert ctx['calls'] == 2
