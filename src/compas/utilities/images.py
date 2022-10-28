from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import compas

if not compas.IPY:
    import imageio


__all__ = ["gif_from_images"]


def gif_from_images(
    files,
    gif_path,
    fps=10,
    loop=0,
    reverse=False,
    pingpong=False,
    subrectangles=True,
    delete_files=False,
):
    """Create an animated GIF from a series of images.

    Parameters
    ----------
    files : list
        The image series.
    gif_path : str
        The location to save the GIF.
    fps : int, optional
        Frames per second.
    loop : int, optional
        The number of loops.
    reverse : bool, optional
        If True, reverse the image series.
    pingpong : bool, optional
        If True, add a reverse sequence to the end of the base sequence to go back to the beginning.
    subrectangles : bool, optional
        If True, optimize the file size by looking for invariant subrectangles.

    Returns
    -------
    None

    """
    if reverse:
        files.reverse()
    if pingpong:
        files += files[::-1]
    with imageio.get_writer(gif_path, mode="I", fps=fps, loop=loop, subrectangles=subrectangles) as writer:
        for filename in files:
            image = imageio.imread(filename)
            writer.append_data(image)
    if delete_files:
        for filename in files:
            os.remove(filename)
