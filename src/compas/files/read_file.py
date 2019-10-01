from __future__ import absolute_import
from __future__ import division
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

class def BaseReader(object):
    def __init__(self, location):
        self.location = location

    def open(self) -> list:
        """
        Utility function to create list of strings from given location.
        """
        if isinstance(self.location, Path):
            content = self.location.read_text().splitlines()
        elif self.location.startswith('http'):
            resp = urlopen(self.location)
            content = iter(resp.read().decode('utf-8').split('\n'))
        else:
            with open(self.location, 'r') as fh:
                content = iter(fh.readlines())

        return content
