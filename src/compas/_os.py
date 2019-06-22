# -*- coding: utf-8 -*-
"""
These are internal functions of the framework.
Not intended to be used outside compas* packages.
"""
import ctypes
import os
import subprocess
import sys

try:
    NotADirectoryError
except NameError:
    class NotADirectoryError(Exception):
        pass

PY3 = sys.version_info[0] == 3
system = sys.platform

# IronPython support (OMG)
if 'ironpython' in sys.version.lower() and os.name == 'nt':
    system = 'win32'

try:
    from compas_bootstrapper import PYTHON_DIRECTORY
except:  # noqa: E722
    # We re-map CONDA_PREFIX for backwards compatibility reasons
    # In a few releases down the line, we can get rid of this bit
    try:
        from compas_bootstrapper import CONDA_PREFIX as PYTHON_DIRECTORY
    except:  # noqa: E722
        PYTHON_DIRECTORY = None


def select_python(python_executable):
    """Selects the most likely python interpreter to run.

    This function detects if there is a conda environment we can use,
    or if we need to default to a system-wide python interpreter instead.

    Parameters
    ----------
    python_executable : str
        Select which python executable you want to use,
        either `python` or `pythonw`.
    """
    python_executable = python_executable or 'python'

    if PYTHON_DIRECTORY and os.path.exists(PYTHON_DIRECTORY):
        python = os.path.join(PYTHON_DIRECTORY, python_executable)
        if os.path.exists(python):
            return python

        python = os.path.join(PYTHON_DIRECTORY, '{0}.exe'.format(python_executable))
        if os.path.exists(python):
            return python

        python = os.path.join(PYTHON_DIRECTORY, 'bin', python_executable)
        if os.path.exists(python):
            return python

        python = os.path.join(PYTHON_DIRECTORY, 'bin', '{0}.exe'.format(python_executable))
        if os.path.exists(python):
            return python

        if python:
            return python

    # Assume a system-wide install exists
    return python_executable


def prepare_environment():
    """Prepares an environment context to run Python on.

    If Python is being used from a conda environment, this is roughly equivalent
    to activating the conda environment by setting up the correct environment
    variables.
    """
    env = os.environ.copy()

    if PYTHON_DIRECTORY:
        lib_bin = os.path.join(PYTHON_DIRECTORY, 'Library', 'bin')
        if os.path.exists(lib_bin):
            env['PATH'] += os.pathsep + lib_bin

        lib_bin = os.path.join(PYTHON_DIRECTORY, 'lib')
        if os.path.exists(lib_bin):
            env['PATH'] += os.pathsep + lib_bin

    return env


def absjoin(*parts):
    return os.path.abspath(os.path.join(*parts))


# Cache whatever symlink function works (native or polyfill)
_os_symlink = None


def _create_symlink_win_polyfill():
    def symlink_ms(source, link_name):
        _run_as_admin(['cmd.exe', '/c', 'mklink', '/D', link_name, source])

    return symlink_ms


def create_symlink(source, link_name):
    """Create a symbolic link pointing to source named link_name.

    Parameters
    ----------
    source: str
        Source of the link
    link_name: str
        Link name.

    Note
    ----
    This function is a polyfill of the native ``os.symlink``
    for Python 2.x on Windows platforms.
    """
    global _os_symlink
    enable_retry_with_polyfill = False

    if not _os_symlink:
        _os_symlink = getattr(os, 'symlink', None)

        if os.name == 'nt':
            if not callable(_os_symlink):
                _os_symlink = _create_symlink_win_polyfill()
            else:
                enable_retry_with_polyfill = True

    try:
        _os_symlink(source, link_name)
    except OSError:
        if not enable_retry_with_polyfill:
            raise

        _os_symlink = _create_symlink_win_polyfill()
        _os_symlink(source, link_name)


def remove_symlink(link):
    if os.path.isdir(link):
        try:
            os.rmdir(link)
        except NotADirectoryError:
            os.unlink(link)
    else:
        os.unlink(link)


