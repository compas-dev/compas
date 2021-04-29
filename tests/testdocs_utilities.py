from compas.utilities import azync
from compas.utilities import coercing
from compas.utilities import colors
from compas.utilities import datetime
from compas.utilities import decorators
from compas.utilities import descriptors
from compas.utilities import encoders
from compas.utilities import images
from compas.utilities import itertools
from compas.utilities import maps
from compas.utilities import remote
from compas.utilities import ssh
from compas.utilities import xfunc


if __name__ == '__main__':
    import doctest

    doctest.testmod(azync)
    doctest.testmod(coercing)
    doctest.testmod(colors)
    doctest.testmod(datetime)
    doctest.testmod(decorators)
    doctest.testmod(descriptors)
    doctest.testmod(encoders)
    doctest.testmod(images)
    doctest.testmod(itertools)
    doctest.testmod(maps)
    doctest.testmod(remote)
    doctest.testmod(ssh)
    doctest.testmod(xfunc)
