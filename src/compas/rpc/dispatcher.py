from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import json
import importlib

try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO
    except ImportError:
        from io import StringIO

try:
    from cProfile import Profile
except ImportError:
    from profile import Profile

import pstats
import traceback

from compas.utilities import DataEncoder
from compas.utilities import DataDecoder


__all__ = ['Dispatcher']


class Dispatcher(object):
    """Base class for remote services.

    Notes
    -----
    ...

    """

    def _dispatch(self, name, args):
        odict = {
            'data'    : None,
            'error'   : None,
            'profile' : None
        }

        parts = name.split('.')

        functionname = parts[-1]

        if len(parts) > 1:
            modulename = ".".join(parts[:-1])
            module = importlib.import_module(modulename)
        else:
            module = self

        try:
            function = getattr(module, functionname)
        except AttributeError:
            odict['error'] = "This function is not part of the API: {0}".format(functionname)
        else:
            try:
                idict = json.loads(args[0], cls=DataDecoder)
            except (IndexError, TypeError):
                odict['error'] = (
                    "API methods require a single JSON encoded dictionary as input.\n"
                    "For example: input = json.dumps({'param_1': 1, 'param_2': [2, 3]})")
            else:
                self._call_wrapped(function, idict, odict)

        return json.dumps(odict, cls=DataEncoder)

    def _call(self, function, idict, odict):
        args = idict['args']
        kwargs = idict['kwargs']

        try:
            data = function(*args, **kwargs)
        except:
            odict['error'] = traceback.format_exc()
        else:
            odict['data'] = data

    def _call_wrapped(self, function, idict, odict):
        args = idict['args']
        kwargs = odict['kwargs']

        try:
            profile = Profile()
            profile.enable()

            data = function(*args, **kwargs)

            profile.disable()
            stream = StringIO()
            stats = pstats.Stats(profile, stream=stream)
            stats.strip_dirs()
            stats.sort_stats(1)
            stats.print_stats(20)
        except:
            odict['error'] = traceback.format_exc()
        else:
            odict['data']    = data
            odict['profile'] = stream.getvalue()


# def list_methods_wrapper(dispatcher):
#     def list_methods():
#         def is_public_method(member):
#             return inspect.ismethod(member) and not member.__name__.startswith('_')
#         members = inspect.getmembers(dispatcher, is_public_method)
#         return [member[0] for member in members]
#     return list_methods


# def method_help_wrapper(dispatcher):
#     def method_help(name):
#         if not hasattr(dispatcher, name):
#             return 'Not a registered API method: {0}'.format(name)
#         method = getattr(dispatcher, name)
#         return inspect.getdoc(method)
#     return method_help


# def method_signature_wrapper(dispatcher):
#     def method_signature(name):
#         if not hasattr(dispatcher, name):
#             return 'Not a registered API method: {0}'.format(name)
#         method = getattr(dispatcher, name)
#         spec = inspect.getargspec(method)
#         args = spec.args
#         defaults = spec.defaults
#         return args[1:], defaults
#     return method_signature


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