def is_admin():
    """Determines whether the current user has admin rights.

    Returns
    -------
    bool
        True if the user is administrator, otherwise False.
    """
    if os.name != 'nt':
        return os.getuid() == 0

    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except:  # noqa: E722
        return False

# PShellExecuteInfo = POINTER(ShellExecuteInfo)


def _run_as_admin(command):
    """Run the specified command as an admin.

    Paramters
    ---------
    command : list
        List of strings of the command to run.

    Returns
    -------
    int
        Exit code of the process.
    """

    if os.name != 'nt':
        raise RuntimeError('Only supported on Windows')

    class ShellExecuteInfo(ctypes.Structure):
        _fields_ = [
            ('cbSize',       ctypes.wintypes.DWORD),
            ('fMask',        ctypes.c_ulong),
            ('hwnd',         ctypes.wintypes.HWND),
            ('lpVerb',       ctypes.c_char_p),
            ('lpFile',       ctypes.c_char_p),
            ('lpParameters', ctypes.c_char_p),
            ('lpDirectory',  ctypes.c_char_p),
            ('nShow',        ctypes.c_int),
            ('hInstApp',     ctypes.wintypes.HINSTANCE),
            ('lpIDList',     ctypes.c_void_p),
            ('lpClass',      ctypes.c_char_p),
            ('hKeyClass',    ctypes.wintypes.HKEY),
            ('dwHotKey',     ctypes.wintypes.DWORD),
            ('hIcon',        ctypes.wintypes.HANDLE),
            ('hProcess',     ctypes.wintypes.HANDLE)]

        def __init__(self, **kw):
            super(ShellExecuteInfo, self).__init__()
            self.cbSize = ctypes.sizeof(self)
            for field_name, field_value in kw.items():
                setattr(self, field_name, field_value)

    SEE_MASK_NOCLOSEPROCESS = 0x00000040
    SEE_MASK_NO_CONSOLE = 0x00008000
    INFINITE = -1

    command_file, command_args = command[0], command[1:]

    params = ShellExecuteInfo(
        nShow=int(False),
        fMask=SEE_MASK_NOCLOSEPROCESS | SEE_MASK_NO_CONSOLE,
        lpVerb=b'runas',
        lpFile=command_file.encode('cp1252'),
        lpParameters=subprocess.list2cmdline(command_args).encode('cp1252'))

    if not ctypes.windll.shell32.ShellExecuteExA(ctypes.byref(params)):
        raise RuntimeError('Failed to run command "%s" as admin', command_file)

    process_handle = params.hProcess
    ctypes.windll.kernel32.WaitForSingleObject(process_handle, INFINITE)

    ret = ctypes.wintypes.DWORD()
    if ctypes.windll.kernel32.GetExitCodeProcess(process_handle, ctypes.byref(ret)) == 0:
        raise RuntimeError('Failed to retrieve exit code')

    return ret.value


# The following methods has been adapted from the appdirs package
#
# MIT license
# Copyright (c) 2005-2010 ActiveState Software Inc.
#
# Copyright (c) 2013 Eddy Petrișor
# http://github.com/ActiveState/appdirs


