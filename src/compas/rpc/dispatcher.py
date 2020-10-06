from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import importlib
import json
import pstats
import sys
import traceback

from compas.utilities import DataDecoder
from compas.utilities import DataEncoder

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


__all__ = ['Dispatcher']


class Dispatcher(object):
    """Base class for remote services.

    Examples
    --------
    >>>

    Notes
    -----
    This object is used to dispatch API calls to the corresponding functions or methods.
    Since it is run on the server side, all errors are intercepted and their
    message strings assigned to the `'error'` key of the output dictionary
    such that the errors can be rethrown on the client side.

    """
    def on_module_imported(self, module, newly_loaded_modules):
        """Event triggered when a module is successfully imported.

        Override this method when subclassing in order to handle the what happens
        after a module has been imported.
        """
        pass

    def _dispatch(self, name, args):
        """Dispatcher method for XMLRPC API calls.

        This method is automatically called by the XMLRPC server if an instance
        of the dispatcher is registered with the server and the API call dies not
        correspond to a method of the server itself, or of an explicilty registered
        function.

        Parameters
        ----------
        name : str
            Name of the function.
        args : list
            List of positional arguments.
            The first argument in the list should be the JSON serialised string
            representation of the input dictionary. The structure of the input
            dictionary is defined by the caller.

        Returns
        -------
        str
            A JSON serialised string representation of the output dictionary.
            The output dicmtionary has the following structure:

            * `'data'`    : The returned result of the function call.
            * `'error'`   : The error message of any error that may have been thrown in the processes of dispatching to or execution of the API function.
            * `'profile'` : A profile of the function execution.

        """
        odict = {
            'data': None,
            'error': None,
            'profile': None
        }

        parts = name.split('.')

        functionname = parts[-1]

        try:
            if len(parts) > 1:
                modulename = ".".join(parts[:-1])

                modules_before_import = set(sys.modules.keys())

                # Trigger import
                module = importlib.import_module(modulename)

                newly_loaded_modules = set(sys.modules.keys()) - modules_before_import
                self.on_module_imported(module, newly_loaded_modules)
            else:
                module = self
        except Exception:
            odict['error'] = traceback.format_exc()

        else:
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
        """Method that handles the actual call to the function corresponding to the API call.

        Parameters
        ----------
        function : callable
            The callable object corresponding to the requested API call.
        idict : dict
            The input dictionary.
        odict : dict
            The output dictionary.

        Notes
        -----
        The output dictionary will be modified in place.

        """
        args = idict['args']
        kwargs = idict['kwargs']

        try:
            data = function(*args, **kwargs)
        except Exception:
            odict['error'] = traceback.format_exc()
        else:
            odict['data'] = data

    def _call_wrapped(self, function, idict, odict):
        """Does the same as _call, but with profiling enabled.
        """
        args = idict['args']
        kwargs = idict['kwargs']

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

        except Exception:
            odict['error'] = traceback.format_exc()
        else:
            odict['data'] = data
            odict['profile'] = stream.getvalue()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
