from threading import Thread

from compas.utilities import await_callback

import pytest


def test_void_return_callback():
    def async_fn(callback):
        def runner(cb):
            cb()
        Thread(target=runner, args=(callback, )).start()

    result = await_callback(async_fn)
    assert result is None


def test_single_positional_arg_callback():
    def async_fn(callback):
        def runner(cb):
            cb('only_return_value')
        Thread(target=runner, args=(callback, )).start()

    result = await_callback(async_fn)
    assert result == 'only_return_value'


def test_many_positional_args_callback():
    def async_fn(callback):
        def runner(cb):
            cb(1, 2)
        Thread(target=runner, args=(callback, )).start()

    result = await_callback(async_fn)
    assert result == (1, 2, )


def test_kwargs_callback():
    def async_fn(callback):
        def runner(cb):
            cb(name='Austin', last_name='Powers')
        Thread(target=runner, args=(callback, )).start()

    result = await_callback(async_fn)
    assert result['name'] == 'Austin'
    assert result['last_name'] == 'Powers'


def test_one_positional_arg_and_kwargs_callback():
    def async_fn(callback):
        def runner(cb):
            cb(1, retries=5)
        Thread(target=runner, args=(callback, )).start()

    result, kwargs = await_callback(async_fn)
    assert result == 1
    assert kwargs['retries'] == 5


def test_many_positional_args_and_kwargs_callback():
    def async_fn(callback):
        def runner(cb):
            cb(4, 2, 3, retries=5)
        Thread(target=runner, args=(callback, )).start()

    a, b, c, kw = await_callback(async_fn)
    assert a == 4
    assert b == 2
    assert c == 3
    assert kw['retries'] == 5


def test_captured_exception_in_thread():
    def async_fn(callback):
        def runner(cb):
            raise ValueError('exception')

        Thread(target=runner, args=(callback, )).start()

    with pytest.raises(ValueError):
        await_callback(async_fn)
