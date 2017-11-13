from __future__ import print_function

import os
import json
import time
import inspect

try:
    from subprocess import Popen
    from subprocess import PIPE
except ImportError:
    pass

from functools import wraps


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['XFunc']


WRAPPER = """
import os
import sys
import importlib

import json
try:
    import cStringIO
except:
    import io
import cProfile
import pstats
import traceback

basedir  = sys.argv[1]
funcname = sys.argv[2]
ipath    = sys.argv[3]
opath    = sys.argv[4]

with open(ipath, 'r') as fp:
    idict = json.load(fp)

try:
    args   = idict['args']
    kwargs = idict['kwargs']

    profile = cProfile.Profile()
    profile.enable()

    sys.path.insert(0, basedir)
    parts = funcname.split('.')

    if len(parts) > 1:
        mname = '.'.join(parts[:-1])
        fname = parts[-1]
        m = importlib.import_module(mname)
        f = getattr(m, fname)
    else:
        raise Exception('Cannot import the function because no module name is specified.')
        # mname = os.path.splitext(os.path.basename(os.path.abspath(basedir)))[0]
        # fname = parts[0]
        # print mname
        # m = importlib.import_module(mname)
        # f = getattr(m, fname)

    r = f(*args, **kwargs)

    profile.disable()

    try:
        stream = cStringIO.StringIO()
    except:
        stream = io.StringIO()
    stats  = pstats.Stats(profile, stream=stream)
    stats.strip_dirs()
    stats.sort_stats(1)
    stats.print_stats(20)

except:
    odict = {}
    odict['error']      = traceback.format_exc()
    odict['data']       = None
    odict['iterations'] = None
    odict['profile']    = None

else:
    odict = {}
    odict['error']      = None
    odict['data']       = r
    odict['iterations'] = None
    odict['profile']    = stream.getvalue()

with open(opath, 'w+') as fp:
    json.dump(odict, fp)
"""


# def xfuncify(tmpdir='.', delete_files=True, mode=1):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             # print(func.__name__)
#             # print(func.__module__)
#             # print(inspect.getmodule(func))
#             # print(__file__)
#             # print(os.path.splitext(os.path.basename(__file__)))
#             modname = os.path.splitext(os.path.basename(__file__))[0]
#             funcname = modname + '.' + func.__name__
#             print(funcname)
#             return _xecute(funcname,
#                            '.',
#                            tmpdir,
#                            delete_files,
#                            mode,
#                            *args,
#                            **kwargs)
#         return wrapper
#     return decorator


def test_xfunc(numiter=100, pause=0.1):
    for k in range(numiter):
        print(k)
        time.sleep(pause)
    return 'test_xfunc_finished'


def _xecute(funcname, basedir, tmpdir, delete_files, mode, callback, callback_args,
            *args, **kwargs):
    """Execute a function with optional positional and named arguments.

    Parameters:
        funcname (str): The full name of the function.
        basedir (str):
            A directory that should be added to the PYTHONPATH such that the function can be found.
        tmpdir (str):
            A directory that should be used for storing the IO files.
        delete_files (bool):
            Set to ``False`` if the IO files should not be deleted afterwards.
        mode (int):
            The printing mode.
        args (list):
            Optional.
            Positional arguments to be passed to the function.
            Default is ``[]``.
        kwargs (dict):
            Optional.
            Named arguments to be passed to the function.
            Default is ``{}``.

    """

    if callback:
        if not callable(callback):
            callback = None

    if not os.path.isdir(basedir):
        raise Exception('basedir is not a directory: %s' % basedir)

    if not os.path.isdir(tmpdir):
        raise Exception('tmpdir is not a directory: %s' % tmpdir)

    if not os.access(tmpdir, os.W_OK):
        raise Exception('you do not have write access to tmpdir')

    basedir = os.path.abspath(basedir)
    tmpdir = os.path.abspath(tmpdir)

    ipath = os.path.join(tmpdir, '%s.in' % funcname)
    opath = os.path.join(tmpdir, '%s.out' % funcname)

    idict = {'args': args, 'kwargs': kwargs}

    with open(ipath, 'w+') as fh:
        json.dump(idict, fh)

    with open(opath, 'w+') as fh:
        fh.write('')

    process_args = ['pythonw', '-u', '-c', WRAPPER, basedir, funcname, ipath, opath]
    print(basedir, funcname, ipath, opath)
    process = Popen(process_args, stderr=PIPE, stdout=PIPE)

    # while process.poll() is None:
    while True:
        if callback:
            callback(callback_args)

        line = process.stdout.readline().strip()

        if not line:
            break
        if mode:
            print(line)

    _, stderr = process.communicate()

    if stderr:
        odict = {'error'     : stderr,
                 'data'      : None,
                 'iterations': None,
                 'profile'   : None}
    else:
        with open(opath, 'r') as fh:
            odict = json.load(fh)

    if delete_files:
        try:
            os.remove(ipath)
        except OSError:
            pass
        try:
            os.remove(opath)
        except OSError:
            pass

    return odict


class XFunc(object):
    """"""

    def __init__(self, funcname=None, basedir='.', tmpdir='.', delete_files=True,
                 mode=1, callback=None, callback_args=None):
        self._basedir      = None
        self._tmpdir       = None
        self.funcname      = funcname
        self.basedir       = basedir
        self.tmpdir        = tmpdir
        self.delete_files  = delete_files
        self.mode          = mode
        self.callback      = callback
        self.callback_args = callback_args
        self.python        = 'pythonw'
        self.data          = None
        self.iterations    = None
        self.profile       = None
        self.error         = None

    @property
    def basedir(self):
        return self._basedir

    @basedir.setter
    def basedir(self, basedir):
        if not os.path.isdir(basedir):
            raise Exception('basedir is not a directory: %s' % basedir)
        self._basedir = os.path.abspath(basedir)

    @property
    def tmpdir(self):
        return self._tmpdir

    @tmpdir.setter
    def tmpdir(self, tmpdir):
        if not os.path.isdir(tmpdir):
            raise Exception('tmpdir is not a directory: %s' % tmpdir)
        if not os.access(tmpdir, os.W_OK):
            raise Exception('you do not have write access to tmpdir')
        self._tmpdir = os.path.abspath(tmpdir)

    def __call__(self, *args, **kwargs):
        funcname = self.funcname
        odict = _xecute(funcname,
                        self.basedir,
                        self.tmpdir,
                        self.delete_files,
                        self.mode,
                        self.callback,
                        self.callback_args,
                        *args,
                        **kwargs)

        self.data       = odict['data']
        self.profile    = odict['profile']
        self.iterations = odict['iterations']
        self.error      = odict['error']

        return odict


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    test_xfunc = XFunc('xfunc.test_xfunc', mode=1)

    res = test_xfunc(numiter=10, pause=0.5)

    print(res['error'])
    print(res['profile'])
    print(res['iterations'])
    print(res['data'])
