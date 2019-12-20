from __future__ import absolute_import
from __future__ import division

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

import binaryornot.check


class BaseReader(object):
    """Base class containing file reading functions for file extension specific readers

    Attributes
    ----------
    location : Path object
        Path to file location
    """

    FILE_SIGNATURE = {
         'content': None,
         'offset': None,
    }

    def __init__(self, address):
        self._address = address
        self._is_binary = None

    @property
    def location(self):
        """Path to local file

        Checks if given address is a Path object, and if not creates one from
        given address if it's a file path or URL in a string.

        If an URL is given as the address the file will be downloaded to a
        temporary directory[1]_ and the location property will be a Path
        object for the downloaded files location.

        .. [1] See builtin module tempfile
           https://docs.python.org/3/library/tempfile.html

        Parameters
        ----------
        self._address : string or Path object
            Address specified either as an URL, string containing path or
            Path object

        Returns
        ------
        Path object
            Path object for file location
        """
        if self.is_address_url():
            pathobj = self._download(self._address)
        else:
            if not isinstance(self._address, Path):
                pathobj = Path(self._address)
            else:
                pathobj = self._address

        # Makes path absolute and raises FileNotFound if file is not found
        pathobj.resolve(strict=True)

        return pathobj

    @property
    def is_binary(self):
        """ Tries to determine if a file is binary or not using the
            binaryornot library.

        Returns
        -------
        bool
            True if binary, else false.
        """
        return binaryornot.check.is_binary(str(self.location))

    @property
    def is_valid(self):
        return NotImplementedError

    def is_address_url(self):
        """Checks if given address is an URL

        Returns
        -------
        bool
            True if recognized as an URL
        """
        return str(self._address).startswith('http')

    def _download(self, url):
        """Downloads file and returns path to tempfle

        Called by property self.location

        Parameters
        ----------
        url : string
            URL to file

        Returns
        -------
        location : Pathlib object
            Path to downloaded file (stored in temporary folder)
        """
        location, _ = urlretrieve(url)

        return Path(location)

    def open_ascii(self):
        """Open ascii file and return file object

        Returns
        -------
        file object
        """
        try:
            file_object = self.location.open(mode='r')
        except UnicodeDecodeError:
            file_object = self.location.open(mode='r', errors='replace', newline='\r')
        return file_object

    def open_binary(self):
        """Open binary file and return file object

        Returns
        -------
        file object
        """
        return self.location.open(mode='rb')

    def iter_lines(self):
        """Yields lines from ascii file

        Yields
        -------
        string
            Next line in file
        """
        # TODO: Handle continuing lines (as in OFF files)

        with self.open_ascii() as fo:
            for line in fo:
                yield line.rstrip()

    def iter_chunks(self, chunk_size=4096):
        """Yields chunks from binary files

        Parameters
        ----------
        chunk_size : int
            Chunks to read with each call

        Yields
        ------
        bytes
            Next chunk of file
        """
        with self.open_binary() as fo:
            # reads until empty byte string is encountered
            for chunk in iter(lambda: fo.read(chunk_size), b''):
                yield chunk

    def read(self):
        raise NotImplementedError

    def is_file_signature_correct(self):
        """Checks wether file signature (also known as magic number) is present
        in input file.

        File signatures are strings, numbers or bytes defined in a file
        format's specification. While not technically required to parse the
        file, a missing file signatures might be a sign of a malformed file.

        More information about file signatures can be found on Wikipedia[1]_
        as well as examples of file signatures[2]_

        Returns
        ------
        bool
            True if file signature for file type is found in file or if file
            type has no file signature.

        .. [1] https://en.wikipedia.org/wiki/List_of_file_signatures
        .. [2] https://en.wikipedia.org/wiki/File_format#Magic_number
        """

        if self.FILE_SIGNATURE['content'] is None:
            return True

        file_signature = self.FILE_SIGNATURE['content']

        if self.FILE_SIGNATURE['offset'] is None:
            signature_offset = 0
        else:
            signature_offset = self.FILE_SIGNATURE['offset']

        with self.location.open(mode="rb") as fd:
            fd.seek(signature_offset)
            found_signature = fd.read(len(file_signature))

        if isinstance(found_signature, str) and found_signature != file_signature.decode():
            return False
        elif found_signature != file_signature:
            return False

        return True
