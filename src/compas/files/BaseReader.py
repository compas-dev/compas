from __future__ import absolute_import
from __future__ import division

from functools import partial

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


class BaseReader(object):
    """Base class containing file reading functions for file extension specific readers

    Attributes
    ----------
    location : str or pathlib object
        Path or URL to the file
    """

    def __init__(self, location):
        self.location = location

    def read_from_location(self):
        """Returns iterable reading file line by line when given a location,
           either as pathlib object, string containing path or string containing url

        Returns
        -------
        iterable
            Iterable returning file line by line
        """

        if isinstance(self.location, Path):
            with self.location.open(mode='r') as fh:
                content = iter(fh.readlines())
        elif self.location.startswith('http'):
            resp = urlopen(self.location)
            content = iter(resp.read().decode('utf-8').split('\n'))
        else:
            with open(self.location, 'r') as fh:
                content = iter(fh.readlines())

        return content

    def read_binary_from_location(self):
        """Opens and reads binary file

        Returns
        -------
        iterable
            Iterable reading file

        """

        if self.location.isinstance(Path):
            with self.location.open(mode='r') as fh:
                content = iter(partial(fh.read, 64), b'')
        elif self.location.startswith('http'):
            raise NotImplementedError
        else:
            with open(self.location, 'r') as fh:
                content = iter(partial(fh.read, 64), b'')

        return content
