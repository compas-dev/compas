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
    import cProfile as Profile
except ImportError:
    import profile as Profile

import pstats
import traceback

from compas.utilities import DataEncoder
from compas.utilities import DataDecoder


__all__ = ['Service']


class Service(object):
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
                self._call(function, idict, odict)

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

    def _call_wrapped(self, method, idict, odict):
        args = idict['args']
        kwargs = odict['kwargs']

        try:
            profile = cProfile.Profile()
            profile.enable()

            data = function(*args, **kwargs)

            profile.disable()
            stream = cStringIO.StringIO()
            stats = pstats.Stats(profile, stream=stream)
            stats.strip_dirs()
            stats.sort_stats(1)
            stats.print_stats(20)
        except:
            odict['error'] = traceback.format_exc()
        else:
            odict['data']    = data
            odict['profile'] = stream.getvalue()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
