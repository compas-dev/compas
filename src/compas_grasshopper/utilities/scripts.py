import os
import json

try:
    from System.Diagnostics import Process
except ImportError as e:
    import platform
    if platform.system() == 'Windows':
        raise e


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = [
    'ScriptServer',
]


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
        # args = [self.python, '-u', self.script, self.ipath, self.opath]
        p = Process()
        p.StartInfo.UseShellExecute = False
        p.StartInfo.RedirectStandardOutput = True
        p.StartInfo.RedirectStandardError = True
        p.StartInfo.FileName = self.python
        p.StartInfo.Arguments = '-u {0} {1} {2}'.format(self.script, self.ipath, self.opath)
        p.Start()
        p.WaitForExit()
        while True:
            # combine with updatefunc?
            # into userfunc?
            if self.waitfunc:
                self.waitfunc()
            line = p.StandardOutput.ReadLine()
            if not line:
                break
            line = line.strip()
            print line
            # check if this does what it is supposed to do
            if self.updatefunc:
                self.updatefunc(self.updateconduit, line)
        stderr = p.StandardError.ReadToEnd()
        if stderr:
            self.error = stderr
            raise ScriptServerError(stderr)
        print p.StandardOutput.ReadToEnd()
        print p.ExitCode
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
        print '=' * 80
        print 'Error'
        print '-' * 80
        print self.error
        print

    def print_profile(self):
        print '=' * 80
        print 'Profile'
        print '-' * 80
        print self.profile
        print

    def print_data(self):
        print '=' * 80
        print 'Data'
        print '-' * 80
        print self.data
        print

    def print_iterations(self):
        print '=' * 80
        print 'Iterations'
        print '-' * 80
        print self.iterations
        print

    def print_output(self, title=None):
        if title:
            print '#' * 80
            print title
            print
        self.print_error()
        self.print_data()
        self.print_iterations()
        self.print_profile()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == '__main__':

    server = ScriptServer('tmp', 'tmp')
    try:
        result = server.test(n=10, pause=0.1)
    except ScriptServerError:
        server.print_error()
    else:
        print result
