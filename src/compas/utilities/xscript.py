from __future__ import print_function

import os
import json

try:
    from subprocess import Popen
    from subprocess import PIPE
except ImportError:
    pass


__all__ = [
    'ScriptServer'
]


# def wrap(f):
#     import sys
#     import json
#     import cStringIO
#     import cProfile
#     import pstats
#     import traceback
#     ipath = sys.argv[1]
#     opath = sys.argv[2]
#     with open(ipath, 'rb') as f:
#         idict = json.load(f)
#     try:
#         profile = cProfile.Profile()
#         profile.enable()
#         # ----------------------------------------------------------------------
#         # profiler enabled
#         # ----------------------------------------------------------------------
#         data = f(idict)
#         # ----------------------------------------------------------------------
#         # profiler disabled
#         # ----------------------------------------------------------------------
#         profile.disable()
#         stream = cStringIO.StringIO()
#         stats  = pstats.Stats(profile, stream=stream)
#         stats.strip_dirs()
#         stats.sort_stats(1)
#         stats.print_stats(20)
#         odict = {}
#         odict['data']       = data
#         odict['error']      = None
#         odict['profile']    = stream.getvalue()
#         odict['iterations'] = None
#     except Exception:
#         odict = {}
#         odict['data']       = None
#         odict['error']      = traceback.format_exc()
#         odict['profile']    = None
#         odict['iterations'] = None
#     with open(opath, 'wb+') as f:
#         json.dump(odict, f)


class ScriptServerError(Exception):
    pass


class ScriptServer(object):
    """"""
    def __init__(self, scriptdir=None, tempdir=None, python=None):
        self.scriptdir = scriptdir
        self.tempdir = tempdir
        self.python = python or 'pythonw'
        self.funcname = None
        self.script = None
        self.ipath = None
        self.opath = None
        self.error = None
        self.profile = None
        self.data = None
        self.iterations = None
        self.waitfunc = None
        self.updatefunc = None
        self.updateconduit = None

    def reset(self):
        self.error = None
        self.profile = None
        self.data = None
        self.iterations = None

    def __getattr__(self, funcname):
        self.reset()
        self.prefunc(funcname)
        return self.func

    def prefunc(self, funcname):
        self.funcname = funcname
        self.script = os.path.join(self.scriptdir, '%s.py' % self.funcname)
        if not os.path.isfile(self.script) or not os.path.exists(self.script):
            self.error = 'The script does not exist: %s' % self.script
            raise ScriptServerError(self.error)
        if not self.tempdir:
            self.tempdir = self.scriptdir
        if not os.path.isdir(self.tempdir):
            self.error = 'The tempdir does not exist: %s' % self.tempdir
            raise ScriptServerError(self.error)
        if not os.access(self.tempdir, os.W_OK | os.X_OK):
            self.error = 'The tempdir is writable: %s' % self.tempdir
            raise ScriptServerError(self.error)
        self.ipath = os.path.join(self.tempdir, '%s.in' % self.funcname)
        self.opath = os.path.join(self.tempdir, '%s.out' % self.funcname)

    def func(self, idict=None, **kwargs):
        if not idict:
            idict = {}
        idict.update(kwargs)
        with open(self.ipath, 'wb+') as fh:
            json.dump(idict, fh)
        with open(self.opath, 'wb+') as fh:
            fh.write('')
        args = [self.python, '-u', self.script, self.ipath, self.opath]
        p = Popen(args, stderr=PIPE, stdout=PIPE)
        while True:
            # combine with updatefunc?
            # into userfunc?
            if self.waitfunc:
                self.waitfunc()
            line = p.stdout.readline()
            if not line:
                break
            line = line.strip()
            print(line)
            # check if this does what it is supposed to do
            if self.updatefunc:
                self.updatefunc(self.updateconduit, line)
        _, stderr = p.communicate()
        if stderr:
            self.error = stderr
            raise ScriptServerError(stderr)
        with open(self.opath, 'rb') as fh:
            result = json.load(fh)
            if not result:
                self.error = 'No output was generated.'
                raise ScriptServerError(self.error)
            self.error = result.get('error', None)
            if self.error:
                raise ScriptServerError(self.error)
            self.data = result.get('data', None)
            self.profile = result.get('profile', '')
            self.iterations = result.get('iterations', [])
        return self.data

    def print_error(self):
        print('=' * 80)
        print('Error')
        print('-' * 80)
        print(self.error)
        print()

    def print_profile(self):
        print('=' * 80)
        print('Profile')
        print('-' * 80)
        print(self.profile)
        print()

    def print_data(self):
        print('=' * 80)
        print('Data')
        print('-' * 80)
        print(self.data)
        print()

    def print_iterations(self):
        print('=' * 80)
        print('Iterations')
        print('-' * 80)
        print(self.iterations)
        print()

    def print_output(self, title=None):
        if title:
            print('#' * 80)
            print(title)
            print()
        self.print_error()
        self.print_data()
        self.print_iterations()
        self.print_profile()


def ScriptWrapper(object):
    pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    scriptdir = '/Users/vanmelet/compAS/packages/compas_ags/_xscripts'
    tempdir = '/Users/vanmelet/compAS/packages/compas_ags/_xscripts'

    server = ScriptServer(scriptdir=scriptdir, tempdir=tempdir)

    try:

        result = server.test(n=100, pause=0.01)

    except ScriptServerError:

        server.print_error()

    else:

        print(result)
        server.print_profile()
