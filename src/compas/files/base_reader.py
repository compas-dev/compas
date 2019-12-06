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
        self.is_url = location
        self.location = location

    @property
    def is_url(self):
        return self._is_url

    @is_url.setter
    def is_url(self, location):
        """Determine if location is local or specified as an URL
        """
        if str(location).startswith('http'):
            self._is_url = True
        else:
            self._is_url = False

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        """Ensure that location is specified using Path object
        """
        if self.is_url:
            self._location = location
        else:
            if not isinstance(location, Path):
                pathobj = Path(location)
            else:
                pathobj = location

            if pathobj.exists():
                self._location = pathobj
            else:
                raise IOError('File not found.')

    def read_line_or_chunk(self, mode='ascii'):
        """Returns iterable reading file line by line

        Should accept both local files as well as URLs, in binary or ascii format.

        Parameters
        ---------
        mode : string
            Treat file as ascii or binary
        Yields
        -------
        string
            Next line or chunk of file
        """
        # TODO: Handle url's to binary files
        # TODO: Handle continuing lines (as in OFF files)
        # TODO: Read binary chunks

        self.check_file_signature()

        if mode == 'ascii':
            print(self.is_url)

            if self.is_url:
                resp = urlopen(self.location)
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

    def check_file_signature(self):
        """Checks wether file signature (also known as magic number) is present
        in input file.

        File signatures are strings, numbers or bytes defined in a file
        format's specification. While not technically required to parse the
        file, a missing file signatures might be a sign of a malformed file.

        More information about file signatures can be found on Wikipedia[1]_
        as well as examples of file signatures[2]_

        Raises
        ------
        Exception
            If file signature is specified for file format but not present
            in file.

        .. [1] https://en.wikipedia.org/wiki/List_of_file_signatures
        .. [2] https://en.wikipedia.org/wiki/File_format#Magic_number
        """
        # TODO: Check url
        if self.is_url:
            # not implemented yet
            return

        try:
            file_signature = self.FILE_SIGNATURE['content']
            signature_offset = self.FILE_SIGNATURE['offset']

        # if file type has no associated file signature
        except AttributeError:
            return

        with self.location.open(mode="rb") as fd:
            fd.seek(signature_offset)
            found_signature = fd.read(len(file_signature))

        if isinstance(found_signature, str) and found_signature != file_signature.decode():
            raise Exception('File not valid, import failed.')
        elif found_signature != file_signature:
            raise Exception('File not valid, import failed.')
