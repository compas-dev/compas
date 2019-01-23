from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys
import time
import threading


__all__ = [
    'await_callback',
]

class ThreadExceptHookHandler(object):
    """Workaround to deal with a bug in the Python interpreter (!).

    Report: http://bugs.python.org/issue1230540
    Discussion: https://stackoverflow.com/a/31622038/269335
    PR (not yet merged): https://github.com/python/cpython/pull/8610
    Disclaimer (!): https://news.ycombinator.com/item?id=11090814
    """
    def __enter__(self):
        original_init = threading.Thread.__init__

        def init(self, *args, **kwargs):

            original_init(self, *args, **kwargs)
            original_run = self.run

            def run_with_except_hook(*args2, **kwargs2):
                try:
                    original_run(*args2, **kwargs2)
                except Exception:
                    sys.excepthook(*sys.exc_info())

            self.run = run_with_except_hook

        self._original_init = original_init
        threading.Thread.__init__ = init

        return self

    def __exit__(self, *args):
        threading.Thread.__init__ = self._original_init


def await_callback(async_func, callback_name='callback', errback_name=None, *args, **kwargs):
    """Wait for the completion of an asynchronous code that uses callbacks to signal completion.

    This helper function turns an async function into a synchronous one,
    waiting for its completion before moving forward (without doing a busy wait).

    It is useful to minimize "callback hell" when more advanced options
    like ``asyncio`` are not available.

    Parameters
    ----------
    async_func : callable
        An asynchronous function that receives at least one callback parameter
        to signal completion.
    callback_name : string, optional
        Name of the callback parameter of ``async_func``.
        Default is `callback`.
    errback_name : string, optional
        Name of the error handling callback parameter of ``async_func``.
        Default is None.

    Notes
    -----

    Exceptions thrown during the async execution are handled and re-thrown as normal
    exceptions, even if they were raised on a different thread.

    Examples
    --------

    The following example shows how to await an async function (``do_sync_stuff` in
    the example), using this utility:

    .. code-block:: python

        from compas.utilities import await_callback

        def do_async_stuff(callback):
            from threading import Thread

            def runner(cb):
                print('doing async stuff')
                # ..
                cb('done')

            Thread(target=runner, args=(callback, )).start()

        result = await_callback(do_async_stuff)

    """
    wait_event = threading.Event()
    call_results = {}
    def inner_callback(*args, **kwargs):
        try:
            call_results['args'] = args
            call_results['kwargs'] = kwargs
            wait_event.set()
        except Exception as e:
            call_results['exception'] = e
            wait_event.set()

    kwargs['callback'] = inner_callback
    if errback_name:
        def inner_errback(error):
            if isinstance(error, Exception):
                call_results['exception'] = error
            else:
                call_results['exception'] = Exception(str(error))
            wait_event.set()

        kwargs[errback_name] = inner_errback

    def unhandled_exception_handler(type, value, traceback):
        call_results['exception'] = value
        wait_event.set()

    try:
        # Install unhanlded exception handler
        sys.excepthook = unhandled_exception_handler

        # Invoke async method and wait
        with ThreadExceptHookHandler():
            async_func(*args, **kwargs)
            wait_event.wait()
    finally:
        # Restore built-in unhanled exception handler
        sys.excepthook = sys.__excepthook__

    if 'exception' in call_results:
        raise call_results['exception']

    return_value = call_results['args']
    dict_values = call_results['kwargs']

    if not dict_values:
        # If nothing, then None
        if len(return_value) == 0:
            return None
        # If it's a one-item tuple,
        # un-wrap from it and return that element
        elif len(return_value) == 1:
            return return_value[0]
        else:
            return return_value

    if not return_value:
        return dict_values

    return return_value + (dict_values,)



# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    def do_async_stuff(callback):
        from threading import Thread

        def runner(cb):
            print('doing async stuff')
            # ..
            cb('done')

        Thread(target=runner, args=(callback, )).start()

    result = await_callback(do_async_stuff)
    print(result)
