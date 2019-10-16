from __future__ import absolute_import
from __future__ import division

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

    def read(self, mode='ascii'):
        """Returns iterable reading file line by line when given a location,
           either as pathlib object, string containing path or string containing url

        Returns
        -------
        iterable
            Iterable returning file line by line
        """

        if mode == 'ascii':

            if isinstance(self.location, Path):
                with self.location.open(mode='r') as fh:
                    for line in fh:
                        yield line
            elif self.location.startswith('http'):
                resp = urlopen(self.location)
                yield from iter(resp.read().decode('utf-8').split('\n'))
            else:
                with open(self.location, 'r') as fh:
                    for line in fh:
                        yield line

        elif mode == 'binary':
            raise NotImplementedError

        else:
            raise ValueError("mode most be ascii or binary")
