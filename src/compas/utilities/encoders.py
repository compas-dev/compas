from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json


__all__ = ['DataDecoder', 'DataEncoder']


def cls_from_dtype(dtype):
    """Get the class object corresponding to a COMPAS data type specification.

    Parameters
    ----------
    dtype : str
        The data type of the COMPAS object in the following format:
        '{}/{}'.format(o.__class__.__module__, o.__class__.__name__).

    Returns
    -------
    :class:`compas.base.Base`

    Raises
    ------
    ValueError
        If the data type is not in the correct format.
    ImportError
        If the module can't be imported.
    AttributeError
        If the module doesn't contain the specified data type.

    """
    mod_name, attr_name = dtype.split('/')
    module = __import__(mod_name, fromlist=[attr_name])
    return getattr(module, attr_name)


class DecoderError(Exception):
    pass


class DataEncoder(json.JSONEncoder):
    """Data encoder for custom JSON serialisation with support for COMPAS data structures and geometric primitives.

    Notes
    -----
    In the context of Remote Procedure Calls,

    """

    def default(self, o):
        if hasattr(o, 'to_data'):
            value = o.to_data()
            if hasattr(o, 'dtype'):
                dtype = o.dtype
            else:
                dtype = "{}/{}".format(".".join(o.__class__.__module__.split(".")[:-1]), o.__class__.__name__)
            return {
                'dtype': dtype,
                'value': value
            }

        if hasattr(o, '__next__'):
            return list(o)

        try:
            import numpy as np
        except ImportError:
            pass
        else:
            if isinstance(o, np.ndarray):
                return o.tolist()
            if isinstance(o, (np.int32, np.int64)):
                return int(o)
            if isinstance(o, (np.float32, np.float64)):
                return float(o)

            elif isinstance(o, (np.int_, np.intc, np.intp, np.int8,
                                np.int16, np.int32, np.int64, np.uint8,
                                np.uint16, np.uint32, np.uint64)):
                return int(o)

            elif isinstance(o, (np.float_, np.float16, np.float32, np.float64)):
                return float(o)

            elif isinstance(o, np.bool_):
                return bool(o)

            elif isinstance(o, np.void):
                return None

        return super(DataEncoder, self).default(o)


class DataDecoder(json.JSONDecoder):
    """Data decoder for custom JSON serialisation with support for COMPAS data structures and geometric primitives."""

    def __init__(self, *args, **kwargs):
        super(DataDecoder, self).__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, o):
        if 'dtype' not in o:
            return o

        try:
            cls = cls_from_dtype(o['dtype'])

        except ValueError:
            raise DecoderError("The data type of the object should be in the following format: '{}/{}'.format(o.__class__.__module__, o.__class__.__name__)")

        except ImportError:
            raise DecoderError("The module of the data type can't be found.")

        except AttributeError:
            raise DecoderError("The data type can't be found in the specified module.")

        return cls.from_data(o['value'])


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
