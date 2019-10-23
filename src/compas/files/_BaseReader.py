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

            # TODO: Handle url's to binary files
            if self.is_URL:
                resp = urlopen(self.location)
                for line in resp.read().decode('utf-8').split('\n'):
                    yield line
            else:
                try:
                    with self.location.open(mode='r') as fh:
                        for line in fh:
                            yield line
                except UnicodeDecodeError:
                    with self.location.open(mode='r',
                                            errors='replace',
                                            newline='\r') as fh:
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
            raise IOError('File not found.')

    def check_file_signature(self):
        '''
        TODO: Docstring
           https://en.wikipedia.org/wiki/List_of_file_signatures
           https://en.wikipedia.org/wiki/File_format#Magic_number
        '''
        if self.is_URL:
            # not implemented yet
            pass

        elif not self.file_signature:
            raise TypeError('File type has no associated file signature')

        else:
            with self.location.open(mode="rb") as fd:
                fd.seek(self.file_signature['offset'])

                found_signature = fd.read(len(self.file_signature['content']))
                file_signature = self.file_signature['content']

                if isinstance(found_signature, str) and found_signature != file_signature.decode():
                    raise Exception('File not valid, import failed.')
                elif found_signature != file_signature:
                    raise Exception('File not valid, import failed.')
