# -*- coding: utf-8 -*-
"""
These are internal functions of the framework.
Not intended to be used outside compas* packages.
"""
import os
import shutil
import sys
import tempfile

try:
    NotADirectoryError
except NameError:
    class NotADirectoryError(Exception):
        pass

PY3 = sys.version_info[0] == 3


__all__ = [
    'absjoin',
    'create_symlink',
    'create_symlinks',
    'remove_symlink',
    'remove_symlinks',
    'copy',
    'remove',
    'rename',
    'user_data_dir',
    'select_python',
    'prepare_environment',
    'is_admin',
    'is_windows',
    'is_linux',
    'is_osx',
    'is_mono',
    'is_ironpython',
    'is_rhino',
    'is_blender'
]


def is_windows():
    """Check if the operating system is Windows.

    Returns
    -------
    bool
        True if the OS is Windows. False otherwise

    """
    if is_ironpython():
        return os.name == 'nt'
    return sys.platform == 'win32'


def is_linux():
    """Check if the operating system is Linux.

    Returns
    -------
    bool
        True if the OS is Linux. False otherwise

    """
    return sys.platform in ('linux', 'linux2')


def is_osx():
    return sys.platform == 'darwin'


def is_mono():
    """Check if the operating system is running on Mono.

    Returns
    -------
    bool
        True if the OS is running on Mono. False otherwise

    """
    return 'mono' in sys.version.lower()


def is_ironpython():
    """Check if the Python implementation is IronPython.

    Returns
    -------
    bool
        True if the implementation is IronPython. False otherwise

    """
    return 'ironpython' in sys.version.lower()


def is_rhino():
    try:
        import Rhino  # noqa : F401
    except ImportError:
        return False
    else:
        return True


def is_blender():
    try:
        import bpy  # noqa : F401
    except ImportError:
        return False
    else:
        return True


if is_windows():
    import subprocess
    import ctypes
    import ctypes.wintypes

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


try:
    from compas_bootstrapper import PYTHON_DIRECTORY
except:  # noqa: E722
    # We re-map CONDA_PREFIX for backwards compatibility reasons
    # In a few releases down the line, we can get rid of this bit
    try:
        from compas_bootstrapper import CONDA_PREFIX as PYTHON_DIRECTORY
    except:  # noqa: E722
        PYTHON_DIRECTORY = None

try:
    from compas_bootstrapper import CONDA_EXE
except:  # noqa: E722
    CONDA_EXE = None


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
    if PYTHON_DIRECTORY and os.path.exists(PYTHON_DIRECTORY):
        python_executables = [python_executable] if python_executable else ['pythonw', 'python']

        for python_exe in python_executables:
            python = os.path.join(PYTHON_DIRECTORY, python_exe)
            if os.path.exists(python):
                return python

            python = os.path.join(PYTHON_DIRECTORY, '{0}.exe'.format(python_exe))
            if os.path.exists(python):
                return python

            python = os.path.join(PYTHON_DIRECTORY, 'bin', python_exe)
            if os.path.exists(python):
                return python

            python = os.path.join(PYTHON_DIRECTORY, 'bin', '{0}.exe'.format(python_exe))
            if os.path.exists(python):
                return python

    default_exe = 'pythonw' if is_windows() else 'python'

    # Assume a system-wide install exists
    return python_executable or default_exe


def prepare_environment(env=None):
    """Prepares an environment context to run Python on.

    If Python is being used from a conda environment, this is roughly equivalent
    to activating the conda environment by setting up the correct environment
    variables.

    Parameters
    ----------
    env : dict, optional
        Dictionary of environment variables to modify. If ``None`` is passed, then
        this will create a copy of the current ``os.environ``.

    Returns
    -------
    dict
        Updated environment variable dictionary.
    """

    if env is None:
        env = os.environ.copy()

    if PYTHON_DIRECTORY:
        if is_windows():
            lib_bin = os.path.join(PYTHON_DIRECTORY, 'Library', 'bin')
        else:
            lib_bin = os.path.join(PYTHON_DIRECTORY, 'bin')

        if os.path.exists(lib_bin) and lib_bin not in env['PATH']:
            env['PATH'] = lib_bin + os.pathsep + env['PATH']

    if CONDA_EXE:
        env['CONDA_EXE'] = CONDA_EXE

    return env


def absjoin(*parts):
    return os.path.abspath(os.path.join(*parts))


# Cache whatever symlink function works (native or polyfill)
_os_symlink = None


def _polyfill_symlinks(symlinks, raise_on_error):
    """Create multiple symlinks using the polyfill implementation."""
    _handle, temp_path = tempfile.mkstemp(suffix='.cmd', text=True)

    with open(temp_path, 'w') as mklink_cmd:
        mklink_cmd.write('@echo off\n')
        mklink_cmd.write('SET /A symlink_result=0\n')
        mklink_cmd.write('ECHO ret=%symlink_result%\n')
        for i, (source, link_name) in enumerate(symlinks):
            mklink_cmd.write("mklink /D {}\n".format(subprocess.list2cmdline([link_name, source])))
            mklink_cmd.write('IF %ERRORLEVEL% EQU 0 SET /A symlink_result += {} \n'.format(2 ** i))

        mklink_cmd.write('EXIT /B %symlink_result%\n')

    ret_value = _run_as_admin([temp_path])

    # The error level integer (ret_value) reflects the success/failure of
    # each of the symlink operations, so we do a bit of bitwise-arithmetic
    # on it to figure out which symlinks worked and which ones failed.

    result = []
    for i in range(len(symlinks)):
        success = ret_value & 2 ** i != 0
        result.append(success)

    return result


