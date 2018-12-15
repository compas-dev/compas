from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json


__all__ = ['DataDecoder', 'DataEncoder']


class DataEncoder(json.JSONEncoder):
    """Dump"""

    def default(self, o):
        from compas.datastructures import Datastructure

        if isinstance(o, Datastructure):
            return {
                'dtype': '{}/{}'.format(o.__class__.__module__, o.__class__.__name__),
                'value': o.to_data()
            }

        try:
            import numpy as np
        except ImportError:
            return super(DataEncoder, self).default(o)

        if isinstance(o, np.ndarray):
            return o.tolist()

        return super(DataEncoder, self).default(o)


class DataDecoder(json.JSONDecoder):
    """Load"""

    def __init__(self, *args, **kwargs):
        super(DataDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, o):
        if 'dtype' not in o:
            return o

        dtype = o['dtype']

        # if this doesn't work
        # raise an Error explaining the required encoding
        module, attr = dtype.split('/')
        cls = getattr(__import__(module, fromlist=[attr]), attr)

        return cls.from_data(o['value'])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