def user_data_dir(appname=None, appauthor=None, version=None, roaming=False):
    r"""Return full path to the user-specific data dir for this application.

    Parameters
    ----------
    appname : str
        Name of application.
        If ``None``, just the system directory is returned.
    appauthor : str
        Only used on Windows. Name of the appauthor or distributing body
        for this application. Typically it is the owning company name.
        This falls back to appname. You may pass ``False`` to disable it.
    version : str
        Version path element to append to the path.
        You might want to use this if you want multiple versions
        of your app to be able to run independently. If used, this
        would typically be "<major>.<minor>".
        Only applied when appname is present.
    roaming : bool, optional
        True to use the Windows roaming appdata directory, otherwise False.
        That means that for users on a Windows network setup for roaming profiles,
        this user data will be sync'd on login. See
        <http://technet.microsoft.com/en-us/library/cc766489(WS.10).aspx>
        for a discussion of issues.

    Returns
    -------
    str
        Full path to the user-specific data dir.
    """
    if system == 'win32':
        if appauthor is None:
            appauthor = appname
        const = "CSIDL_APPDATA" if roaming else "CSIDL_LOCAL_APPDATA"
        path = os.path.normpath(_get_win_folder(const))
        if appname:
            if appauthor is not False:
                path = os.path.join(path, appauthor, appname)
            else:
                path = os.path.join(path, appname)
    elif system == 'darwin':
        path = os.path.expanduser('~/Library/Application Support/')
        if appname:
            path = os.path.join(path, appname)
    else:
        path = os.getenv('XDG_DATA_HOME', os.path.expanduser("~/.local/share"))
        if appname:
            path = os.path.join(path, appname)

    if appname and version:
        path = os.path.join(path, version)

    return path


def _get_win_folder_from_registry(csidl_name):
    """This is a fallback technique at best. I'm not sure if using the
    registry for this guarantees us the correct answer for all CSIDL_*
    names.
    """
    if PY3:
        import winreg as _winreg
    else:
        import _winreg

    shell_folder_name = {
        "CSIDL_APPDATA": "AppData",
        "CSIDL_COMMON_APPDATA": "Common AppData",
        "CSIDL_LOCAL_APPDATA": "Local AppData",
    }[csidl_name]

    key = _winreg.OpenKey(
        _winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
    )
    dir, type = _winreg.QueryValueEx(key, shell_folder_name)
    return dir


def _get_win_folder_with_pywin32(csidl_name):
    from win32com.shell import shellcon, shell
    dir = shell.SHGetFolderPath(0, getattr(shellcon, csidl_name), 0, 0)
    # Try to make this a unicode path because SHGetFolderPath does
    # not return unicode strings when there is unicode data in the
    # path.
    try:
        dir = str(dir) if PY3 else unicode(dir)

        # Downgrade to short path name if have highbit chars. See
        # <http://bugs.activestate.com/show_bug.cgi?id=85099>.
        has_high_char = False
        for c in dir:
            if ord(c) > 255:
                has_high_char = True
                break
        if has_high_char:
            try:
                import win32api
                dir = win32api.GetShortPathName(dir)
            except ImportError:
                pass
    except UnicodeError:
        pass
    return dir


def _get_win_folder_with_ctypes(csidl_name):
    import ctypes

    csidl_const = {
        "CSIDL_APPDATA": 26,
        "CSIDL_COMMON_APPDATA": 35,
        "CSIDL_LOCAL_APPDATA": 28,
    }[csidl_name]

    buf = ctypes.create_unicode_buffer(1024)
    ctypes.windll.shell32.SHGetFolderPathW(None, csidl_const, None, 0, buf)

    # Downgrade to short path name if have highbit chars. See
    # <http://bugs.activestate.com/show_bug.cgi?id=85099>.
    has_high_char = False
    for c in buf:
        if ord(c) > 255:
            has_high_char = True
            break
    if has_high_char:
        buf2 = ctypes.create_unicode_buffer(1024)
        if ctypes.windll.kernel32.GetShortPathNameW(buf.value, buf2, 1024):
            buf = buf2

    return buf.value


if system == "win32":
    try:
        import win32com.shell
        _get_win_folder = _get_win_folder_with_pywin32
    except ImportError:
        try:
            from ctypes import windll
            _get_win_folder = _get_win_folder_with_ctypes
        except ImportError:
            _get_win_folder = _get_win_folder_from_registry


__all__ = [
    'absjoin',
    'system',
    'create_symlink',
    'remove_symlink',
    'user_data_dir',
    'select_python',
    'prepare_environment',
    'is_admin'
]
