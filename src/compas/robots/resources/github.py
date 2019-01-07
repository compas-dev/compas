from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Mesh
from compas.robots.resources.basic import SUPPORTED_FORMATS
from compas.robots.resources.basic import AbstractMeshLoader
from compas.robots.resources.basic import _mesh_import

__all__ = ['GithubPackageMeshLoader']

try:
    from urllib.request import urlopen, urlretrieve
except ImportError:
    from urllib2 import urlopen
    from urllib import urlretrieve


class GithubPackageMeshLoader(AbstractMeshLoader):
    """Loads resources stored in Github.

    Attributes
    ----------
    repository : str
        Repository name including organization,
        e.g. ``ros-industrial/abb``.
    support_package : str
        Name of the support package containing URDF, Meshes
        and additional assets, e.g. 'abb_irb4400_support'
    branch : str
        Branch name, defaults to ``master``.
    """

    HOST = 'https://raw.githubusercontent.com'

    def __init__(self, repository, support_package, branch='master'):
        super(GithubPackageMeshLoader, self).__init__()
        self.repository = repository
        self.support_package = support_package
        self.branch = branch
        self.schema_prefix = 'package://' + self.support_package + '/'

    def build_url(self, file):
        return '{}/{}/{}/{}/{}'.format(GithubPackageMeshLoader.HOST,
                                       self.repository,
                                       self.branch,
                                       self.support_package,
                                       file)

    def load_urdf(self, file):
        """Load a URDF file from a Github support package repository.

        Parameters
        ----------
        file : str
            File name. Following convention, the file should reside
            inside a ``urdf`` folder.
        """
        url = self.build_url('urdf/{}'.format(file))
        return urlopen(url)

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
            matches the specified in the constructor, otherwise ``False``.
        """
        return url.startswith(self.schema_prefix)

    def load_mesh(self, url):
        """Loads a mesh from a Github repository URL.

        Parameters
        ----------
        url : str
            Mesh location

        Returns
        -------
        :class:`Mesh`
            Instance of a mesh.
        """
        _prefix, path = url.split(self.schema_prefix)
        url = self.build_url(path)

        # TODO: As soon as compas.files adds support
        # for file-like objects, we could skip
        # storing a temp file for these urls
        tempfile, _ = urlretrieve(url)
        return _mesh_import(url, tempfile)
