"""
These are internal functions of the framework.
Not intended to be used outside compas* packages.
"""
import os


def create_symlink(source, link_name):
    """Create a symbolic link pointing to source named link_name.

    Parameters:
        source: Source of the link
        link_name: Link name.

    Note:
        This function is a polyfill of the native ``os.symlink``
        for Python 2.x on Windows platforms.
    """
    os_symlink = getattr(os, 'symlink', None)

    if not callable(os_symlink) and os.name == 'nt':
        import subprocess

        def symlink_ms(source, link_name):
            subprocess.check_output(
                ['mklink', '/D', link_name, source], stderr=subprocess.STDOUT, shell=True)

        os_symlink = symlink_ms

    os_symlink(source, link_name)

def remove_symlink(link):
    if os.path.isdir(link):
        os.rmdir(link)
    else:
        os.unlink(link)
