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
        Repository name including organization, e.g. ``compas-dev/robots``.
    support_package : str
        Name of the support package containing URDF, Meshes and additional assets.
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

    def open_url(self, file):
        url = self.build_url(file)
        return urlopen(url)

    def can_handle_url(self, url):
        return url.startswith(self.schema_prefix)

    def resolve(self, url):
        """Resolves a URL and loads the external mesh.

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
