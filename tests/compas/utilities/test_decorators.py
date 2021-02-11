from compas.utilities import add_observer
from compas.utilities import memoize
from compas.utilities import observable
from compas.utilities import remove_observer

import pytest


def test_memoize():
    ctx = dict(calls=0)

    @memoize
    def func(arg):
        ctx['calls'] += 1
        return arg + 1

    assert func(444) == 445
    assert func(444) == 445
    assert func(444) == 445
    assert ctx['calls'] == 1

    assert func(555) == 556
    assert ctx['calls'] == 2


@pytest.fixture
def observable_instance():
    class ObservableObject(object):
        @observable(event_name='increment')
        def increment(self):
            self.value += 1

        @property
        @observable(event_name='get_prop')
        def prop(self):
            return self.value

        @prop.setter
        @observable(event_name='set_prop')
        def prop(self, value):
            self.value = value

    return ObservableObject()


def test_observable_on_methods(observable_instance):
    t = observable_instance
    t.value = 0
    t.increment()

    assert t.value == 1

    def handler(ctx):
        t.value *= 10

    add_observer(t, 'increment', handler)
    t.increment()
    assert t.value == 20

    remove_observer(t, 'increment', handler)
    t.increment()
    assert t.value == 21


def test_observable_on_property_getter(observable_instance):
    c = dict()
    t = observable_instance
    t.value = 10

    assert t.prop == 10

    def handler(ctx):
        c['was_called'] = True

    c['was_called'] = False
    add_observer(t, 'get_prop', handler)
    assert t.prop == 10
    assert c['was_called'] == True

    c['was_called'] = False
    remove_observer(t, 'get_prop', handler)
    assert t.prop == 10
    assert c['was_called'] == False


def test_observable_on_property_setter(observable_instance):
    c = dict()
    t = observable_instance

    def handler(ctx):
        c['was_called'] = True

    c['was_called'] = False
    add_observer(t, 'set_prop', handler)
    t.prop = 20
    assert t.prop == 20
    assert c['was_called'] == True
