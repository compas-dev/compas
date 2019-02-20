from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas.datastructures import Mesh

__all__ = [
    'AbstractMeshLoader',
    'DefaultMeshLoader',
    'LocalPackageMeshLoader'
]

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

SUPPORTED_FORMATS = ('obj', 'stl', 'ply')


class AbstractMeshLoader(object):
    """Basic contract/interface for all mesh loaders."""

    def can_load_mesh(self, url):
        """Determine whether this loader can load a given Mesh URL.

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

    def load_mesh(self, url):
        """Load the mesh from the given URL.

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
    """Handles basic mesh loader tasks, mostly from local files.

    Attributes
    ----------
    kwargs (optional): dict
        Additional keyword arguments.
    """

    def __init__(self, **kwargs):
        super(DefaultMeshLoader, self).__init__()
        self.attr = kwargs or dict()

    def can_load_mesh(self, url):
        """Determine whether this loader can load a given mesh URL.

        Parameters
        ----------
        url : str
            Mesh URL.

        Returns
        -------
        bool
            ``True`` if the URL points to a local and valid file.
            Otherwise ``False``.
        """

        url = self._get_mesh_url(url)
        scheme = urlparse(url).scheme

        # Local files have either:
        #  - no scheme
        #  - a one-letter scheme in Windows
        #  - file scheme
        is_local_file = len(scheme) in (0, 1) or scheme == 'file'

        if is_local_file:
            if os.path.isfile(url):
                return True

        # Only OBJ loader supports remote files atm
        is_obj = _get_file_format(url) == 'obj'
        return scheme in ('http', 'https') and is_obj

    def load_mesh(self, url):
        """Loads a mesh from local storage.

        Parameters
        ----------
        url : str
            Mesh location

        Returns
        -------
        :class:`Mesh`
            Instance of a mesh.
        """        
        url = self._get_mesh_url(url)
        return _mesh_import(url, url)

    def _get_mesh_url(self, url):
        """Concatenates basepath directory to URL only if defined in the keyword arguments.
        It also strips out the scheme 'file:///' from the URL if present.

        Parameters
        ----------
        url : str
            Mesh location.

        Returns
        -------
        url: str
            Extended mesh url location if basepath in kwargs. 
            Else, it returns url. 
        """
        if url.startswith('file:///'):
            url = url[8:]
        
        basepath = self.attr.get('basepath') 
        if basepath:
            return os.path.join(basepath, url)
        return url


def _get_file_format(url):
    # This could be much more elaborate
    # with an actual header check
    # and/or remote content-type check
    file_extension = url.split('.')[-1].lower()
    return file_extension


class LocalPackageMeshLoader(AbstractMeshLoader):
    """Loads suport package resources stored locally.

    Attributes
    ----------
    path : str
        Path where the package is stored locally.
    support_package : str
        Name of the support package containing URDF, Meshes
        and additional assets, e.g. 'abb_irb4400_support'
    """

    def __init__(self, path, support_package):
        super(LocalPackageMeshLoader, self).__init__()
        self.path = path
        self.support_package = support_package
        self.schema_prefix = 'package://' + self.support_package + '/'

    def build_path(self, *path_parts):
        return os.path.join(self.path,
                            self.support_package,
                            *path_parts)

    def load_urdf(self, file):
        """Load a URDF file from local storage.

        Parameters
        ----------
        file : str
            File name. Following convention, the file should reside
            inside a ``urdf`` folder.
        """

        path = self.build_path('urdf', file)
        return open(path, 'r')

    def can_load_mesh(self, url):
        """Determine whether this loader can load a given mesh URL.

        Parameters
        ----------
        url : str
            Mesh URL.

        Returns
        -------
        bool
            ``True`` if the URL uses the ``package://` scheme and the package name
            matches the specified in the constructor and the file exists locally,
            otherwise ``False``.
        """
        if not url.startswith(self.schema_prefix):
            return False

        local_file = self._get_local_path(url)
        return os.path.isfile(local_file)

    def load_mesh(self, url):
        """Loads a mesh from local storage.

        Parameters
        ----------
        url : str
            Mesh location

        Returns
        -------
        :class:`Mesh`
            Instance of a mesh.
        """
        local_file = self._get_local_path(url)
        return _mesh_import(url, local_file)

    def _get_local_path(self, url):
        _prefix, path = url.split(self.schema_prefix)
        return self.build_path(*path.split('/'))


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
