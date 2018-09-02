from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Mesh

__all__ = ['AbstractMeshLoader', 'DefaultMeshLoader']

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

SUPPORTED_FORMATS = ('obj', 'stl', 'ply')


class AbstractMeshLoader(object):
    """Basic contract/interface for all mesh loaders."""

    def can_handle_url(self, url):
        """Determine whether this loader can resolve a given URL.

        Parameters
        ----------
        url : str
            Mesh URL.

        Returns
        -------
        bool
            ``True`` if it can handle it, otherwise ``False``.
        """
        return NotImplementedError

    def resolve(self, url):
        """Resolve and load the given URL.

        Parameters
        ----------
        url : str
            Mesh URL

        Returns
        -------
        :class:`Mesh`
            Instance of a mesh.
        """
        return NotImplementedError


class DefaultMeshLoader(AbstractMeshLoader):
    """Handles basic mesh loader tasks, mostly from local files."""

    def __init__(self):
        super(DefaultMeshLoader, self).__init__()

    def can_handle_url(self, url):
        scheme = urlparse(url).scheme

        # Local files have either:
        #  - no scheme
        #  - a one-letter scheme in Windows
        #  - file scheme
        is_local_file = len(scheme) in (0, 1) or scheme == 'file'

        if is_local_file:
            return True

        # Only OBJ loader supports remote files atm
        is_obj = _get_file_format(url) == 'obj'
        return scheme in ('http', 'https') and is_obj

    def resolve(self, url):
        if url.startswith('file:///'):
            url = url[8:]

        return _mesh_import(url, url)


def _get_file_format(url):
    # This could be much more elaborate
    # with an actual header check
    # and/or remote content-type check
    file_extension = url.split('.')[-1].lower()
    return file_extension


def _mesh_import(name, file):
    """Internal function to load meshes using the correct loader.

    Name and file might be the same but not always, e.g. temp files."""
    file_extension = _get_file_format(name)

    if file_extension not in SUPPORTED_FORMATS:
        raise NotImplementedError(
            'Mesh type not supported: {}'.format(file_extension))

    if file_extension == 'obj':
        return Mesh.from_obj(file)
    elif file_extension == 'stl':
        return Mesh.from_stl(file)
    elif file_extension == 'ply':
        return Mesh.from_ply(file)

    raise Exception
