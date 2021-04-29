from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

from compas.data import Data

__all__ = ['Datastructure']


class Datastructure(Data):

    def __init__(self):
        super(Datastructure, self).__init__()

    def __str__(self):
        """Generate a readable representation of the data of the datastructure."""
        return json.dumps(self.data, sort_keys=True, indent=4)


# ==============================================================================
#
# ==============================================================================

if __name__ == '__main__':
    pass
