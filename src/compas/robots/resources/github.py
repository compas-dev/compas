from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.robots.resources.basic import AbstractMeshLoader
from compas.robots.resources.basic import _mesh_import

__all__ = ['GithubPackageMeshLoader']

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


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
        Branch name, defaults to ``main``.
    relative_path : str
        Relative path of the support package within the repository.
        If the repository itself is the support package, set
        ``relative_path`` to ``'.'``.  Defaults to ``support_package``
    """

    HOST = 'https://raw.githubusercontent.com'

    def __init__(self, repository, support_package, branch='main', relative_path=None):
        super(GithubPackageMeshLoader, self).__init__()
        self.repository = repository
        self.support_package = support_package
        self.branch = branch
        self.schema_prefix = 'package://' + self.support_package + '/'
        self.relative_path = support_package if relative_path is None else relative_path

    def build_url(self, file):
        """Returns the corresponding url of the file.

        Parameters
        ----------
        file : str
            File name. Following convention, the file should reside
            inside a ``urdf`` folder.

        Returns
        -------
        str
            The file's url.
        """
        url_components = [
            GithubPackageMeshLoader.HOST,
            self.repository,
            self.branch,
            file
        ]
        if self.relative_path != '.':
            url_components.insert(3, self.relative_path)
        return '/'.join(url_components)

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

        return _mesh_import(url, url)
