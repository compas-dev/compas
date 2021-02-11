from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import functools
import pstats

try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

try:
    import cProfile as Profile
except ImportError:
    import profile as Profile


__all__ = [
    'abstractstaticmethod',
    'abstractclassmethod',
    'memoize',
    'print_profile',
    'observable',
    'add_observer',
    'remove_observer',
]


class abstractstaticmethod(staticmethod):
    """Decorator for declaring a static method abstract.

    Parameters
    ----------
    function : callable
        The method to declare abstract static.
    """

    __slots__ = ()

    __isabstractmethod__ = True

    def __init__(self, function):
        function.__isabstractmethod__ = True
        super(abstractstaticmethod, self).__init__(function)

class abstractclassmethod(classmethod):
    """Decorator for declaring a class method abstract.

    Parameters
    ----------
    function : callable
        The class method to declare abstract.
    """

    __slots__ = ()

    __isabstractmethod__ = True

    def __init__(self, function):
        function.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(function)


def memoize(func, *args, **kwargs):
    """Decorator to wrap a function with a memoizing callable.

    Parameters
    ----------
    func : callable
        The function that should be memoized.

    Returns
    -------
    memoized_func : callable
        A wrapper for the original function that returns a previously
        computed and cached result when possible.
    """
    cache = func.cache = {}

    @functools.wraps(func)
    def memoized_func(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return memoized_func


def print_profile(func):
    """Decorate a function with automatic profile printing.

    Parameters
    ----------
    func : callable
        The function to decorate.

    Returns
    -------
    callable
        The decorated function.

    Examples
    --------
    .. code-block:: python

        @print_profile
        def f(n):
            return sum(for i in range(n))

        print(f(100))
        print(f.__doc__)
        print(f.__name__)

    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        profile = Profile.Profile()
        profile.enable()
        #
        res = func(*args, **kwargs)
        #
        profile.disable()
        stream = StringIO()
        stats = pstats.Stats(profile, stream=stream)
        stats.strip_dirs()
        stats.sort_stats(1)
        stats.print_stats(20)
        print(stream.getvalue())
        #
        return res
    return wrapper


def _get_event_key(event_source, event_name):
    return '/{}/{}'.format(event_source.__class__.__name__, event_name)


def observable(observable_method=None, event_name=None, *args, **kwargs):
    """Decorator to mark a property or method of a class as observable.

    Observable methods/properties send notifications (events) that
    other code can listen to and act when they are triggered. This
    is useful to decouple classes where a class B depends on events
    occurring on class A, but class A should not be in charge of
    actively track and update class B on those events.

    Notes
    -----
    This decorator should only be applied to methods and properties
    of a class, not to stand-alone functions.

    Examples
    --------
    >>> class Test(object):
    ...   @observable(event_name='init')
    ...   def init(self):
    ...      print('init')
    ...
    >>> def init_observer(ctx):
    ...   print('inside observer')
    ...
    >>> t = Test()
    >>> t.init()
    init
    >>> add_observer(t, 'init', init_observer)
    >>> t.init()
    init
    inside observer
    >>> remove_observer(t, 'init', init_observer)
    >>> t.init()
    init

    Parameters
    ----------
    observable_method
        The method that is to be declared observable.
    event_name : [type], optional
        The name of the event that will be triggered when the method/property is invoked.
    """
    def observable_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _self = args[0] if len(args) else None
            if not _self:
                raise Exception('Cannot make an observable without a containing class')

            event_observers = None
            event_key = _get_event_key(_self, event_name)

            if hasattr(_self, '__event_observers__'):
                event_observers = _self.__event_observers__.get(event_key)

            return_value = func(*args, **kwargs)

            if event_observers:
                for observer in event_observers:
                    ctx = EventContext(event_name, *args, **kwargs)
                    observer(ctx)

            return return_value
        return wrapper
    if observable_method is None:
        return observable_decorator
    else:
        return observable_decorator(observable_method)


def add_observer(event_source, event_name, callback):
    """Add an observer to an event in a class containing observable methods/properties.

    Parameters
    ----------
    event_source
        Object containing ``@observable`` instances.
    event_name : str
        Name of the event to listen to.
    callback : function
        Function to execute every time the specified event is fired.
    """
    if not hasattr(event_source, '__event_observers__'):
        event_source.__event_observers__ = {}

    event_key = _get_event_key(event_source, event_name)
    observers = event_source.__event_observers__.get(event_key, set())
    observers.add(callback)

    event_source.__event_observers__[event_key] = observers


def remove_observer(event_source, event_name, callback):
    """Remove an observer from an event in a class containing observable methods/properties.

    Parameters
    ----------
    event_source
        Object containing ``@observable`` instances.
    event_name : str
        Name of the event to listen to.
    callback : function
        Function to execute every time the specified event is fired.
    """
    if not hasattr(event_source, '__event_observers__'):
        return

    event_key = _get_event_key(event_source, event_name)
    event_observers = event_source.__event_observers__.get(event_key)

    if event_observers:
        event_observers.remove(callback)
    if not event_observers:
        del event_source.__event_observers__[event_key]


class EventContext(object):
    """Provides context for the observers of an event."""
    def __init__(self, event_name, *args, **kwargs):
        self.event_name = event_name
        self.args = args
        self.kwargs = kwargs
