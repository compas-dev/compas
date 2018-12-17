from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

try:
    import imageio
except ImportError:
    pass


__all__ = ['gif_from_images']


def gif_from_images(files,
                    gif_path,
                    fps=10,
                    loop=0,
                    reverse=False,
                    pingpong=False,
                    subrectangles=True,
                    delete_files=False):
    """Create an animated GIF from a series of images.

    Parameters
    ----------
    files : list
        The image series.
    gif_path : str
        The location to svae the- GIF.
    fps : int, optional
        Frames per second. Default is ``10``.
    loop : int
        The number of loops.
    reverse : bool, optional
        Flag for reversing the image series. Default is ``False``.
    pingpong : bool, optional
        Default is ``False``.
    subrectangles : bool, optional
        Default is ``True``.

    """
    if reverse:
        files.reverse()

    if pingpong:
        files += files[::-1]

    with imageio.get_writer(gif_path,
                            mode='I',
                            fps=fps,
                            loop=loop,
                            subrectangles=subrectangles) as writer:
        for filename in files:
            image = imageio.imread(filename)
            writer.append_data(image)

    if delete_files:
        for filename in files:
            os.remove(filename)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas

    base  = 'example-mesh-remeshing-on-mesh'
    files = [os.path.join(compas.TEMP, 'screenshots', base + '-' + str(i).zfill(4) + '.jpg') for i in range(5, 295, 10)]

    gif_from_images(files, os.path.join(compas.TEMP, base + '.gif'))
