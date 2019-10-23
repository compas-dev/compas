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
        self.is_URL = False
        self.location = self.check_location(location)

    def read(self, mode='text'):
        """Returns iterable reading file line by line when given a location,
           either as pathlib object, string containing path or string containing url
           TODO: Update docstring
        Arguments
        ---------
        mode : string
            Treat file as ascii or binary

        Yields
        -------
        string
            yields next line
        """

        if mode == 'text':

            if self.is_URL:
                resp = urlopen(self.location)
                print(resp)
                for line in resp.read().decode('utf-8').split('\n'):
                    yield line
            else:
                try:
                    with self.location.open(mode='r') as fh:
                        for line in fh:
                            yield line
                except UnicodeDecodeError:
                    with self.location.open(mode='r', errors='replace', newline='\r') as fh:
                        for line in fh:
                            yield line

        elif mode == 'binary':
            raise NotImplementedError

        else:
            raise ValueError('mode {} not recognized'.format(mode))

    def check_location(self, location):
        """ TODO: Docstring
        """
        if str(location).startswith('http'):
            self.is_URL = True
            return location
        elif not isinstance(location, Path):
            pathobj = Path(location)
        else:
            pathobj = location

        if pathobj.exists():
            return pathobj
        else:
            raise FileNotFoundError


    def check_file_signature(self):
        '''
        TODO: Docstring
           https://en.wikipedia.org/wiki/List_of_file_signatures
           https://en.wikipedia.org/wiki/File_format#Magic_number
        '''
        if not self.file_signature:
            raise TypeError('File type has no associated file signature')

        with self.location.open(mode="rb") as fd:
            return fd.read(len(self.file_signature)) == self.file_signature