def _native_symlinks(symlinks, raise_on_error):
    """Create multiple symlinks using the native implementation."""
    result = []

    for source, link_name in symlinks:
        try:
            os.symlink(source, link_name)
            result.append(True)
        except OSError:
            if raise_on_error:
                raise

            result.append(False)

    return result


def _set_symlink_function(fn):
    global _os_symlink
    _os_symlink = fn


def _get_symlink_function():
    global _os_symlink
    allow_polyfill_retry = False

    if not _os_symlink:
        if getattr(os, 'symlink', None):
            _os_symlink = _native_symlinks

        if is_windows():
            if not callable(_os_symlink):
                _os_symlink = _polyfill_symlinks
            else:
                allow_polyfill_retry = True

    return _os_symlink, allow_polyfill_retry


def create_symlink(source, link_name):
    """Create a symbolic link pointing to source named link_name.

    Parameters
    ----------
    source: str
        Source of the link
    link_name: str
        Link name.

    Notes
    -----
    This function is a polyfill of the native ``os.symlink``
    for Python 2.x on Windows platforms.
    """
    create_symlinks([(source, link_name)], raise_on_error=True)


def create_symlinks(symlinks, raise_on_error=False):
    """Create multiple symbolic links in one call.

    Parameters
    ----------
    symlinks: list of string tuples
        List of ``source`` and ``link_name`` of the symlinks as tuples.
    """
    symlink, allow_polyfill_retry = _get_symlink_function()

    try:
        return symlink(symlinks, raise_on_error=True)
    except OSError:
        if raise_on_error:
            raise

        _set_symlink_function(_polyfill_symlinks)
        return _polyfill_symlinks(symlinks, raise_on_error=False)


def remove_symlink(symlink):
    """Remove a symlink from the file system.

    Parameters
    ----------
    symlink : :obj:`str`
        Symlink to remove.
    """
    # Broken links return False on .exists(), so we need to check .islink() as well
    if not (os.path.islink(symlink) or os.path.exists(symlink)):
        return

    if os.path.isdir(symlink):
        try:
            os.rmdir(symlink)
        except NotADirectoryError:
            os.unlink(symlink)
        except PermissionError:
            if not is_windows():
                raise

            _run_command_as_admin('rmdir', [symlink])
    else:
        os.unlink(symlink)


def remove_symlinks(symlinks, raise_on_error=False):
    """Remove one or more symlinks.

    Parameters
    ----------
    links
        Sequence of symlinks to remove.
    raise_on_error : bool
        ``False`` to continue removing even on error,
        otherwise ``True``.

    Returns
    -------
    list
        If ``raise_on_error`` is ``False``, returns a list
        of bools indicating which links were successfully removed.
    """
    result = []

    for symlink in symlinks:
        try:
            remove_symlink(symlink)
            result.append(True)
        except OSError:
            if raise_on_error:
                raise

            result.append(False)

    return result


def rename(src, dst):
    """Rename a file or directory."""
    try:
        os.rename(src, dst)
    except (PermissionError, OSError):
        if not is_windows():
            raise

        _run_command_as_admin('move', [src, dst])


def remove(path):
    """Remove path."""
    try:
        os.remove(path)
    except (PermissionError, OSError):
        if not is_windows():
            raise

        _run_command_as_admin('del', [path])


def copy(src, dst):
    """Copy a file from source to destination."""
    try:
        shutil.copy(src, dst)
    except (PermissionError, OSError):
        if not is_windows():
            raise

        _run_command_as_admin('copy', [src, dst])


def is_admin():
    """Determines whether the current user has admin rights.

    Returns
    -------
    bool
        True if the user is administrator, otherwise False.
    """
    if not is_windows():
        return os.getuid() == 0

    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except:  # noqa: E722
        return False


def _run_command_as_admin(command, arguments):
    """Run a single command as admin on Windows.

    Parameters
    ----------
    command : str
        Command name.
    arguments : list of str
        List of arguments.
    """
    _handle, temp_path = tempfile.mkstemp(suffix='.cmd', text=True)

    with open(temp_path, 'w') as remove_symlink_cmd:
        remove_symlink_cmd.write('@echo off\n')
        remove_symlink_cmd.write('{} {}\n'.format(command, subprocess.list2cmdline(arguments)))

    _run_as_admin([temp_path])


def _run_as_admin(command):
    """Run the specified command as an admin.

    Paramters
    ---------
    command : :obj:`list` of :obj:`str`
        List of strings of the command to run.

    Returns
    -------
    int
        Exit code of the process.
    """

    if not is_windows():
        raise RuntimeError('Only supported on Windows')

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
    if is_windows():
        if appauthor is None:
            appauthor = appname
        const = "CSIDL_APPDATA" if roaming else "CSIDL_LOCAL_APPDATA"
        path = os.path.normpath(_get_win_folder(const))
        if appname:
            if appauthor is not False:
                path = os.path.join(path, appauthor, appname)
            else:
                path = os.path.join(path, appname)

    elif is_osx():
        path = os.path.expanduser('~/Library/Application Support/')
        if appname:
            path = os.path.join(path, appname)

    elif is_mono():
        path = os.path.expanduser('~/Library/Application Support/')
        if appname:
            path = os.path.join(path, appname)

    else:
        # is_linux()
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
        dir = str(dir) if PY3 else unicode(dir)  # noqa: F821

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


if is_windows():
    try:
        import win32com.shell  # noqa: F401
        _get_win_folder = _get_win_folder_with_pywin32
    except ImportError:
        try:
            from ctypes import windll  # noqa: F401
            _get_win_folder = _get_win_folder_with_ctypes
        except ImportError:
            _get_win_folder = _get_win_folder_from_registry
