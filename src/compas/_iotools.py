"""For the time being, these functions are only for internal use."""
from __future__ import print_function

import io
import platform
from contextlib import contextmanager

if "ironpython" == platform.python_implementation().lower():
    from System import Array
    from System import Byte
    from System.IO import MemoryStream
    from System.Net import SecurityProtocolType
    from System.Net import ServicePointManager
    from System.Net import WebRequest

    def download_url_as_bytes(url):
        ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12

        request = WebRequest.Create(url)

        response = request.GetResponse()
        responseStream = response.GetResponseStream()

        memoryStream = MemoryStream()
        buffer = Array.CreateInstance(Byte, 8192)
        bytesRead = responseStream.Read(buffer, 0, buffer.Length)

        while bytesRead > 0:
            memoryStream.Write(buffer, 0, bytesRead)
            bytesRead = responseStream.Read(buffer, 0, buffer.Length)

        return memoryStream.ToArray()

else:
    from urllib.request import urlopen

    def download_url_as_bytes(url):
        response = urlopen(url)
        return response.read()


@contextmanager
def open_file(file_or_filename, mode="r"):
    """Context-manager to open a file, path or URL and return a corresponding file object.

    If the argument is a path-like object, it will open it,
    if the argument is an HTTP(s) URL, it will open it, and
    if the argument is already a file-like object, it will simply yield it.

    This context manager ensures that when using a path-like object as input,
    the file is closed once it it goes out of scope.

    Notes
    -----
    This context-manager will only close files that it opened itself. If an opened file
    is passed as the argument, it will not close it.

    Parameters
    ----------
    file_or_filename : path-like, file-like object or URL string
        A path-like, a file-like object or a URL pointing to a file.
    mode : str, optional
        Specifies the mode in which the file is opened. It defaults to ``'r'`` which means open for reading in text mode.

    Yields
    -------
    file-like object
        File object already opened.
    """
    file = file_or_filename
    close_source = False

    if not hasattr(file, "read"):
        # If it's a URL, open and read its response into an in-memory stream
        if hasattr(file, "startswith") and file.startswith("http"):
            # support all read modes (r, r+, rb, etc)
            if not mode.startswith("r"):
                raise ValueError("URLs can only be opened in read mode.")
            file = io.BytesIO(download_url_as_bytes(file))
        else:
            file = open(file, mode=mode)
            close_source = True
    try:
        yield file
    finally:
        if close_source:
            file.close()


def iter_file(file, size=65536):
    """Iterate over a file returning chunks of data until EOF.

    Parameters
    ----------
    file : file-like object
        A file-like object.
    size : int, optional
        Size of each chuck of data to be read. Defaults to ``65536``.

    Yields
    -------
    bytes
        Byte array chunks read from the file.
    """
    while True:
        data = file.read(size)
        if not data:
            break
        yield data


if __name__ == "__main__":
    import time

    from compas.datastructures import Mesh

    platform.RANDOM = "python"
    iters = 5.0

    if "ironpython" == platform.python_implementation().lower():
        print("Running on urllib2 implementation")
        for i in range(5):
            all_times = []
            for j in range(int(iters)):
                t1 = time.time()
                url = r"https://raw.githubusercontent.com/ros-industrial/abb/kinetic-devel/abb_irb6600_support/meshes/irb6640/visual/link_{}.stl".format(
                    i + 1
                )
                mesh = Mesh.from_stl(url)
                if i > 0:  # discard first iteration
                    all_times.append(time.time() - t1)
                    print("  File {}, took {:.3f} secs".format(i, all_times[-1]), end=", ")
            if all_times:
                print()
                print("Average: {:.3f} secs".format(sum(all_times) / iters))

        print("Switch to .NET implementation")
        platform.RANDOM = ".NET"
        for i in range(5):
            all_times = []
            for j in range(int(iters)):
                t1 = time.time()
                url = r"https://raw.githubusercontent.com/ros-industrial/abb/kinetic-devel/abb_irb6600_support/meshes/irb6640/visual/link_{}.stl".format(
                    i + 1
                )
                mesh = Mesh.from_stl(url)
                if i > 0:  # discard first iteration
                    all_times.append(time.time() - t1)
                    print("  File {}, took {:.3f} secs".format(i, all_times[-1]), end=", ")
            if all_times:
                print()
                print("Average: {:.3f} secs".format(sum(all_times) / iters))

    else:
        print("Running on urllib.request implementation")
        for i in range(5):
            all_times = []
            for j in range(int(iters)):
                t1 = time.time()
                url = r"https://raw.githubusercontent.com/ros-industrial/abb/kinetic-devel/abb_irb6600_support/meshes/irb6640/visual/link_{}.stl".format(
                    i + 1
                )
                mesh = Mesh.from_stl(url)
                if i > 0:  # discard first iteration
                    all_times.append(time.time() - t1)
                    print("  File {}, took {:.3f} secs".format(i, all_times[-1]), end=", ", flush=True)
            if all_times:
                print()
                print("Average: {:.3f} secs".format(sum(all_times) / iters))
